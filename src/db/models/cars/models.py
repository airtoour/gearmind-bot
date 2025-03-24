import uuid

from sqlalchemy import UUID, Integer, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class Cars(Base):
    """Модель таблицы Cars"""
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    brand_name: Mapped[str] = mapped_column(String, nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    gen_name: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    full: Mapped[str] = mapped_column(String, nullable=False)

    # Связи
    user: Mapped["Users"] = relationship(  # type: ignore
        argument="Users",
        back_populates="cars",
        lazy="joined"
    )

    # Индексы
    idx_cars_full = Index("idx_cars_full", full)
