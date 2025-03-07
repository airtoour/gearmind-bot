import uuid
from typing import List

from sqlalchemy import UUID, BigInteger, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class Users(Base):
    """Модель таблицы Users"""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    tg_username: Mapped[str] = mapped_column(String, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # Связи
    cars: Mapped[List["Cars"]] = relationship(
        argument="Cars",
        back_populates="user",
        lazy="joined"
    )

    # Индексы
    idx_users_tg_user_id_unq = Index("idx_users_tg_user_id", tg_user_id, unique=True)
    idx_users_tg_user_id_tg_user_name_unq = Index(
        "idx_users_tg_user_id_tg_user_name",
        *[tg_user_id, tg_username],
        unique=True
    )
