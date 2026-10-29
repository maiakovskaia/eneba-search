from sqlalchemy.ext.asyncio import AsyncSession

from app.database import GameOffers, get_all_offers, search_offers
from app.schemas import GameOfferResponse


class GameService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_offers(self) -> list[GameOfferResponse]:
        all_offers = await get_all_offers(self.db)
        return self._extract_offers(all_offers)

    async def search_offers(self, search_query: str) -> list[GameOfferResponse]:
        filtered_offers = await search_offers(self.db, search_query)
        if not filtered_offers:
            return []
        return self._extract_offers(filtered_offers)

    @staticmethod
    def _extract_offers(offers: list[GameOffers]) -> list[GameOfferResponse]:
        result = []
        for offer in offers:
            final_price = None
            if offer.discount_percent:
                final_price = offer.full_price * (1 - offer.discount_percent / 100)

            normalized_offer = GameOfferResponse(
                id=offer.id,
                title=offer.game.title,
                image_url=offer.game.image_url,
                platform=offer.platform.name,
                platform_icon_url=offer.platform.icon_url,
                region=offer.region,
                edition=offer.edition,
                likes_count=offer.likes_count,
                full_price=offer.full_price,
                final_price=final_price,
                discount_percent=offer.discount_percent,
                cashback_amount=offer.cashback_amount,
            )
            result.append(normalized_offer)

        return result
