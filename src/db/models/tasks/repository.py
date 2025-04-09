from typing import List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import Tasks, UsersTasks, Users

from logger import logger


class TasksRepository(BaseRepository):
    """Репозиторий для работы со справочником Заданий игры"""
    model = Tasks

    @classmethod
    async def get_all(cls, session: AsyncSession, telegram_id: int) -> List[dict]:
        """Поиск всех активных заданий игрока"""
        try:
            stmt = (
                select(cls.model, UsersTasks.current_value)
                .join(UsersTasks, UsersTasks.task_id == cls.model.id)
                .join(Users, Users.id == UsersTasks.user_id)
                .where(
                    Users.tg_user_id == telegram_id,
                    cls.model.is_active.is_(True)
                )
            )
            result = await session.execute(stmt)
            return result.unique().mappings().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(e)
            return []


if __name__ == "__main__":
    import asyncio
    from db.db_config import async_session_maker

    async def main():
        async with async_session_maker() as session:
            res = await TasksRepository.get_all(session, 1068989629)
            print(res)

    asyncio.run(main())