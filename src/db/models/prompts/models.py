import uuid
from typing import List

from sqlalchemy import UUID, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base
from db.models.prompts.schemas import TypesEnum, EnumsDecorator


class Prompts(Base):
    """Справочник промптов для работы с ИИ"""
    __tablename__ = "prompts"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4, doc="ID промпта")
    type: Mapped[TypesEnum] = mapped_column(EnumsDecorator(TypesEnum), nullable=False, index=True, doc="Тип промпта")
    text: Mapped[str] = mapped_column(String, nullable=False, index=True, doc="Текст промпта")

    # Зависимости
    requests: Mapped[List["Requests"]] = relationship(  # type: ignore
        argument="Requests",
        back_populates="prompt",
        foreign_keys="Requests.prompt_id",
        cascade="all, delete-orphan"
    )

    # Индексы
    idx_prompts_type_text = Index("idx_prompts_type_text", type, text)
