from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

from db.dao.base import BaseDAO
from db.cars.cars import Cars
from db.db import async_session_maker

from logger import logger


class CarsDAO(BaseDAO):
    model = Cars

    @classmethod
    async def add_car(cls, user_id: int, **data):
        async with async_session_maker as session:
            get_id = select(cls.model).filter_by(user_ud=user_id)
            result_get = session.execute(get_id)

            result: int = result_get.scalar_one_or_none()

            if result:
                ...
