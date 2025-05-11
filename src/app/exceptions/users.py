from fastapi import status
from .base import GearMindAPIException


class UserNotFound(GearMindAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден :("

class UsersNotFound(GearMindAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователи не найдены :("
