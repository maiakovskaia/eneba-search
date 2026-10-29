import asyncio

from alembic.config import Config
from sqlalchemy import inspect

from alembic import command
from app.database.connection import engine

APP_TABLES = {"games", "platforms", "game_offers"}


async def table_names() -> set[str]:
    async with engine.connect() as conn:
        names = await conn.run_sync(lambda c: set(inspect(c).get_table_names()))
    return names


async def test_upgrade_creates_app_tables(alembic_config: Config) -> None:
    names = await table_names()

    assert names >= APP_TABLES
    assert "currencies" not in names


async def test_downgrade_and_upgrade_round_trip(alembic_config: Config) -> None:
    try:
        await asyncio.to_thread(command.downgrade, alembic_config, "base")
        assert not APP_TABLES & await table_names()
    finally:
        await asyncio.to_thread(command.upgrade, alembic_config, "head")

    assert await table_names() >= APP_TABLES


async def test_models_match_migrations(alembic_config: Config) -> None:
    await asyncio.to_thread(command.check, alembic_config)
