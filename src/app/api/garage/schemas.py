from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel


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
    last_wash_car_time: Optional[datetime]
    message: str


class WashedCarReturnSchema(BaseModel):
    """Схема, возвращающая результат помывки автомобиля"""
    status: Literal["ok", "fail"]
    washed: bool
    data: WashedCarData
