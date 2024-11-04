from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError

from .db_config import async_session_maker
from loguru import logger


class BaseRepository:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session_maker() as session:
                stmt = select(cls.model).filter_by(id=model_id)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e)

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                stmt = select(cls.model).filter_by(**filter_by)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e)

    @classmethod
    async def find_all(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                stmt = select(cls.model).filter_by(**filter_by)
                result = await session.execute(stmt)
                return result.mappings().all()
        except SQLAlchemyError as e:
            logger.error(e)

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session_maker() as session:
                stmt = insert(cls.model).values(**data)
                await session.execute(stmt)
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)

    @classmethod
    async def update(cls, model_id: int, **data):
        try:
            async with async_session_maker() as session:
                stmt = (
                    update(cls.model)
                    .filter_by(id=model_id)
                    .values(**data)
                )
                await session.execute(stmt)
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)

    @classmethod
    async def delete(cls, **data):
        try:
            async with async_session_maker() as session:
                query = delete(cls.model).where(**data)
                await session.execute(query)
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)
