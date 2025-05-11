from db.base_repository import BaseRepository
from db.models.prompts.models import Prompts


class PromptsRepository(BaseRepository):
    """Репозиторий для работы с таблицей Промптов"""
    model = Prompts
