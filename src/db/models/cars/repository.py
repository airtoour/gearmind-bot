<<<<<<< HEAD:src/db/models/cars/repository.py
from db.base_repository import BaseRepository
from db.models.cars.models import Cars
=======
from sqlalchemy import select, insert, update
from sqlalchemy.exc import SQLAlchemyError

from db.repository.base import BaseRepository
from db.cars.models import Cars
from db.db import async_session_maker

from logger import logger
>>>>>>> dev:db/cars/repository.py


class CarsRepository(BaseRepository):
    model = Cars

<<<<<<< HEAD:src/db/models/cars/repository.py
    ...
=======
    @classmethod
    async def add_car(cls, user_id: int, **data):
        try:
            async with async_session_maker as session:
                get_id = select(cls.model).filter_by(user_id=user_id)
                result_get = session.execute(get_id)

                result: int = result_get.scalar_one_or_none()

                if result:
                    query = insert(cls.model).values(**data)
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
                "user_id": user_id,
                "field_name": field_name,
                "new_value": new_value
            }
            logger.error(message, extra=extra, exc_info=True)
>>>>>>> dev:db/cars/repository.py
