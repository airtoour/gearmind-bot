from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import get_session_app
from db.models import UsersRepository, GameProgressUsersRepository

from .garage.router import router as garage_router
from ..schemas.game import BasePageReturnSchema

from logger import logger


router = APIRouter(prefix="/game", tags=["Игра"])
router.include_router(garage_router)


@router.get("/{tg_user_id}", response_model=BasePageReturnSchema)
async def get_game(tg_user_id: int, session: AsyncSession = Depends(get_session_app)):
    """Проверка профиля пользователя в Игре"""
    try:
        added_profile = None

        user = await UsersRepository.find_one_or_none(session, tg_user_id=tg_user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Сначала потребуется зарегистрироваться!"
            )

        progress = await GameProgressUsersRepository.get_user(
            session, tg_user_id=user.tg_user_id
        )

        if not progress:
            added_profile = await GameProgressUsersRepository.add(
                session, user_id=user.id, car_id=user.car.id
            )

        return {
            "status": "ok",
            "user_name": user.name,
            "level": progress.level if progress else added_profile.level,
            "experience": progress.experience if progress else added_profile.experience
        }
    except HTTPException as e:
        logger.error(e)
        return {"status": "fail", "error": str(e)}


@router.get("/level/{tg_user_id}")
async def get_user_level(tg_user_id: int, session: AsyncSession = Depends(get_session_app)):
    try:
        progress = await GameProgressUsersRepository.get_level(session, tg_user_id)
        return progress
    except HTTPException as e:
        logger.error(e)
        return {"status": "fail", "error": str(e)}