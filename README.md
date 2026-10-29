# Game Offers Search

A small web application for browsing game offers and searching them with fuzzy matching.

Live demo: https://eneba.maiakovskaia.online/

The project started as a take-home assignment for a game marketplace.

## Stack

- Python 3.13, FastAPI, Jinja2, async SQLAlchemy 2.0, asyncpg, Alembic, RapidFuzz
- PostgreSQL 16, Docker Compose, Caddy
- uv, ruff, mypy, pytest
- GitHub Actions for CI and deployment

## Run locally

You need Docker with Compose.

```bash
cp .env.example .env
```

Fill in `.env`: any `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB`, `POSTGRES_HOST=localhost`, and `POSTGRES_PORT` set to a free port (for example `5433`).

```bash
docker compose up --build
```

Open http://localhost:8000. On start the web container applies migrations and fills an empty database with sample data; existing data is never touched.

`POSTGRES_PORT` is used everywhere: the database listens on it, publishes it on `127.0.0.1`, and the app connects to it, so one `.env` works both for the containers and for commands run on your machine. `WEB_PORT` (default `8000`) sets the published port of the web app.

## Development

```bash
make install   # dependencies and the pre-commit hook
make lint      # ruff, mypy and file hygiene hooks
make test      # integration tests against a throwaway PostgreSQL
make help      # all targets, including migrations
```

`make test` starts PostgreSQL from `docker-compose.test.yml` (settings in the committed `.env.test`), runs pytest and removes the container afterwards. The tests use the real application and a real database, with no mocks:

- `test_endpoints.py`: the HTTP contract (redirect, listing, search, prices, escaping of the query, static files, 404).
- `test_search.py`: fuzzy search (case, prefixes, typos, partial titles, ordering).
- `test_migrations.py`: migrations apply, downgrade and upgrade round trip, models match migrations.
- `test_populate.py`: the seed script is idempotent and does not touch existing data.

Tests refuse to run if the database name does not end with `_test`, because they truncate tables.

## Project structure

```
app/
  database/   engine, models, repository (queries and fuzzy search)
  routers/    HTTP layer
  services/   view data (prices)
  schemas/    response models
  templates/  Jinja2 templates
alembic/      migrations
scripts/      sample data seeding
tests/        integration tests
```

## API

| Endpoint | Description |
| --- | --- |
| `GET /` | Redirects to `/list`. |
| `GET /list` | All offers. |
| `GET /list?search=<query>` | Offers whose game title fuzzy-matches the query, best match first. |

## CI and deployment

`ci.yml` runs on pull requests: `lint`, then `test`, then `docker-build`, each only if the previous one passed. It runs the same `make` commands as local development, on GitHub-hosted runners.

`deploy.yml` runs on every push to `main` (and manually). It calls CI first, then a `deploy` job on a self-hosted runner writes `.env` from a secret, runs `docker compose up -d --build` and checks that the app answers.

Caddy runs on the host, not in Docker. It handles HTTPS and proxies to the app on `127.0.0.1`; the whole config is one file:

```
example.com {
	reverse_proxy 127.0.0.1:<WEB_PORT>
	encode gzip
}
```

To reproduce the setup you need:

1. A Linux host with Docker, Caddy and a domain pointing to it.
2. A repository-level self-hosted runner on that host with the extra label `eneba-deploy`, running as a dedicated user without `sudo`, in the `docker` group.
3. A GitHub environment `production`, limited to the `main` branch, with a secret `ENV_FILE` containing the `.env`:

```
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database>
POSTGRES_PORT=<free local port>
WEB_PORT=<free local port>
DEBUG=False
```

### Security of the pipeline

The repository is public and a deploy job runs on my own machine, so the main question is who can make that machine run code:

- The deploy workflow never runs on `pull_request` or `pull_request_target`, only on `push` to `main` and manual dispatch. A pull request, even from a fork, cannot reach the runner.
- Lint, tests and the Docker build run on GitHub-hosted runners; the self-hosted runner only deploys.
- Workflows from outside contributors need a maintainer's approval, and secrets are not passed to workflows from forks.
- The `production` environment and its secret are available only to `main`.
- The default token is read-only, and all actions are pinned to commit SHAs, so a moved tag cannot change the code that runs.
- The runner is an unprivileged user. Membership in the `docker` group is still equivalent to root on the host, which is why the rules above matter.

## Decisions and trade-offs

- **Layers.** Router, service and repository are separate, so search and pricing can be tested without HTTP.
- **Fuzzy search in Python.** All offers are loaded and scored with RapidFuzz. It needs no database extensions and is easy to read, but it scales linearly; `pg_trgm` with a GIN index would be the next step.
- **Tests on a real database.** Mocks would only test my assumptions about PostgreSQL. The cost is that Docker is needed to run tests.
- **Seed does not wipe data.** It fills only an empty database, so a restart or redeploy never deletes anything.
- **Caddy on the host.** One Caddy with one config; the application stays a plain Compose stack with no TLS logic.
- **Self-hosted runner instead of SSH from GitHub.** No SSH key to the host is stored in GitHub. The price is a machine that executes CI jobs, hence the restrictions above.
- **Image built on the deployment host.** No registry and no registry credentials. For heavier use I would build in CI and pull from a registry.
- **Nullable columns.** Several columns allow NULL in the schema, though the app always fills them; `NOT NULL` needs a migration and was left out.

## License

MIT, see [LICENSE](LICENSE).
