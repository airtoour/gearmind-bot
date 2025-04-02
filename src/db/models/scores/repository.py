from db.base_repository import BaseRepository
from db.models import Scores


class ScoresRepository(BaseRepository):
    """Репозиторий для работы с таблицей Оценок"""
    model = Scores
