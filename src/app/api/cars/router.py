from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import get_session_app
from db.models.cars.repository import CarsRepository

router = APIRouter(prefix="/cars", tags=["Автомобили"])


@router.get("/{tg_user_id}")
async def get_car(tg_user_id: int, session: AsyncSession = Depends(get_session_app)):
    car = await CarsRepository.get_car_id(session, tg_user_id)

    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    return car
