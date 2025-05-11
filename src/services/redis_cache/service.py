from typing import Callable, Optional

from fastapi import Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from config import settings
from logger import logger


class GearMindCacheService:
    """Сервис кэширования GearMind"""
    def __init__(self, url: str):
        self.url = url

        self.client = None
        self.initialized = False

    async def connect(self):
        """Метод подключения к Redis-клиенту"""

        self.client = await aioredis.from_url(
            self.url,
            encoding="utf-8",
            decode_responses=True
        )

        FastAPICache.init(
            backend=RedisBackend(self.client),
            prefix="fastapi-cache"
        )

        await self.client.ping()
        self.initialized = True

    async def disconnect(self):
        """Метод закрытия подключения от Redis-клиента"""
        if self.client:
            await self.client.close()

            self.client = None
            self.initialized = False

    def model_key_builder(
        self,
        func: Callable,
        namespace: Optional[str] = "",
        request: Optional[Request] = None,
        response: Optional[Response] = None,
        *args,
        **kwargs,
    ) -> str:
        """Билдер формирования ключа для кэширования запросов"""

        cls = args[0] if args else None

        if cls and hasattr(cls, "model"):
            model_name = cls.model.__name__.lower()
            method_name = func.__name__
            filter_args = ":".join([f"{k}={v}" for k, v in kwargs.items()])
            key = f"{model_name}:{method_name}:{filter_args}"

            return key

        return self._get_key_builder()(
            func,
            namespace=namespace,  # type: ignore
            request=request,
            response=response,
            *args,
            **kwargs
        )

    async def invalidate_cache(self, model):
        if not self.initialized:
            raise RuntimeError("Redis client is not initialized")

        cursor = 0

        try:
            while True:
                cursor, keys = await self.client.scan(
                    cursor=cursor,
                    match=f"{model.__name__.lower().replace(' ', '_')}:*",
                    count=500
                )

                if keys:
                    await self.client.delete(*keys)

                if cursor == 0:
                    break
        except aioredis.RedisError as e:
            logger.error(f"Cache invalidation failed: {str(e)}")
            raise

    @staticmethod
    def _get_backend():
        return FastAPICache.get_backend()

    @staticmethod
    def _get_key_builder():
        return FastAPICache.get_key_builder()


# Определение экземпляра сервиса
cache_service = GearMindCacheService(settings.REDIS_URL)
