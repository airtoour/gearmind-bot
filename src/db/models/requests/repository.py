from db.base_repository import BaseRepository
from db.models.requests.models import Requests


class RequestsRepository(BaseRepository):
    """Репозиторий для работы с таблицей запросов в ИИ"""
    model = Requests
