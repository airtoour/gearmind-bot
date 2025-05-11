from enum import StrEnum
from sqlalchemy import TypeDecorator, String


class UsersRoles(StrEnum):
    """Енам для ролей пользователей"""
    ADMIN = "Администратор"
    USER = "Пользователь"
    BOT = "Бот"


class UsersRolesTypeDecorator(TypeDecorator):
    """
    Декоратор, с помощью которого мы получаем
    значения UsersRoles для корректной работы
    """
    impl = String(13)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if isinstance(value, UsersRoles):
            return value.value
        elif isinstance(value, str) and value in UsersRoles.__members__:
            return UsersRoles[value].value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                return UsersRoles(value)
            except ValueError:
                raise ValueError(f"{value} is not a valid UsersRoles value")
        return value
