from db.repository.base import BaseRepository
from db.cars.models import Cars


class CarsRepository(BaseRepository):
    """Репозиторий для определения методов работы с таблицей Cars"""
    model = Cars

