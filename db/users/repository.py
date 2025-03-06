from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

<<<<<<< HEAD:db/users/repository.py
from db.db import async_session_maker
from db.repository.base import BaseRepository
from db.users.models import Users
=======
<<<<<<< HEAD:src/db/models/users/repository.py
from db.base_repository import BaseRepository
from db.models.users.models import Users
from db.db_config import async_session_maker
=======
from db.db import async_session_maker
from db.repository.base import BaseRepository
from db.users.models import Users
>>>>>>> dev:db/users/repository.py
>>>>>>> 617c386 (Merge branch 'dev'):src/db/models/users/repository.py

from logger import logger


class UsersRepository(BaseRepository):
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
