from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.tasks.schemas import TaskInfo
from db.db_config import get_session_app
from db.models import TasksRepository
from db.models.users_tasks.schemas import AllUsersTaskSchema


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
            title=row['Tasks'].title,
            description=row['Tasks'].description,
            type=row['Tasks'].type,
            target_value=row['Tasks'].target_value,
            reward_xp=row['Tasks'].reward_xp,
            current_value=row['current_value']
        )
        for row in rows
    ]

