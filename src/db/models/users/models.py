import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import UUID, BigInteger, String, Index
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base
from .schemas import UsersRoles, UsersRolesTypeDecorator

if TYPE_CHECKING:
    from db.models import Cars, Scores, UsersGameProfiles


class Users(AsyncAttrs, Base):
    """Модель таблицы Users"""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    role: Mapped[UsersRoles] = mapped_column(UsersRolesTypeDecorator(), insert_default=UsersRoles.USER.value)

    # Связи
    car: Mapped["Cars"] = relationship(
        argument="Cars",
        back_populates="user",
        lazy="selectin",
        single_parent=True
    )
    recommendation_score: Mapped[List["Scores"]] = relationship(
        argument="Scores",
        back_populates="user",
        lazy="selectin"
    )
    game_progress: Mapped["UsersGameProfiles"] = relationship(
        argument="UsersGameProfiles",
        back_populates="user",
        lazy="selectin",
        uselist=False
    )

    # Индексы
    idx_users_tg_user_id_unq = Index("idx_users_tg_user_id", tg_user_id, unique=True)

    def __str__(self):
        return f"{self.name} ({self.role.value})"