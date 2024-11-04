from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.db_config import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=False, unique=True)
    tg_username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)

    car = relationship("Cars", backref="user")
