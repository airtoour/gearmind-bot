from db.base_repository import BaseRepository
from db.models.prompts.models import Prompts


class PromptsRepository(BaseRepository):
    model = Prompts
