from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.api.tasks.schemas import TaskInfo


class AllUsersTaskSchema(BaseModel):
    """Схема данных Заданий игрока"""
    id: UUID
    user_id: UUID
    task: TaskInfo
    current_value: int
    is_completed: bool
    assigned_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UsersTasksAllReturnSchema(BaseModel):
    """Схема для получения всех заданий"""
    tasks: List[AllUsersTaskSchema]
