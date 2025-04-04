from typing import Union

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.base_repository import BaseRepository
from db.models import Users

from logger import logger


class UsersRepository(BaseRepository):
    """Репозиторий для определения методов работы с таблицей Users"""
    model = Users

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by) -> Union[model, None]:
        try:
            stmt = (
                select(cls.model)
                .options(joinedload(cls.model.car))
                .filter_by(**filter_by)
            )
            result = await session.execute(stmt)
            return result.unique().scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в find_one_or_none {cls.model.__name__}: {e}")
            return None