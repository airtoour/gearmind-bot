from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db.dao.base import BaseDAO
from db.users.users import Users
from db.db import async_session_maker

from logger import logger


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_by_tg(cls, tg_id: int):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(tg_user_id=tg_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e, extra={"tg_id": tg_id}, exc_info=True)
