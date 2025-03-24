from typing import List

from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger


class BaseRepository:
    model = None

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by) -> model:
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)

            return result.unique().scalar_one_or_none()
        except SQLAlchemyError as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            return None

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by) -> List[model]:
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)

            return result.unique().scalars().all()
        except SQLAlchemyError as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            return []

    @classmethod
    async def add(cls, session: AsyncSession, **data) -> model:
        try:
            async with session.begin():
                stmt = (
                    insert(cls.model)
                    .values(**data)
                    .returning(cls.model)
                )
                result = await session.execute(stmt)
                return result.unique().scalar_one_or_none()
        except SQLAlchemyError as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            return None

    @classmethod
    async def update(cls, session: AsyncSession, *filters, **data) -> model:
        try:
            async with session.begin():
                stmt = (
                    update(cls.model)
                    .where(*filters)
                    .values(**data)
                    .returning(cls.model)
                )
                result = await session.execute(stmt)

            return result.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в update {cls.model.__name__}: {e}")
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, **data):
        try:
            async with session.begin():
                query = delete(cls.model).where(**data)
                await session.execute(query)
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в delete {cls.model.__name__}: {e}")
            return None
