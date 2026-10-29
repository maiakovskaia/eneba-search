from fastapi import APIRouter

from app.routers.games import router as games_router

router = APIRouter()
router.include_router(games_router, prefix="/list", tags=["games"])
