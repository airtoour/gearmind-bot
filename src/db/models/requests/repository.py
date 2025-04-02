from db.base_repository import BaseRepository
from db.models.requests.models import Requests


class RequestsRepository(BaseRepository):
    model = Requests
