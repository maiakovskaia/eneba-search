"""
Populate the database with sample data.

Run with: python -m scripts.populate_db
"""

import asyncio
import logging

from sqlalchemy import text

from app.database.connection import AsyncSessionLocal
from app.database.models import GameOffers, GamePlatforms, Games

logger = logging.getLogger(__name__)


async def populate_database():
    async with AsyncSessionLocal() as db:
        try:
            # Clear existing data
            await db.execute(
                text(
                    "TRUNCATE TABLE game_offers, games, platforms "
                    "RESTART IDENTITY CASCADE"
                )
            )

            # Create Games
            games_data = [
                Games(title="FIFA 23", image_url="/static/img/fifa23.jpeg"),
                Games(title="Red Dead Redemption 2", image_url="/static/img/rdr2.jpeg"),
                Games(
                    title="Split Fiction", image_url="/static/img/split_fiction.jpeg"
                ),
            ]
            db.add_all(games_data)
            await db.flush()

            # Create Platforms
            platforms_data = [
                GamePlatforms(name="Origin", icon_url="/static/img/origin.svg"),
                GamePlatforms(name="Steam", icon_url="/static/img/steam.svg"),
                GamePlatforms(name="Xbox", icon_url="/static/img/xbox.svg"),
            ]
            db.add_all(platforms_data)
            await db.flush()

            # Create Game Offers
            offers_data = [
                # FIFA 23 offers
                GameOffers(
                    game_id=1,
                    platform_id=1,
                    region="GLOBAL",
                    edition="Standard Edition",
                    likes_count=1250,
                    full_price=59.99,
                    discount_percent=25,
                    cashback_amount=2.99,
                ),
                GameOffers(
                    game_id=1,
                    platform_id=1,
                    region="EUROPE",
                    edition="Ultimate Edition",
                    likes_count=890,
                    full_price=89.99,
                    discount_percent=15,
                    cashback_amount=None,
                ),
                GameOffers(
                    game_id=1,
                    platform_id=2,
                    region="GLOBAL",
                    edition="Standard Edition",
                    likes_count=2100,
                    full_price=54.99,
                    discount_percent=None,
                    cashback_amount=1.50,
                ),
                GameOffers(
                    game_id=1,
                    platform_id=3,
                    region="EUROPE",
                    edition="Champions Edition",
                    likes_count=670,
                    full_price=79.99,
                    discount_percent=20,
                    cashback_amount=3.20,
                ),
                # Red Dead Redemption 2 offers
                GameOffers(
                    game_id=2,
                    platform_id=2,
                    region="GLOBAL",
                    edition="Ultimate Edition",
                    likes_count=3450,
                    full_price=59.99,
                    discount_percent=30,
                    cashback_amount=2.50,
                ),
                GameOffers(
                    game_id=2,
                    platform_id=2,
                    region="EUROPE",
                    edition="Standard Edition",
                    likes_count=2890,
                    full_price=39.99,
                    discount_percent=None,
                    cashback_amount=None,
                ),
                GameOffers(
                    game_id=2,
                    platform_id=3,
                    region="GLOBAL",
                    edition="Special Edition",
                    likes_count=1560,
                    full_price=49.99,
                    discount_percent=25,
                    cashback_amount=None,
                ),
                GameOffers(
                    game_id=2,
                    platform_id=1,
                    region="EUROPE",
                    edition=None,
                    likes_count=990,
                    full_price=44.99,
                    discount_percent=10,
                    cashback_amount=1.80,
                ),
                # Split Fiction offers
                GameOffers(
                    game_id=3,
                    platform_id=2,
                    region="GLOBAL",
                    edition="EA App Key",
                    likes_count=626,
                    full_price=49.99,
                    discount_percent=18,
                    cashback_amount=4.50,
                ),
                GameOffers(
                    game_id=3,
                    platform_id=3,
                    region="EUROPE",
                    edition="XBOX LIVE Key",
                    likes_count=500,
                    full_price=49.99,
                    discount_percent=32,
                    cashback_amount=3.76,
                ),
                GameOffers(
                    game_id=3,
                    platform_id=3,
                    region="GLOBAL",
                    edition="XBOX LIVE Key",
                    likes_count=1039,
                    full_price=49.99,
                    discount_percent=30,
                    cashback_amount=3.87,
                ),
                GameOffers(
                    game_id=3,
                    platform_id=1,
                    region="EUROPE",
                    edition="Nintendo Switch eShop Key",
                    likes_count=288,
                    full_price=49.99,
                    discount_percent=None,
                    cashback_amount=3.99,
                ),
                GameOffers(
                    game_id=3,
                    platform_id=2,
                    region="EUROPE",
                    edition="Steam Key",
                    likes_count=820,
                    full_price=44.99,
                    discount_percent=22,
                    cashback_amount=None,
                ),
            ]
            db.add_all(offers_data)

            await db.commit()
            logger.info(
                "Database populated: %d games, %d platforms, %d game offers",
                len(games_data),
                len(platforms_data),
                len(offers_data),
            )

        except Exception:
            await db.rollback()
            logger.exception("Error populating database")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(populate_database())
