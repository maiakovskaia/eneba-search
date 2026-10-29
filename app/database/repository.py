from collections.abc import Sequence

from rapidfuzz import fuzz
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import GameOffers


async def get_all_offers(db: AsyncSession) -> Sequence[GameOffers]:
    query = select(GameOffers).options(
        joinedload(GameOffers.game), joinedload(GameOffers.platform)
    )
    result = await db.execute(query)
    return result.scalars().unique().all()


async def search_offers(db: AsyncSession, search_query: str) -> list[GameOffers]:
    normalized_query = search_query.lower().strip()

    stmt = select(GameOffers).options(
        joinedload(GameOffers.game), joinedload(GameOffers.platform)
    )
    result = await db.execute(stmt)
    all_offers = result.scalars().unique().all()

    scored_offers: list[tuple[float, GameOffers]] = []
    for offer in all_offers:
        offer_title = offer.game.title.lower().strip()

        scores = [
            fuzz.partial_ratio(normalized_query, offer_title),
            fuzz.token_set_ratio(normalized_query, offer_title),
            fuzz.ratio(normalized_query, offer_title),
        ]
        best_score = max(scores)

        if best_score > 60:
            scored_offers.append((best_score, offer))

    scored_offers.sort(key=lambda x: x[0], reverse=True)
    return [offer for score, offer in scored_offers]
