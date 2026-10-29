# Eneba Game Search

A web application for searching and browsing game offers with fuzzy search functionality. Built as a test assignment for an internship at [Eneba](https://www.eneba.com/).

## About

This application provides a game marketplace interface where users can search for games using fuzzy matching. The search supports partial matches and typo tolerance (e.g., "fifa2" matches "FIFA 23", "fif" matches "FIFA 23").

## Tech Stack

**Backend:**
- FastAPI (Python 3.13)
- PostgreSQL (async with asyncpg)
- SQLAlchemy (async ORM)
- Alembic (migrations)
- RapidFuzz (fuzzy search)

**Frontend:**
- Jinja2 templates
- HTML/CSS
- Vanilla JavaScript

**Infrastructure:**
- Docker & Docker Compose
- Caddy (reverse proxy with auto-SSL)
- UV (package manager)

**Database:**
- PostgreSQL 16
- Sample data: FIFA 23, Red Dead Redemption 2, Split Fiction

## Quick Start (Local Development)

You can launch the application locally via Docker Compose. Make sure you have Docker and Docker Compose installed.

1. Clone the repository:
```bash
git clone https://github.com/aigelia/eneba-search
cd eneba-search
```

2. Create `.env` file and add PostgreSQL credentials:
```bash
cp .env.example .env
```

3. Start the application:
```bash
docker compose up --build
```

4. Open in browser:
```
http://localhost:8000
```

The application will:
- Create and migrate the database
- Populate it with sample game data
- Start the web server on port 8000

## Production Deployment

1. On your server, clone the repository and navigate to the project directory, then create `.env` with your production settings. Make sure you have added your domain name to `.env`, as well as an A-record pointing to your server's IP address.

2. Launch Docker Compose with the production profile (includes Caddy with auto-SSL):
```bash
docker compose --profile prod up -d --build
```

3. The application will be available at:
- HTTP: `http://yourdomain.com` (redirects to HTTPS)
- HTTPS: `https://yourdomain.com` (with auto-provisioned SSL certificate)

## API Endpoints

- `GET /` - Redirects to `/list`
- `GET /list` - Display all game offers
- `GET /list?search=<query>` - Search games with fuzzy matching

## Project Purpose

Created as a test assignment for the [Eneba](https://www.eneba.com) internship.
