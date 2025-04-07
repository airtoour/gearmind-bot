from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import Cars, Users

from sqlalchemy import select

from logger import logger


class CarsRepository(BaseRepository):
    """Репозиторий для определения методов работы с таблицей Cars"""
    model = Cars

    @classmethod
    async def get_car_id(cls, session: AsyncSession, tg_user_id: int):
        try:
            stmt = (
                select(cls.model.id)
                .join(Users, cls.model.user_id == Users.id)
                .where(Users.tg_user_id == tg_user_id)
            )

            result = await session.execute(stmt)
            return result.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(e)
            return None