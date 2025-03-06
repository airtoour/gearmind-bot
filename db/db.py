from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
DATABASE_PARAMS = {}

async_engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

sync_database_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
sync_engine = create_engine(sync_database_url, **DATABASE_PARAMS)
sync_session_maker = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
