from fastapi import status
from .base import GearMindAPIException


class UsersTasksNotFound(GearMindAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "У Вас закончились задания! Ожидайте завтрашнего дня!"
