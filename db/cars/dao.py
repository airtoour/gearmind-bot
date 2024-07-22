from sqlalchemy import select, insert, update
from sqlalchemy.exc import SQLAlchemyError

from db.dao.base import BaseDAO
from db.cars.cars import Cars
from db.db import async_session_maker

from logger import logger


class CarsDAO(BaseDAO):
    model = Cars

    @classmethod
    async def add_car(cls, user_id: int, **data):
        try:
            async with async_session_maker as session:
                get_id = select(cls.model).filter_by(user_ud=user_id)
                result_get = session.execute(get_id)

                result: int = result_get.scalar_one_or_none()

                if result:
                    query = insert(cls.model).values(
                        **data
                    )
                    await session.execute(query)
                    await session.commit()
        except SQLAlchemyError as e:
            if isinstance(e, SQLAlchemyError):
                message = 'Database'
            else:
                message = 'Unknown'
            extra = {"user_id": user_id}
            logger.error(message, extra=extra, exc_info=True)

    @classmethod
    async def update_car(cls, user_id: int, field_name, new_value):
        try:
            async with async_session_maker as session:
                query = update(cls.model).where(
                    cls.model.user_id == user_id
                ).values(
                    {field_name: new_value}
                )
                await session.execute(query)
                await session.commit()
        except SQLAlchemyError as e:
            if isinstance(e, SQLAlchemyError):
                message = 'Database'
            else:
                message = 'Unknown'
            extra = {
                "car_id": car_id,
                "field_name": field_name,
                "new_value": new_value
            }
            logger.error(message, extra=extra, exc_info=True)
