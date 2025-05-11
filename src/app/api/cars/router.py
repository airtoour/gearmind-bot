from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.cars import CarNotFound
from db.db_config import get_session_app
from db.models.cars.repository import CarsRepository


router = APIRouter(prefix="/cars", tags=["Автомобили"])


@router.get("/{telegram_id}")
@cache(60)
async def get_users_car(telegram_id: int, session: AsyncSession = Depends(get_session_app)):
    """Получение автомобиля пользователя"""
    car = await CarsRepository.get_car_id(session, telegram_id)

    if not car:
        raise CarNotFound

    return car
