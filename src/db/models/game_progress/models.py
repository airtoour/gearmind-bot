import uuid
from datetime import datetime

from sqlalchemy import UUID, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class GameProgressUsers(Base):
    __tablename__ = "game_progress"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4, doc="ID прогресса")
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, doc="ID пользователя"
    )

    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False, doc="Уровень игрока")
    experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False, doc="Опыт игрока")
    first_login_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False, doc="Время первого входа")

    # Связи
    user = relationship("Users", back_populates="game_progress")
