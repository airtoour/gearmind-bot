from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import GameProgressUsers, Users, UsersRepository

from logger import logger


class GameProgressUsersRepository(BaseRepository):
    """Репозиторий для работы с Игровым процессом пользователя"""
    model = GameProgressUsers

    @classmethod
    async def get_user(cls, session: AsyncSession, tg_user_id: int):
        try:
            stmt = (
                select(cls.model)
                .join(Users, Users.id == cls.model.user_id)
                .where(Users.tg_user_id == tg_user_id)
            )

            result = await session.execute(stmt)
            return result.unique().scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в get_user {cls.model.__name__}: {e}")
            return None

    @classmethod
    async def add_progress(cls, session: AsyncSession, tg_id: int, **data):
        try:
            user = await UsersRepository.find_one_or_none(session, tg_user_id=tg_id)

            stmt = (
                insert(cls.model)
                .values(user_id=user.id, **data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            return result.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в add_progress {cls.model.__name__}: {e}")
            return None
