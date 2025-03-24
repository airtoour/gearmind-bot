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
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Связи
    cars: Mapped[List["Cars"]] = relationship(  # type: ignore
        argument="Cars",
        back_populates="user",
        lazy="joined"
    )

    # Индексы
    idx_users_tg_user_id_unq = Index("idx_users_tg_user_id", tg_user_id, unique=True)

