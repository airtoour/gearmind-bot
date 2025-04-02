import uuid
from datetime import datetime
from sqlalchemy import UUID, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class Requests(Base):
    """Модель таблицы запросов в ИИ"""
    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4, doc="ID запроса")
    date: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), nullable=False, doc="Дата запроса")
    prompt_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("prompts.id"), nullable=False, doc="ID промпта")
    text: Mapped[str] = mapped_column(String, nullable=False, doc="Текст запроса")
    response: Mapped[str] = mapped_column(String, nullable=False, doc="Ответ запроса")
    response_data: Mapped[dict] = mapped_column(JSONB, nullable=False, doc="Данные использования запроса")

    # Связи
    prompt: Mapped["Prompts"] = relationship(  # type: ignore
        argument="Prompts",
        back_populates="requests",
        foreign_keys=[prompt_id],
        lazy="joined",
        single_parent=True
    )
    score: Mapped["Scores"] = relationship(  # type: ignore
        argument="Scores",
        back_populates="request",
        lazy="joined",
    )
