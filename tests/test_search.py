import pytest

from app.database.connection import AsyncSessionLocal
from app.database.repository import search_offers


async def search_titles(query: str) -> list[str]:
    async with AsyncSessionLocal() as db:
        offers = await search_offers(db, query)
        return [offer.game.title for offer in offers]


@pytest.mark.parametrize("query", ["FIFA 23", "fifa 23", "  fifa 23  ", "FIFA"])
async def test_search_ignores_case_and_surrounding_spaces(query: str) -> None:
    assert await search_titles(query) == ["FIFA 23", "FIFA 23"]


@pytest.mark.parametrize("query", ["fif", "fifa2", "fifa23", "fifaa 23"])
async def test_search_tolerates_prefixes_and_typos(query: str) -> None:
    titles = await search_titles(query)

    assert titles[:2] == ["FIFA 23", "FIFA 23"]


async def test_search_matches_a_part_of_the_title() -> None:
    assert await search_titles("red dead") == ["Red Dead Redemption 2"]


async def test_search_returns_every_offer_of_the_matching_game() -> None:
    titles = await search_titles("fifa 23")

    assert len(titles) == 2


async def test_search_with_no_match_returns_nothing() -> None:
    assert await search_titles("qwerty") == []


async def test_search_orders_best_match_first() -> None:
    titles = await search_titles("split fiction")

    assert titles[0] == "Split Fiction"
