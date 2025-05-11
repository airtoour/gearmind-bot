import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, CheckConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base

if TYPE_CHECKING:
    from db.models import Requests, Users


class Scores(AsyncAttrs, Base):
    """Модель таблицы с оценками запросов от пользователей"""
    __tablename__ = "scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("requests.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    score: Mapped[int]

    # Ограничения
    __table_args__ = (
        CheckConstraint(
            sqltext="score >= 1 AND score <= 5",
            name="check_score_range"
        ),
    )

    # Связи
    request: Mapped["Requests"] = relationship(
        argument="Requests",
        back_populates="score",
        foreign_keys=[request_id],
        cascade="all, delete-orphan",
        lazy="selectin",
        single_parent=True
    )
    user: Mapped["Users"] = relationship(
        argument="Users",
        back_populates="recommendation_score",
        foreign_keys=[user_id],
        cascade="all, delete-orphan",
        lazy="selectin",
        single_parent=True
    )
