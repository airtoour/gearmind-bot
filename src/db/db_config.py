from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

from config import settings


# Определяем асинхронный движок
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=15,
    max_overflow=10,
    pool_recycle=1800,
    pool_pre_ping=True
)

# Создаём генератор асинхронных сессий
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессий для БД"""
    async with async_session_maker() as session:
        yield session


# Определяем класс Base, для создания таблиц
class Base(DeclarativeBase):
    pass
