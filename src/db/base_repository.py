from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError

from db.db_config import async_session_maker

from loguru import logger


class BaseRepository:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session_maker() as session:
                stmt = select(cls.model).filter_by(id=model_id)
                result = await session.execute(stmt)
                return result.unique().scalar_one_or_none()
        except SQLAlchemyError as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            raise

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                stmt = select(cls.model).filter_by(**filter_by)
                result = await session.execute(stmt)
                return result.unique().scalar_one_or_none()
        except SQLAlchemyError as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            raise

    @classmethod
    async def find_all(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                stmt = select(cls.model).filter_by(**filter_by)
                result = await session.execute(stmt)
                return result.unique().mappings().all()
        except SQLAlchemyError as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            raise

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session_maker() as session:
                stmt = insert(cls.model).values(**data)
                await session.execute(stmt)
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            raise

    @classmethod
    async def update(cls, *filters, **data):
        try:
            async with async_session_maker() as session:
                stmt = select(cls.model).where(*filters)
                result = await session.execute(stmt)
                row = result.unique().scalar_one_or_none()

                if row:
                    for key, value in data.items():
                        setattr(row, key, value)

                    session.add(row)
                    await session.commit()
                    await session.refresh(row)

                    logger.info(f"Объект обновлён: {row}")
                    return row
                else:
                    logger.warning("Не найден объект для обновления")
                    return None
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            raise

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
