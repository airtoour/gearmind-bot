from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.settings import settings

DB_URL = f'postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}'

engine = create_engine(DB_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
