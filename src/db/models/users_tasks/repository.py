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

            return result.unique().scalars().all()
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(e)
            return []
