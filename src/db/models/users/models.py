import uuid
from typing import List

from sqlalchemy import UUID, BigInteger, String, Index
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base
from .schemas import UsersRoles, UsersRolesTypeDecorator


class Users(AsyncAttrs, Base):
    """Модель таблицы Users"""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4, doc="ID пользователя")
    tg_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, index=True, doc="TelegramID")
    name: Mapped[str] = mapped_column(String, nullable=False, doc="Имя пользователя")
    role: Mapped[UsersRoles] = mapped_column(
        UsersRolesTypeDecorator(), nullable=False, insert_default=UsersRoles.USER.value, doc="Роль пользователя"
    )

    # Связи
    car: Mapped["Cars"] = relationship(  # type: ignore
        argument="Cars",
        back_populates="user",
        lazy="joined",
        single_parent=True
    )
    recommendation_score: Mapped[List["Scores"]] = relationship(  # type: ignore
        argument="Scores",
        back_populates="user",
        lazy="joined"
    )
    game_progress: Mapped["GameProgressUsers"] = relationship(  # type: ignore
        argument="GameProgressUsers",
        back_populates="user",
        lazy="joined",
        uselist=False
    )

    # Индексы
    idx_users_tg_user_id_unq = Index("idx_users_tg_user_id", tg_user_id, unique=True)

    def __str__(self):
        return f"{self.name} ({self.role.value})"