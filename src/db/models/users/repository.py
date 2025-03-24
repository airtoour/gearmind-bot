from db.base_repository import BaseRepository
from db.models.users.models import Users


class UsersRepository(BaseRepository):
    """Репозиторий для определения методов работы с таблицей Users"""
    model = Users
