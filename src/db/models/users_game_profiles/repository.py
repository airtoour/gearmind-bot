from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.base_repository import BaseRepository
from db.models import UsersGameProfiles, Users

from logger import logger


class UsersGameProfilesRepository(BaseRepository):
    """Репозиторий для работы с Игровым процессом пользователя"""
    model = UsersGameProfiles

    @classmethod
    async def get_user(cls, session: AsyncSession, telegram_id: int):
        try:
            stmt = (
                select(cls.model)
                .options(selectinload(cls.model.user))
                .join(Users, Users.id == cls.model.user_id)
                .where(Users.tg_user_id == telegram_id)
            )

            result = await session.execute(stmt)
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в get_user {cls.__name__}: {e}")
            return None

    @classmethod
    async def reward_user_experience(
            cls,
            session: AsyncSession,
            profile: UsersGameProfiles,
            experience: int
    ):
        try:
            if not profile:
                return None

            # Начисляем опыт
            profile.experience += experience

            # Проверяем, если опыт больше или равен порогу уровня
            while profile.experience >= profile.level_threshold:
                profile.level += 1
                profile.level_threshold += 50  # Увеличиваем порог на 50
                remains_exp = profile.experience - profile.level_threshold
                profile.experience = remains_exp  # Оставшийся опыт после повышения уровня

            await session.commit()
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в get_user {cls.model.__name__}: {e}")
            return None

