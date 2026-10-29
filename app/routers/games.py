from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.services import GameService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def list_offers(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    search: Annotated[str | None, Query()] = None,
) -> Response:
    """List all game offers or search by game name (fuzzy matching)."""
    service = GameService(db)
    query = (search or "").strip()
    if query:
        offers = await service.search_offers(query)
    else:
        offers = await service.get_all_offers()

    return templates.TemplateResponse(
        request,
        "list.html",
        {
            "games": offers,
            "search_query": query,
            "results_count": len(offers),
        },
    )
