from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from db.base_repository import BaseRepository
from db.db_config import async_session_maker
from db.models.cars.models import Cars

from logger import logger


class CarsRepository(BaseRepository):
    """Репозиторий для определения методов работы с таблицей"""
    model = Cars

    @classmethod
    async def update_car(cls, user_id: int, field_name, new_value):
        try:
            async with async_session_maker as session:
                query = (
                    update(cls.model)
                    .where(cls.model.user_id == user_id)
                    .values({field_name: new_value})
                )
                await session.execute(query)
                await session.commit()
        except SQLAlchemyError as e:
            message = "Database" if isinstance(e, SQLAlchemyError) else "Unknown"
            extra = {
                "user_id": user_id,
                "field_name": field_name,
                "new_value": new_value
            }
            logger.error(message, extra=extra, exc_info=True)
