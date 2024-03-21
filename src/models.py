from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from aiogram.types import Message

from src.db.config import session
from src.exceptions import server_exceptions

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=True)
    tg_username = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False)
    user_password = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    city_id = Column(Integer, nullable=True)
    car_id = Column(Integer, nullable=True)
    card_id = Column(Integer, nullable=True)
    is_vip = Column(String, default='N', nullable=True)

    cities = relationship("Cities", back_populates="user")

    @classmethod
    async def get_current(cls, message: Message | None):
        user = session.query(Users).filter_by(tg_user_id=message.from_user.id)
        return user

    @classmethod
    async def create(cls,
                     tg_user_id: str | None,
                     tg_username: str | None,
                     first_name: str,
                     last_name: str,
                     phone_number: str | None,
                     city_id: int | None,
                     car_id: int | None,
                     card_id: int | None,
                     is_vip: str | None):
        try:
            if not Users.get_current() is None:
                error_message = 'Такой пользователь уже существует!'
                session.rollback()
                return server_exceptions(status_code=204, detail=error_message)
            else:
                new_user = Users(tg_user_id=tg_user_id,
                                 tg_username=tg_username,
                                 first_name=first_name,
                                 last_name=last_name,
                                 phone_number=phone_number,
                                 city_id=city_id,
                                 car_id=car_id,
                                 card_id=card_id,
                                 is_vip=is_vip)
                session.add(new_user)
                session.commit()
                return new_user
        except Exception as e:
            session.rollback()
            return server_exceptions(status_code=400, detail=e)
        finally:
            session.close()

    # ТУТ НУЖНО ПАРОЛЬ СОЗДАТЬ ПОЛУЧАЕТСЯ НАХУЙ БЛЯТЬ КАК Я ЗАЕБАЛСЯ
    def create_password(self):
        pass


class Cities(Base):
    __tablename__ = 'cities'

    city_id = Column(Integer, ForeignKey('users.city_id'), primary_key=True)
    city_name = Column(String, nullable=False)

    user = relationship("Users", back_populates="cities")


class ProdGroup(Base):
    __tablename__ = 'prod_groups'

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False)


class Cars(Base):
    __tablename__ = 'cars'

    car_id = Column(Integer, ForeignKey('users.car_id'), primary_key=True)
    prod_group_id = Column(Integer, ForeignKey('prod_groups.group_id'), nullable=False)
    car_name = Column(String, nullable=False)
    car_year = Column(Integer, nullable=False)

    user = relationship("Users", back_populates="cars")
    prod_group = relationship("ProdGroup", back_populates="cars")
