.DEFAULT_GOAL := help

##@ General

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: \033[36mmake <target>\033[0m\n\nAvailable targets:\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ App management

.PHONY: install
install: ## Install dependencies and git hooks.
	uv sync
	uv run pre-commit install

.PHONY: up
up: ## Run the application in Docker containers.
	docker compose up -d

.PHONY: build
build: ## Build & run the application in Docker containers.
	docker compose up -d --build

.PHONY: down
down: ## Stop the Docker containers.
	docker compose down

##@ Migrations

.PHONY: up-db
up-db: ## Start the DB Docker container separately from the application.
	docker compose up -d db

.PHONY: down-db
down-db: ## Stop the DB Docker container.
	docker compose down db

.PHONY: guard-msg
guard-msg:
	@test -n "$(msg)" || { echo 'msg argument is required. Usage: make migration msg="init"' >&2; exit 1; }

.PHONY: migration
migration: guard-msg ## Generate a new migration. Requires DB container to be running. Usage: make migration msg="init"
	uv run alembic revision --autogenerate -m "$(msg)"

.PHONY: migrate
migrate: ## Apply migrations. Requires DB container to be running.
	uv run alembic upgrade head

##@ Linting and formatting

.PHONY: lint
lint: ## Run linting and formatting checks (pre-commit on all files).
	uv run pre-commit run --all-files
