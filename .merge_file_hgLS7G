from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError

from db.db import async_session_maker
from logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(id=model_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e, extra={"model_id": model_id}, exc_info=True)

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    async def find_all(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.mappings().all()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data)
                await session.execute(query)
                await session.commit()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    async def update(cls, **data):
        try:
            async with async_session_maker() as session:
                query = update(cls.model).where(**data)
                await session.execute(query)
                await session.commit()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    async def delete(cls, **data):
        try:
            async with async_session_maker() as session:
                query = delete(cls.model).where(**data)
                await session.execute(query)
                await session.commit()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)
