from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.api.tasks.schemas import TaskInfo
from app.api.users_tasks.schemas import UsersTaskCompleteSchema
from db.db_config import get_session_app
from db.models import TasksRepository
from db.models.users_game_profiles.repository import UsersGameProfilesRepository

from services.game.service import GearGameService

router = APIRouter(prefix="/tasks", tags=["Задания GearGame"])


@router.get("/{telegram_id}/all", response_model=List[TaskInfo])
async def get_all_tasks(
    telegram_id: int,
    session: AsyncSession = Depends(get_session_app)
):
    """Получение всех активных Заданий Игрока"""
    rows = await TasksRepository.get_all(session, telegram_id)

    return [
        TaskInfo(
            title=row["Tasks"].title,
            description=row["Tasks"].description,
            type=row["Tasks"].type,
            target_value=row["Tasks"].target_value,
            reward_xp=row["Tasks"].reward_xp,
            current_value=row["current_value"]
        )
        for row in rows
    ]

@router.post("/{task_id}/complete")
async def task_complete(
    data: UsersTaskCompleteSchema,
    session: AsyncSession = Depends(get_session_app)
):
    profile = await UsersGameProfilesRepository.get_user(session, data.telegram_id)
    game_service = GearGameService(session, profile)
    complete = await game_service.process_task(data.task_id)

    if not complete:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "not completed", "message": "Задание не обновлено по ошибке сервера"}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": ""}
    )
