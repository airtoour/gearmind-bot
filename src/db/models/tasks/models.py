import uuid
from typing import List, TYPE_CHECKING

from db.db_config import Base

from sqlalchemy import UUID, Index
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .schemas import TasksType, TasksTypeTypeDecorator

if TYPE_CHECKING:
    from db.models import UsersTasks


class Tasks(AsyncAttrs, Base):
    """Справочник заданий игры GearGame"""
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    title: Mapped[str]
    description: Mapped[str]
    type: Mapped[TasksType] = mapped_column(TasksTypeTypeDecorator())
    target_value: Mapped[int]
    reward_xp: Mapped[int]
    is_active: Mapped[bool] = mapped_column(insert_default=True, index=True)

    # Отношения
    user_tasks: Mapped[List["UsersTasks"]] = relationship(
        argument="UsersTasks",
        back_populates="task",
        lazy="selectin"
    )

    # Индексы
    ix_tasks_is_active = Index("ix_tasks_is_active", is_active)