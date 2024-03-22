from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI

from src.models import Base
from src.routes.signup import signup
from get_env import get_env

app = FastAPI()
app.include_router(signup)

DB_URL = f'postgresql://{get_env("BD_USERNAME")}:{get_env("BD_PASSWORD")}@{get_env("BD_HOST")}/{get_env("BD_NAME")}'


engine = create_engine(DB_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
