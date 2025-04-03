from typing import List, Union

from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger


class BaseRepository:
    model = None

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by) -> Union[model, None]:
        """Метод поиска записи, возвращает её или ничего"""
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)

            return result.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в find_one_or_none {cls.model.__name__}: {e}")
            return None

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by) -> List[model]:
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)

            return result.unique().scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в find_all {cls.model.__name__}: {e}")
            return []

    @classmethod
    async def add(cls, session: AsyncSession, **data) -> model:
        try:
            stmt = (
                insert(cls.model)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()

            return result.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в add {cls.model.__name__}: {e}")
            return None

    @classmethod
    async def update(cls, session: AsyncSession, *filters, **data) -> model:
        try:
            stmt = (
                update(cls.model)
                .where(*filters)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()

            return result.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в update {cls.model.__name__}: {e}")
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, **data):
        try:
            stmt = delete(cls.model).where(**data)
            await session.commit()

            await session.execute(stmt)
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в delete {cls.model.__name__}: {e}")
            return None
