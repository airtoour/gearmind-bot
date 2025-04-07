from app import TEMPLATES_DIR

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import get_session_app
from db.models import UsersRepository, GameProgressUsersRepository

from .garage.router import router as garage_router
from ..schemas.game import CreateProgressSchema

from logger import logger


router = APIRouter(prefix="/game", tags=["Игра"])
router.include_router(garage_router)

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/{tg_user_id}")
async def get_game(
    request: Request,
    tg_user_id: int,
    session: AsyncSession = Depends(get_session_app)
):
    """
    Обработчик игры. Получает initData из заголовка X-Telegram-InitData,
    парсит его и проверяет соответствие id пользователя.
    """
    # Проверяем регистрацию пользователя
    user = await UsersRepository.find_one_or_none(session, tg_user_id=tg_user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Register in bot first")

    # Логика получения прогресса
    progress = await GameProgressUsersRepository.get_user(session, tg_user_id=tg_user_id)

    if not progress:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Register your progress first")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_name": user.name,
            "level": progress.level,
            "experience": progress.experience
        }
    )


@router.post("/create")
async def create_progress(data: CreateProgressSchema, session: AsyncSession = Depends(get_session_app)):
    """Создание прогресса игры для пользователя"""

    # Получение прогресса
    progress = await GameProgressUsersRepository.find_one_or_none(
        session, user_id=data.user_id
    )

    # Если прогресс найден
    if progress:
        # Получение пользователя
        user = await UsersRepository.find_one_or_none(
            session, id=data.user_id
        )

        # Редирект на главную страницу игры
        return RedirectResponse(
            url=f"/game/{user.tg_user_id}",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Создаём новый Прогресс
    added_progress = await GameProgressUsersRepository.add(
        session, user_id=data.user_id, car_id=data.car_id
    )

    # Ответ сервера
    return {
        "status": "ok",
        "message": "Ну что ж, начнём игру?",
        "data": added_progress.model_dump()
    }


@router.get("/level/{tg_user_id}")
async def get_user_level(tg_user_id: int, session: AsyncSession = Depends(get_session_app)):
    try:
        progress = await GameProgressUsersRepository.get_level(session, tg_user_id)
        return progress
    except HTTPException as e:
        logger.error(e)
        return {"status": "fail", "error": str(e)}
