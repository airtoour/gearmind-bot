from fastapi import status
from .base import GearMindAPIException


class CarNotFound(GearMindAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Автомобиль не найден :("
