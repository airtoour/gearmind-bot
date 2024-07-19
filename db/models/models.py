from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from db.db import Base, session

from logger import logger


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=False, unique=True)
    tg_username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)

    car = relationship('Cars', backref='user')

    @classmethod
    def get_user_by_tg(cls, tg_user_id: int):
        user = session.query(cls).filter_by(tg_user_id=tg_user_id).first()
        return user if user else None

    @classmethod
    def get_user_id(cls, tg_user_id: int):
        user = session.query(cls).filter_by(tg_user_id=tg_user_id).first()
        return user.id if user else None

    @classmethod
    def create(
        cls,
        tg_user_id: int,
        tg_username: str,
        first_name: str,
        phone_number: str
    ):
        try:
            user = cls(
                tg_user_id = tg_user_id,
                tg_username = tg_username,
                first_name = first_name,
                phone_number = phone_number
            )
            session.add(user)
            session.commit()

            return user
        except Exception as e:
            logger.exception("create_user", e)
            session.rollback()
        finally:
            session.close()


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    gen_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    user_id = Column(ForeignKey("users.id"))

    @classmethod
    def car_register(
        cls,
        brand: str,
        model: str,
        gen: str,
        year: int,
        tg_user_id: str
    ):
        try:
            user = Users.get_user_id(tg_user_id)

            new_car = cls(
                brand_name = brand,
                model_name = model,
                gen_name = gen,
                year = year,
                user_id = user
            )
            session.add(new_car)
            session.commit()

            return new_car if user else None
        except Exception as e:
            logger.exception("create_user", e)
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def get_car(user_id: int):
        car = session.query(Cars).filter_by(user_id=user_id).first()
        return car if car else None


class ProductsTypes(Base):
    __tablename__ = 'products_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)

    oil = relationship('Oils', backref='products_type')
    busbar = relationship('Busbars', backref='products_type')
    batteries = relationship('Batteries', backref='products_type')
    disks = relationship('Disks', backref='products_type')


class Oils(Base):
    __tablename__ = 'oils'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    name = Column(String, nullable=False)
    liter = Column(Float, nullable=False)
    comment = Column(String, nullable=False)
    structure = Column(String, nullable=False)

class Busbars(Base):
    __tablename__ = 'busbars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    diameter = Column(Integer, nullable=False)
    thorns = Column(Boolean, nullable=False)

class Batteries(Base):
    __tablename__ = 'batteries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    voltage = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    toque = Column(Float, nullable=False)

class Disks(Base):
    __tablename__ = 'disks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    diameter = Column(Integer, nullable=False)
    material = Column(String, nullable=False)
