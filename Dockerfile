FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock* ./

ENV UV_NO_DEV=1

RUN uv sync --locked

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run python -m scripts.populate_db && uv run uvicorn main:app --host 0.0.0.0 --port 8000"]
