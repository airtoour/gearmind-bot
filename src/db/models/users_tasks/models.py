import uuid
from datetime import datetime
from typing import Union

from sqlalchemy import UUID, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class UsersTasks(AsyncAttrs, Base):
    """Модель таблицы прогресса по Заданиям"""
    __tablename__ = "users_tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))
    task_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("tasks.id"))
    current_value: Mapped[int] = mapped_column(insert_default=0)
    is_completed: Mapped[bool] = mapped_column(insert_default=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, insert_default=datetime.now)
    completed_at: Mapped[Union[datetime, None]]

    # Отношения
    user: Mapped["Users"] = relationship(argument="Users", back_populates="user_tasks", lazy="joined")  # noqa
    task: Mapped["Tasks"] = relationship(argument="Tasks", back_populates="user_tasks", lazy="joined")  # noqa
