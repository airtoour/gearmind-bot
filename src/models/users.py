from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from src.db.db import Base, session

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=True, unique=True)
    tg_username = Column(String, nullable=True, unique=True)
    first_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    city_name = Column(String, nullable=True)
    password = Column(String, nullable=True)

    @staticmethod
    def get_current(tg_user_id):
        user = session.query(Users).filter_by(tg_user_id=tg_user_id).first()
        return user if user else None

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_hash(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create(cls,
               first_name: str,
               phone_number: str,
               city_name: str,
               password: str):
        try:
            new_user = cls(
                first_name = first_name,
                phone_number = phone_number,
                city_name = city_name,
            )
            new_user.set_password(password)

            session.add(new_user)
            session.commit()

            return new_user
        except Exception as e:
            print("create user:", e)
            session.rollabck()
        finally:
            session.close()

    @classmethod
    def tg_insert(cls,
                  tg_id: int,
                  tg_username: str,
                  phone: str):
        try:
            user = session.query(Users).filter_by(phone_number=phone).first()

            if user:
                user.tg_user_id = tg_id
                user.tg_username = tg_username

                session.commit()
                return user
            else:
                return None
        except Exception as e:
            print("tg_insert:", e)
            session.rollback()
        finally:
            session.close()
