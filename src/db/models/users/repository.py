from typing import Union

from fastapi_cache.decorator import cache

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from services.redis_cache.service import cache_service

from db.base_repository import BaseRepository
from db.models import Users

from logger import logger


class UsersRepository(BaseRepository):
    """Репозиторий для определения методов работы с таблицей Users"""
    model = Users

    @classmethod
    @cache(expire=3600, key_builder=cache_service.model_key_builder)
    async def find_one_or_none(cls, session: AsyncSession, **filter_by) -> Union[model, None]:
        try:
            stmt = (
                select(cls.model)
                .options(selectinload(cls.model.car))
                .filter_by(**filter_by)
            )
            result = await session.execute(stmt)
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка в find_one_or_none {cls.model.__name__}: {e}")
            return None


if __name__ == "__main__":
    import asyncio

    from redis import asyncio as aioredis
    from db.db_config import async_session_maker
    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.redis import RedisBackend


    async def main():
        redis = aioredis.from_url("redis://127.0.0.1:6379")
        FastAPICache.init(RedisBackend(redis), prefix="db-cache")

        async with async_session_maker() as session:
            users = await UsersRepository.find_one_or_none(session, tg_user_id=1068989629)

        print(users)

        await redis.connection_pool.disconnect()

    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"RuntimeError caught: {e}")
