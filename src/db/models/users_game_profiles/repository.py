from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.base_repository import BaseRepository
from db.models import UsersGameProfiles, Users

from logger import logger


class UsersGameProfilesRepository(BaseRepository):
    """Репозиторий для работы с Игровым процессом пользователя"""
    model = UsersGameProfiles

    @classmethod
    async def get_user(cls, session: AsyncSession, tg_user_id: int):
        try:
            stmt = (
                select(cls.model)
                .options(joinedload(cls.model.user))
                .join(Users, Users.id == cls.model.user_id)
                .where(Users.tg_user_id == tg_user_id)
            )

            result = await session.execute(stmt)
            return result.unique().scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в get_user {cls.model.__name__}: {e}")
            return None
