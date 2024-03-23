from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from aiogram.types import Message

from werkzeug.security import generate_password_hash, check_password_hash

from pydantic import BaseModel
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
    tg_user_id = Column(Integer, nullable=False, unique=True)
    tg_username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    city_id = Column(Integer, nullable=True)
    car_id = Column(Integer, nullable=True)
    card_id = Column(Integer, nullable=True)
    is_vip = Column(String, default='N', nullable=True)

    cities = relationship("Cities", back_populates="user")
    cars = relationship("Cars", back_populates="user")

    @classmethod
    async def get_current(cls, session, message: Message | None):
        user = session.query(Users).filter(Users.tg_user_id == message.from_user.id).first()
        return user

    def set_password(self, user_password):
        self.user_password = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.user_password, user_password)

    @classmethod
    async def create(cls,
                     session,
                     first_name: str,
                     user_email: str,
                     user_password: str,
                     phone_number: str,
                     city_id: int | None,
                     car_id: int | None,
                     card_id: int | None,
                     is_vip: str | None,

                     message: Message):
        try:
            if Users.get_current(session) is not None:
                error_message = 'Такой пользователь уже существует!'
                return server_exceptions(status_code=204, detail=error_message)
            else:
                new_user = Users(tg_user_id=message.from_user.id,
                                 tg_username=message.from_user.username,
                                 first_name=first_name,
                                 phone_number=phone_number,
                                 user_email=user_email,
                                 user_password=user_password,
                                 city_id=city_id,
                                 car_id=car_id,
                                 card_id=card_id,
                                 is_vip=is_vip)
                session.add(new_user)
                session.commit()
                return new_user
        except Exception as e:
            session.rollback()
            return server_exceptions(status_code=400, detail=str(e))
        finally:
            session.close()

    class SignUp(BaseModel):
        tg_user_id:    int | None
        tg_user_name:  str | None
        first_name:    str
        phone_number:  str
        user_email:    str
        user_password: str
        city_id:       int | None
        car_id:        int | None
        card_id:       int | None
        is_vip:        str | None

    # ТУТ НУЖНО ПАРОЛЬ СОЗДАТЬ ПОЛУЧАЕТСЯ НАХУЙ БЛЯТЬ КАК Я ЗАЕБАЛСЯ
    def create_password(self):
        pass
