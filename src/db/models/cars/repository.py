from db.base_repository import BaseRepository
from db.models.cars.models import Cars


class CarsRepository(BaseRepository):
    model = Cars

    ...