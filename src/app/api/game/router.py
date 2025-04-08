from app import TEMPLATES_DIR

from fastapi import APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession
from services.redis_cache.service import cache_service

from db.db_config import get_session_app
from db.models import GameProgressUsersRepository

from app.api.garage.router import router as garage_router
from app.api.game.schemas import CreateProgressSchema, UserProfileResponse
from app.exceptions.game import ProfileNotFound, CreateProfileBadRequest


router = APIRouter(prefix="/game", tags=["Игра"])
router.include_router(garage_router)

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("")
async def entry(request: Request):
    """Точка входа в игру"""
    return templates.TemplateResponse("entry_game.html", {"request": request})


@router.get("/init/{telegram_id}")
@cache(expire=120, key_builder=cache_service.model_key_builder)
async def init_progress(
    telegram_id: int,
    session: AsyncSession = Depends(get_session_app)
):
    """Проверка прогресса и имени пользователя для инициализации клиента."""
    progress = await GameProgressUsersRepository.get_user(session, tg_user_id=telegram_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "has_progress": True,
            "user_name": progress.user.name,  # noqa
            "level": progress.level,  # noqa
            "experience": progress.experience,  # noqa
            "last_wash": progress.last_wash_car_time  # noqa
        }
    )


@router.get("/get_profile/{telegram_id}", response_model=UserProfileResponse)
@cache(240)
async def get_profile_data(
    request: Request,  # noqa
    telegram_id: int,
    session: AsyncSession = Depends(get_session_app)
):
    """Получение данных прогресса пользователя"""
    progress = await GameProgressUsersRepository.get_user(session, tg_user_id=telegram_id)

    if not progress:
        raise ProfileNotFound

    return {
        "user_name": progress.user.name,  # noqa
        "level": progress.level,  # noqa
        "experience": progress.experience,  # noqa
        "last_wash": progress.last_wash_car_time  # noqa
    }


@router.get("/profile/{telegram_id}")
async def get_profile(
    request: Request,
    telegram_id: int,
    session: AsyncSession = Depends(get_session_app)
):
    profile_data = await get_profile_data(request, telegram_id, session)

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            **profile_data
        }
    )

@router.post("/create")
async def create_profile(
    data: CreateProgressSchema,
    session: AsyncSession = Depends(get_session_app)
):
    """Создание прогресса игры для пользователя"""
    added_progress = await GameProgressUsersRepository.add(
        session, user_id=data.user_id, car_id=data.car_id
    )

    if not added_progress:
        raise CreateProfileBadRequest

    return {
        "status": "ok",
        "message": "Ну что ж, начнём игру?",
        "data": added_progress.model_dump()
    }
