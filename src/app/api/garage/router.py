from datetime import datetime, timedelta

from .schemas import (
    WashStatusReturnSchema,
    WashCarSchema,
    WashedCarReturnSchema
)

from db.db_config import get_session_app
from db.models import GameProgressUsersRepository

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from services.game.service import GearGameService

from logger import logger


router = APIRouter(prefix="/garage")


@router.get("/wash/status", response_model=WashStatusReturnSchema)
async def check_wash_car(tg_user_id: int, session: AsyncSession = Depends(get_session_app)):
    """Запрос на проверку 'Загрязнённости' автомобиля"""
    try:
        progress = await GameProgressUsersRepository.get_user(session, tg_user_id)

        if not progress:
            return RedirectResponse(f"/game/{tg_user_id}")

        if progress.last_wash_car_time + timedelta(hours=6) < datetime.now():
            return {
                "status": "ok",
                "can_wash": True,
                "message": "Ваш автомобиль ждёт, пока Вы его помоете"
            }

        return {
            "status": "ok",
            "can_wash": False,
            "message":
                "Автомобиль ещё не такой грязный, "
                "чтобы его мыть, можно ещё покататься! "
                "Хорошей дороги!"
        }
    except Exception as e:
        logger.error(e)
        return {
            "status": "fail",
            "can_wash": False,
            "message": "Произошла ошибка при проверке, извините"
        }


@router.patch("/wash", response_model=WashedCarReturnSchema)
async def wash_car(data: WashCarSchema, session: AsyncSession = Depends(get_session_app)):
    """Запрос на помывку автомобиля"""
    progress = None
    response_data = {
        "status": "fail",
        "washed": False,
        "data": {
            "new_level": None,
            "last_wash_car_time": None,
            "message": ""
        }
    }

    try:
        progress = await GameProgressUsersRepository.get_user(session, data.tg_user_id)
        service = GearGameService(data.tg_user_id, session, progress)

        if not progress:
            response_data["data"]["message"] = "Профиль не найден"
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_302_FOUND,
                headers={"Location": f"/game/{data.tg_user_id}"}
            )

        if progress.last_wash_car_time + timedelta(hours=6) < datetime.now():
            washed = await service.wash(100)

            if not washed:
                response_data["data"]["message"] = "Ошибка при мытье автомобиля, попробуйте позже"
                return JSONResponse(content=response_data, status_code=status.HTTP_400_BAD_REQUEST)

            response_data["status"] = "ok"
            response_data["washed"] = True
            response_data["data"]["new_level"] = washed.level  # type: ignore
            response_data["data"]["last_wash_car_time"] = datetime.now()  # type: ignore
            response_data["data"]["message"] = "Автомобиль помыт! Следующая мойка через 6 часов!"

            return response_data
        else:
            response_data["data"]["message"] = "Мойка доступна через 6 часов"
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_302_FOUND,
                headers={"Location": f"/game/wash/status?tg_user_id={data.tg_user_id}"}
            )
    except Exception as e:
        logger.error(e)
        response_data["data"]["message"] = "Ошибка при обработке запроса"

        if progress:
            response_data["data"]["new_level"] = progress.level  # type: ignore

        return response_data
