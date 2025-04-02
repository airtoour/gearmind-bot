from enum import StrEnum

from sqlalchemy import TypeDecorator, String


class TypesEnum(StrEnum):
    """Енам, ограничивающий поле Prompts.type"""
    COMPONENTS = "Запчасти"
    LIQUIDS = "Жидкости для авто"
    ACCESSORIES = "Аксессуары"


class EnumsDecorator(TypeDecorator):
    """TypeDecorator для получения значения типа промпта без указания '.value'"""
    impl = String(17)
    cache_ok = True

    def __init__(self, enum_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not issubclass(enum_class, str):
            raise ValueError("Enum должен наследоваться от строки")
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if isinstance(value, self.enum_class):
            return value.value  # type: ignore
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.enum_class(value)
        return value
