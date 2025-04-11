from typing import List

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import Tasks, UsersTasks, Users
from db.models.users_game_profiles.models import UsersGameProfiles

from logger import logger


class TasksRepository(BaseRepository):
    """Репозиторий для работы со справочником Заданий игры"""
    model = Tasks

    users_tasks: UsersTasks = aliased(UsersTasks)
    users_profiles: UsersGameProfiles = aliased(UsersGameProfiles)
    users: Users = aliased(Users)

    @classmethod
    async def get_all(cls, session: AsyncSession, telegram_id: int) -> List[dict]:
        """Поиск всех активных заданий игрока"""
        try:
            stmt = (
                select(cls.model, cls.users_tasks.current_value)
                .join(cls.users_tasks, cls.users_tasks.task_id == cls.model.id)
                .join(cls.users_profiles, cls.users_profiles.id == cls.users_tasks.profile_id)
                .join(cls.users, cls.users.id == cls.users_profiles.user_id)
                .where(
                    cls.users.tg_user_id == telegram_id,
                    cls.model.is_active.is_(True)
                )
            )
            result = await session.execute(stmt)
            return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(e)
            return []

    @classmethod
    async def find_liked(cls, session: AsyncSession, pattern: str) -> List[model]:
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.description.ilike(pattern))
            )
            result = await session.execute(stmt)
            return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(e)
            return []


if __name__ == "__main__":
    import asyncio
    from db.db_config import async_session_maker

    async def main():
        async with async_session_maker() as session:
            res = await TasksRepository.find_liked(session, "помой%")
            print(res)

    asyncio.run(main())