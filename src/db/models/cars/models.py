import uuid

from typing import TYPE_CHECKING

from sqlalchemy import UUID, String, ForeignKey, Index
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base

if TYPE_CHECKING:
    from db.models import Users, UsersGameProfiles


class Cars(AsyncAttrs, Base):
    """Таблица с автомобилями пользователей"""
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    brand_name: Mapped[str] = mapped_column(String(128))
    model_name: Mapped[str] = mapped_column(String(128))
    gen_name: Mapped[str] = mapped_column(String(128))
    year: Mapped[int]
    mileage: Mapped[int]
    full: Mapped[str] = mapped_column(String(256))

    # Связи
    user: Mapped["Users"] = relationship(
        argument="Users",
        back_populates="car",
        lazy="selectin"
    )
    game_progress: Mapped["UsersGameProfiles"] = relationship(
        argument="UsersGameProfiles",
        back_populates="car",
        lazy="selectin",
        uselist=False
    )

    # Индексы
    idx_cars_brand = Index("idx_cars_brand", brand_name)
    idx_cars_full = Index("idx_cars_full", full)

    def __str__(self):
        return f"{self.brand_name} {self.model_name} {self.year} года"
