import uuid
from datetime import datetime
from typing import List, Union

from sqlalchemy import UUID, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class UsersGameProfiles(AsyncAttrs, Base):
    __tablename__ = "users_game_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    car_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("cars.id"))

    level: Mapped[int] = mapped_column(insert_default=1)
    experience: Mapped[int] = mapped_column(insert_default=0)
    level_threshold: Mapped[int] = mapped_column(insert_default=100)

    last_wash_car_time: Mapped[Union[datetime, None]] = mapped_column(DateTime)

    # Связи
    user: Mapped["Users"] = relationship("Users", back_populates="game_progress")  # type: ignore
    car: Mapped["Cars"] = relationship("Cars", back_populates="game_progress")  # type: ignore
    user_tasks: Mapped[List["UsersTasks"]] = relationship(  # noqa
        argument="UsersTasks",
        back_populates="user",
        lazy="selectin"
    )

    def __str__(self):
        return f"Профиль. Уровень: {self.level}"
