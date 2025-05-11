from enum import StrEnum
from sqlalchemy import TypeDecorator, String


class TasksType(StrEnum):
    """Енам типов заданий"""
    DAILY = "Ежедневные"
    LONG = "Обычные"


class TasksTypeTypeDecorator(TypeDecorator):
    """
    Декоратор, с помощью которого мы получаем
    значения TasksType для корректной работы
    """
    impl = String(11)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if isinstance(value, TasksType):
            return value.value
        elif isinstance(value, str) and value in TasksType.__members__:
            return TasksType[value].value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                return TasksType(value)
            except ValueError:
                raise ValueError(f"{value} is not a valid UsersRoles value")
        return value
