from sqlalchemy import Column, Integer, String, ForeignKey

from src.db.db import Base, session
from src.models.users import Users

class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(Integer, nullable=False, unique=True)
    model_name = Column(String, nullable=False, unique=True)
    gen_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    user_id = Column(ForeignKey("users.id"))

    @staticmethod
    def car_register(brand: str, model: str, gen: str, year: int, tg_user_id: str):
        user = Users.get_current(tg_user_id)

        try:
            user_car = Cars(
                brand_name=brand,
                model_name=model,
                gen_name=gen,
                year=year,
                user_id=user.user_id
            )
            session.add(user_car)
            session.commit()
            print('Машина успешно зарегистрирована в базе данных!')
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()