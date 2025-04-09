from pydantic import BaseModel, ConfigDict
from db.models.tasks.schemas import TasksType


class TaskInfo(BaseModel):
    """Схема основной информации о Задании"""
    title: str
    description: str
    type: TasksType
    target_value: int
    reward_xp: int
    current_value: int

    model_config = ConfigDict(from_attributes=True)