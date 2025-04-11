from datetime import datetime
from typing import List, Union

from sqlalchemy import update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import UsersTasks, Tasks
from db.models.tasks.schemas import TasksType

from logger import logger


class UsersTasksRepository(BaseRepository):
    """Репозиторий для работы с прогрессом Заданий"""
    model = UsersTasks

    @classmethod
    async def reset_daily(cls, session: AsyncSession) -> Union[List[model]]:
        try:
            stmt = (
                update(cls.model)
                .values(
                    current_value=0,
                    is_completed=False,
                    assigned_at=datetime.now(),
                    completed_at=None
                )
                .where(cls.model.task_id.in_(
                    select(Tasks.id).where(
                        Tasks.type == TasksType.DAILY
                    )
                ))
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()

            return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(e)
            return []

    @classmethod
    async def increment_task(cls, session: AsyncSession, task: UsersTasks):
        try:
            if not task:
                return None

            # Увеличиваем current_value
            task.current_value += 1

            # Если достигнут target_value, задание завершено
            if task.current_value >= task.task.target_value:
                task.is_completed = True
                task.completed_at = datetime.now()
                task.task.is_active = False

            await session.commit()
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(e)
            return None

