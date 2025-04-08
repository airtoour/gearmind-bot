from fastapi_cache.decorator import cache

from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from services.redis_cache.service import cache_service

from logger import logger


class BaseRepository:
    """Базовый репозиторий с универсальными методами"""
    model = None

    @classmethod
    @cache(expire=3600, key_builder=cache_service.model_key_builder)
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        """Метод поиска записи, возвращает её или ничего"""
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)

            return result.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в find_one_or_none {cls.model.__name__}: {e}")
            return None

    @classmethod
    @cache(expire=3600, key_builder=cache_service.model_key_builder)
    async def find_all(cls, session: AsyncSession, **filter_by):
        """Метод поиска всех записей из таблицы"""
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)

            return result.unique().scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в find_all {cls.model.__name__}: {e}")
            return []

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        """Метод добавления объекта в таблицу"""
        try:
            select_result = await cls.find_one_or_none(**data)

            if select_result:
                return select_result

            insert_query = (
                insert(cls.model)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(insert_query)
            await session.commit()

            added_instance = result.unique().scalar_one_or_none()
            await cache_service.invalidate_cache(cls.model)

            return added_instance
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в add {cls.model.__name__}: {e}")
            return None

    @classmethod
    async def update(cls, session: AsyncSession, *filters, **data):
        """Метод обновления объекта в таблице"""
        try:
            stmt = (
                update(cls.model)
                .where(*filters)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()

            updated_instance = result.unique().scalar_one_or_none()

            if updated_instance:
                await cache_service.invalidate_cache(cls.model)

            return updated_instance
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в update {cls.model.__name__}: {e}")
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, **data):
        """Метод удаления объекта в таблице"""
        try:
            stmt = delete(cls.model).where(**data)
            await session.commit()

            await session.execute(stmt)
            await session.commit()

            await cache_service.invalidate_cache(cls.model)
        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            logger.error(f"Ошибка в delete {cls.model.__name__}: {e}")
            return None
