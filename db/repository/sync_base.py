from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError

from db.db import sync_session_maker
from logger import logger


class SyncBaseRepository:
    model = None

    @classmethod
    def find_by_id(cls, model_id: int):
        try:
            with sync_session_maker() as session:
                query = select(cls.model).filter_by(id=model_id)
                result = session.execute(query)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e, extra={"model_id": model_id}, exc_info=True)

    @classmethod
    def find_one_or_none(cls, **filter_by):
        try:
            with sync_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = session.execute(query)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    def find_all(cls, **filter_by):
        try:
            with sync_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = session.execute(query)
                return result.mappings().all()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    def add(cls, **data):
        try:
            with sync_session_maker() as session:
                query = insert(cls.model).values(**data)
                session.execute(query)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    def update(cls, **data):
        try:
            with sync_session_maker() as session:
                query = update(cls.model).where(**data)
                session.execute(query)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)

    @classmethod
    def delete(cls, **data):
        try:
            with sync_session_maker() as session:
                query = delete(cls.model).where(**data)
                session.execute(query)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)
