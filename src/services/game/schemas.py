from uuid import UUID
from pydantic import BaseModel


class CreateProfileSchema(BaseModel):
    """Схема создания прогресса игры"""
    user_id: UUID
    car_id: UUID


class NewLevelReturnSchema(BaseModel):
    level: int
    experience: int
    upped: bool
