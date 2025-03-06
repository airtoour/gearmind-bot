from sqlalchemy import select, insert, update
from sqlalchemy.exc import SQLAlchemyError

from db.repository.sync_base import SyncBaseRepository
from db.cars.models import Cars
from db.users.models import Users
from db.db import sync_session_maker

from logger import logger


class SyncCarsRepository(SyncBaseRepository):
    model = Cars

    @classmethod
    def add_car(
        cls,
        user_id: int,
        brand_name: str,
        model_name: str,
        gen_name: str,
        year: int,
    ):
        try:
            with sync_session_maker() as session:
                get_id = select(Users).filter_by(tg_user_id=user_id)
                result_get = session.execute(get_id)

                result: int = result_get.scalar_one_or_none()

                if result:
                    query = insert(cls.model).values(
                        user_id=user_id, brand_name=brand_name, model_name=model_name, gen_name=gen_name, year=year
                    )
                    session.execute(query)
                    session.commit()
        except SQLAlchemyError as e:
            if isinstance(e, SQLAlchemyError):
                message = 'Database'
            else:
                message = 'Unknown'
            extra = {
                "user_id": user_id,
                "brand_name": brand_name,
                "model_name": model_name,
                "gen_name": gen_name,
                "year": year,
            }
            logger.error(message, extra=extra, exc_info=True)

    @classmethod
    def update_car(cls, user_id: int, field_name, new_value):
        try:
            with sync_session_maker() as session:
                query = update(cls.model).where(
                    cls.model.user_id == user_id
                ).values(
                    {field_name: new_value}
                )
                session.execute(query)
                session.commit()
        except SQLAlchemyError as e:
            if isinstance(e, SQLAlchemyError):
                message = 'Database'
            else:
                message = 'Unknown'
            extra = {
                "user_id": user_id,
                "field_name": field_name,
                "new_value": new_value,
            }
            logger.error(message, extra=extra, exc_info=True)
