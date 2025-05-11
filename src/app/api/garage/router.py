from datetime import datetime, timedelta

from db.models.tasks.repository import TasksRepository
from .schemas import (
    WashStatusReturnSchema,
    WashCarSchema,
    WashedCarReturnSchema
)

from db.db_config import get_session_app
from db.models import UsersGameProfilesRepository

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from services.game.service import GearGameService

from logger import logger


router = APIRouter(prefix="/garage")


@router.get("/wash/status", response_model=WashStatusReturnSchema)
async def check_wash_car(telegram_id: int, session: AsyncSession = Depends(get_session_app)):
    """Запрос на проверку 'Загрязнённости' автомобиля"""
    try:
        profile = await UsersGameProfilesRepository.get_user(session, telegram_id)

        if not profile:
            return RedirectResponse(f"/game/{telegram_id}")

        # Проверка на None для last_wash_car_time
        if profile.last_wash_car_time is None:
            profile.last_wash_car_time = datetime.now()  # Если нет времени, устанавливаем текущее

        next_wash_time = profile.last_wash_car_time + timedelta(hours=6)
        current_time = datetime.now()

        if next_wash_time <= current_time:
            return {
                "status": "ok",
                "can_wash": True,
                "message": "Ваш автомобиль ждёт, пока Вы его помоете 🧽🪣",
                "next_wash_at": next_wash_time.isoformat()
            }

        time_remaining = next_wash_time - datetime.now()
        hours_left = time_remaining.seconds // 3600
        minutes_left = (time_remaining.seconds % 3600) // 60
        seconds_left = (time_remaining.seconds % 60)

        return {
            "status": "ok",
            "can_wash": False,
            "message": f"🚿 Следующая мойка доступна через {hours_left}ч {minutes_left}м {seconds_left}с",
            "next_wash_at": next_wash_time.isoformat()
        }
    except Exception as e:
        logger.error(f"Ошибка при проверке статуса мытья: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при проверке, извините"
        )


@router.patch("/wash", response_model=WashedCarReturnSchema)
async def wash_car(data: WashCarSchema, session: AsyncSession = Depends(get_session_app)):
    """Запрос на помывку автомобиля"""
    washed = None

    response_data = {
        "status": "fail",
        "washed": False,
        "data": {
            "last_wash_car_time": None,
            "message": ""
        }
    }

    try:
        profile = await UsersGameProfilesRepository.get_user(session, data.tg_user_id)
        service = GearGameService(session, profile)

        tasks = await TasksRepository.find_liked(session, pattern="помой%")

        if not profile:
            response_data["data"]["message"] = "Профиль не найден"
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_302_FOUND,
                headers={"Location": f"/game/{data.tg_user_id}"}
            )

        # Проверка, можно ли помыть
        if profile.last_wash_car_time is None:
            profile.last_wash_car_time = datetime.now() - timedelta(hours=6)

        if profile.last_wash_car_time + timedelta(hours=6) < datetime.now():
            for task in tasks:
                washed = await service.process_task(task)

            if not washed:
                response_data["data"]["message"] = "Ошибка при мытье автомобиля, попробуйте позже"
                return JSONResponse(content=response_data, status_code=status.HTTP_400_BAD_REQUEST)

            # Обновление времени мойки
            profile.last_wash_car_time = datetime.now()
            await session.commit()

            response_data["status"] = "ok"
            response_data["washed"] = True
            response_data["data"]["last_wash_car_time"] = profile.last_wash_car_time.isoformat()  # type: ignore
            response_data["data"]["message"] = "Автомобиль помыт! Следующая мойка через 6 часов!"

            return response_data
        else:
            response_data["status"] = "error"
            response_data["data"]["message"] = f"Мойка доступна через 6 часов"
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса на мойку: {e}")
        response_data["data"]["message"] = "Ошибка при обработке запроса"
        return response_data
