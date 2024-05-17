from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

DATABASE_URL = (f'postgresql://{settings.DB_USER}:{settings.DB_PASS}'
                f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine, expire_on_commit=False)

session = Session()

class Base(DeclarativeBase):
    pass