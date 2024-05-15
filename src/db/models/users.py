from sqlalchemy import Column, Integer, String
from src.db.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=True, unique=True)
    tg_username = Column(String, nullable=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    city_name = Column(String, nullable=True)
    password = Column(String, nullable=True)

