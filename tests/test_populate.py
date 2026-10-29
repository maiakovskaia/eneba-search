from sqlalchemy import func, select, text

from app.database.connection import AsyncSessionLocal
from app.database.models import GameOffers, Games
from scripts.populate_db import populate_database


async def count(model: type[Games] | type[GameOffers]) -> int:
    async with AsyncSessionLocal() as db:
        return await db.scalar(select(func.count()).select_from(model)) or 0


async def clear_tables() -> None:
    async with AsyncSessionLocal() as db:
        await db.execute(text("TRUNCATE TABLE game_offers, games, platforms CASCADE"))
        await db.commit()


async def test_populate_fills_an_empty_database() -> None:
    await clear_tables()

    await populate_database()

    assert await count(Games) == 3
    assert await count(GameOffers) == 13


async def test_populate_twice_does_not_duplicate_data() -> None:
    await clear_tables()

    await populate_database()
    await populate_database()

    assert await count(Games) == 3
    assert await count(GameOffers) == 13


async def test_populate_does_not_touch_existing_data() -> None:
    games_before = await count(Games)

    await populate_database()

    assert await count(Games) == games_before == 3
    assert await count(GameOffers) == 4


async def test_populate_works_after_sequences_have_advanced() -> None:
    await clear_tables()
    await populate_database()
    await clear_tables()

    await populate_database()

    assert await count(GameOffers) == 13
