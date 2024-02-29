from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

DB_URL = f'postgresql://postgres:postgres@localhost/diplom_db'

engine = create_engine(DB_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
