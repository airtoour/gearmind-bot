from fastapi import APIRouter

from .garage.router import router as garage_router


router = APIRouter(prefix="/game", tags=["Игра"])

router.include_router(garage_router)
