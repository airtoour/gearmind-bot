import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base

if TYPE_CHECKING:
    from db.models import Prompts, Scores


class Requests(AsyncAttrs, Base):
    """Модель таблицы запросов в ИИ"""
    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    date: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    prompt_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("prompts.id"))
    text: Mapped[str] = mapped_column(String(2000))
    response: Mapped[str] = mapped_column(String(4000))
    response_data: Mapped[dict] = mapped_column(JSONB)

    # Связи
    prompt: Mapped["Prompts"] = relationship(
        argument="Prompts",
        back_populates="requests",
        foreign_keys=[prompt_id],
        lazy="selectin",
        single_parent=True
    )
    score: Mapped["Scores"] = relationship(
        argument="Scores",
        back_populates="request",
        lazy="selectin",
    )

    def __str__(self):
        return f"Запрос от {self.date}"