import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateProgressSchema(BaseModel):
    """Схема создания прогресса игры"""
    user_id: uuid.UUID
    car_id: uuid.UUID


class UserProfileResponse(BaseModel):
    """Схема возврата данных профиля игрока"""
    user_name: str
    level: int
    experience: int
    last_wash: datetime

    model_config = ConfigDict(from_attributes=True)
