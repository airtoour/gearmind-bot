from fastapi import status
from .base import GearMindAPIException


class GetProfileBadRequest(GearMindAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка получения Вашего профиля :("

class CreateProfileBadRequest(GearMindAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка создания Вашего профиля :("

class ProfileNotFound(GearMindAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Ваш игровой профиль не найден. Необходимо зарегистрироваться в игре, чтобы начать игру"
