import uuid

from sqlalchemy import UUID, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class Scores(Base):
    """Модель таблицы с оценками запросов от пользователей"""
    __tablename__ = "scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    # Ограничения
    __table_args__ = (
        CheckConstraint(
            sqltext="score >= 1 AND score <= 5",
            name="check_score_range"
        ),
    )

    # Связи
    request: Mapped["Requests"] = relationship(  # type: ignore
        argument="Requests",
        back_populates="score",
        foreign_keys=[request_id],
        cascade="all, delete-orphan",
        lazy="joined",
        single_parent=True
    )
    user: Mapped["Users"] = relationship(  # type: ignore
        argument="Users",
        back_populates="recommendation_score",
        foreign_keys=[user_id],
        cascade="all, delete-orphan",
        lazy="joined",
        single_parent=True
    )
