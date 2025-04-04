import uuid
from datetime import datetime
from typing import Union

from sqlalchemy import UUID, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class GameProgressUsers(Base):
    __tablename__ = "game_progress"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4, doc="ID прогресса")

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, doc="ID пользователя"
    )
    car_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("cars.id"), nullable=False, doc="ID автомобиля")

    level: Mapped[int] = mapped_column(Integer, insert_default=1, nullable=False, doc="Уровень игрока")
    experience: Mapped[int] = mapped_column(Integer, insert_default=0, nullable=False, doc="Опыт игрока")
    last_wash_car_time: Mapped[Union[datetime, None]] = mapped_column(DateTime, doc="Дата последнего мытья автомобиля")

    # Связи
    user: Mapped["Users"] = relationship("Users", back_populates="game_progress")  # type: ignore
    car: Mapped["Cars"] = relationship("Cars", back_populates="game_progress")  # type: ignore
