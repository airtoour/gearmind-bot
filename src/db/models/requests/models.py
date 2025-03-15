import uuid
from datetime import datetime
from sqlalchemy import UUID, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class Requests(Base):
    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4())
    date: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), nullable=False)
    prompt_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("prompts.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    response: Mapped[str] = mapped_column(String, nullable=False)
    response_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Зависимости
    prompt: Mapped["Prompts"] = relationship(
        argument="Prompts",
        back_populates="requests",
        foreign_keys=[prompt_id],
        cascade="all, delete-orphan",
        lazy="joined"
    )
