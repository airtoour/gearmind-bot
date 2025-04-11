import uuid

from pydantic import BaseModel
from ..tasks.schemas import TaskInfo


class UsersTasksAllReturnSchema(BaseModel):
    """Схема прогресса по заданию Игрока"""
    task_info: TaskInfo
    current_value: int
    is_completed: bool


class UsersTaskCompleteSchema(BaseModel):
    task_id: uuid.UUID
    telegram_id: int