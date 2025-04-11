import uuid
from typing import List

from sqlalchemy import UUID, String, Index
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base
from db.models.prompts.schemas import TypesEnum, EnumsDecorator


class Prompts(AsyncAttrs, Base):
    """Справочник промптов для работы с ИИ"""
    __tablename__ = "prompts"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    type: Mapped[TypesEnum] = mapped_column(EnumsDecorator(TypesEnum), index=True)
    text: Mapped[str] = mapped_column(String(2000))

    # Зависимости
    requests: Mapped[List["Requests"]] = relationship(  # type: ignore
        argument="Requests",
        back_populates="prompt",
        foreign_keys="Requests.prompt_id",
        cascade="all, delete-orphan"
    )

    # Индексы
    idx_prompts_type = Index("idx_prompts_type", type)

    def __str__(self):
        return f"Промпт для {self.type}"
