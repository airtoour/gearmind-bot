from app import TEMPLATES_DIR

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import get_session_app
from db.models import UsersRepository, GameProgressUsersRepository

from .garage.router import router as garage_router
from ..schemas.game import CreateProgressSchema
from ...dependencies import verify_telegram_data

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
    """Обработчик игры с прямой проверкой Telegram данных"""

    # Получаем initData из заголовков
    init_data = request.headers.get("X-Telegram-InitData")

    logger.debug(init_data)

    # Валидируем данные Telegram
    parsed_data = verify_telegram_data(init_data)

    logger.debug(parsed_data)

    if not parsed_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Telegram auth")

    # Извлекаем ID пользователя
    user_data = parsed_data.get("user", {})
    telegram_user_id = user_data.get("id")

    logger.debug(f"{user_data} {telegram_user_id}")

    # Проверяем соответствие ID в URL и данных Telegram
    if int(telegram_user_id) != tg_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ID mismatch")

    # Проверяем регистрацию пользователя
    user = await UsersRepository.find_one_or_none(session, tg_user_id=tg_user_id)

    logger.debug(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Register in bot first")

    # Логика получения прогресса
    progress = await GameProgressUsersRepository.get_user(session, tg_user_id=tg_user_id)

    logger.debug(progress)

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
    added_progress = await GameProgressUsersRepository.add(
        session, user_id=data.id, car_id=data.car.id
    )
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