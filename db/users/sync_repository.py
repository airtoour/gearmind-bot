from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db.db import sync_session_maker
from db.repository.base import BaseRepository
from db.users.models import Users

from logger import logger


class SyncUsersRepository(BaseRepository):
    model = Users

    @classmethod
    def get_by_tg(cls, tg_id: int):
        try:
            with sync_session_maker() as session:
                query = select(cls.model).filter_by(tg_user_id=tg_id)
                result = session.execute(query)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e, extra={"tg_id": tg_id}, exc_info=True)
