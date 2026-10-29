import asyncio
from collections.abc import AsyncIterator

import pytest
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from alembic import command
from app.config import settings
from app.database.connection import AsyncSessionLocal
from app.database.models import GameOffers, GamePlatforms, Games
from main import app


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    if not settings.database.db.endswith("_test"):
        pytest.exit(
            f"Refusing to run: database {settings.database.db!r} is not a test "
            "database (its name must end with '_test').",
            returncode=2,
        )
    return Config(toml_file="pyproject.toml")


@pytest.fixture(scope="session", autouse=True)
async def migrated_db(alembic_config: Config) -> None:
    await asyncio.to_thread(command.upgrade, alembic_config, "head")


@pytest.fixture(autouse=True)
async def offers(migrated_db: None) -> None:
    async with AsyncSessionLocal() as db:
        await db.execute(
            text(
                "TRUNCATE TABLE game_offers, games, platforms RESTART IDENTITY CASCADE"
            )
        )
        fifa = Games(title="FIFA 23", image_url="/static/img/fifa23.jpeg")
        rdr2 = Games(title="Red Dead Redemption 2", image_url="/static/img/rdr2.jpeg")
        split = Games(title="Split Fiction", image_url="/static/img/split.jpeg")
        steam = GamePlatforms(name="Steam", icon_url="/static/img/steam.svg")
        xbox = GamePlatforms(name="Xbox", icon_url="/static/img/xbox.svg")
        db.add_all([fifa, rdr2, split, steam, xbox])
        await db.flush()
        db.add_all(
            [
                GameOffers(
                    game_id=fifa.id,
                    platform_id=steam.id,
                    region="GLOBAL",
                    edition="Standard Edition",
                    likes_count=10,
                    full_price=60.0,
                    discount_percent=25,
                    cashback_amount=2.5,
                ),
                GameOffers(
                    game_id=fifa.id,
                    platform_id=xbox.id,
                    region="EUROPE",
                    full_price=50.0,
                ),
                GameOffers(
                    game_id=rdr2.id,
                    platform_id=steam.id,
                    region="GLOBAL",
                    full_price=40.0,
                    discount_percent=50,
                ),
                GameOffers(
                    game_id=split.id,
                    platform_id=xbox.id,
                    region="EUROPE",
                    full_price=45.0,
                ),
            ]
        )
        await db.commit()


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
