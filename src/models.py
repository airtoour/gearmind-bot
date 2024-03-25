from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from aiogram.types import Message

from werkzeug.security import generate_password_hash, check_password_hash
from src.exceptions import server_exceptions


Base = declarative_base()

class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    city_id = Column(Integer, ForeignKey('users.city_id'))
    city_name = Column(String, nullable=False)

    user = relationship("Users", back_populates="cities")


class ProdGroup(Base):
    __tablename__ = 'prod_groups'

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False)

    cars = relationship("Cars", back_populates="prod_group")

class Cars(Base):
    __tablename__ = 'cars'

    car_id = Column(Integer, ForeignKey('users.car_id'), primary_key=True)
    prod_group_id = Column(Integer, ForeignKey('prod_groups.group_id'), nullable=False)
    car_name = Column(String, nullable=False)
    car_year = Column(Integer, nullable=False)

    user = relationship("Users", back_populates="cars")
    prod_group = relationship("ProdGroup", back_populates="cars")


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    tg_user_id = Column(Integer,         nullable=True,             unique=True)
    tg_username = Column(String,         nullable=True,             unique=True)
    first_name = Column(String,          nullable=False)
    phone_number = Column(String,        nullable=False,            unique=True)
    user_email = Column(String,          nullable=False,            unique=True)
    user_password = Column(String,       nullable=False)
    city_id = Column(Integer,            nullable=True)
    car_id = Column(Integer,             nullable=True)
    card_id = Column(Integer,            nullable=True)
    is_vip = Column(String, default='N', nullable=True)

    cities = relationship("Cities", back_populates="user")
    cars = relationship("Cars", back_populates="user")

    @classmethod
    async def get_current(cls, user_email):
        from src.db.config import session

        user = session.query(Users).filter(Users.user_email == user_email).first()
        return user

    def set_password(self, user_password):
        self.user_password = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.user_password, user_password)

    @classmethod
    async def create(cls,
                     first_name: str,
                     user_email: str,
                     user_password: str,
                     phone_number: int):
        from src.db.config import session

        try:
            exist_user = await cls.get_current(user_email)

            if exist_user is not None:
                error_message = 'Такой пользователь уже существует!'
                return server_exceptions(status_code=204, detail=error_message)
            else:
                new_user = cls(tg_user_id=None,
                               tg_username=None,
                               first_name=first_name,
                               phone_number=phone_number,
                               user_email=user_email,
                               user_password=user_password,
                               city_id=None,
                               car_id=None,
                               card_id=None,
                               is_vip=None)
                new_user.set_password(user_password)
                session.add(new_user)
                session.flush()
                session.commit()
                return new_user
        except Exception as e:
            session.rollback()
            print(e)
            return server_exceptions(status_code=400, detail=str(e))
        finally:
            session.close()
