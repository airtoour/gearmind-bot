import uuid
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel


class BasePageReturnSchema(BaseModel):
    """Схема, возвращающая информацию о профиле пользователя"""
    status: Literal["ok", "fail"]
    user_name: str
    level: int
    experience: int


class WashStatusReturnSchema(BaseModel):
    """Схема, возвращающая статус 'загрязнённости' автомобиля"""
    status: Literal["ok", "fail"]
    can_wash: bool
    message: str


class WashCarSchema(BaseModel):
    """Схема, с для запроса на помывку автомобиля"""
    tg_user_id: int


class WashedCarData(BaseModel):
    """Схема полученных данных после помывки"""
    new_level: Optional[int]
    last_wash_car_time: Optional[datetime]
    message: str


class WashedCarReturnSchema(BaseModel):
    """Схема, возвращающая результат помывки автомобиля"""
    status: Literal["ok", "fail"]
    washed: bool
    data: WashedCarData
