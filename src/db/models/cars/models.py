import uuid

from sqlalchemy import UUID, Integer, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


class Cars(Base):
    """Таблица с автомобилями пользователей"""
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, insert_default=uuid.uuid4, doc="ID автомобиля")
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, doc="ID владельца"
    )
    brand_name: Mapped[str] = mapped_column(String, nullable=False, doc="Марка")
    model_name: Mapped[str] = mapped_column(String, nullable=False, doc="Модель")
    gen_name: Mapped[str] = mapped_column(String, nullable=False, doc="Модификация")
    year: Mapped[int] = mapped_column(Integer, nullable=False, doc="Год выпуска")
    mileage: Mapped[int] = mapped_column(Integer, nullable=False, doc="Пробег")
    full: Mapped[str] = mapped_column(String, nullable=False, doc="Полное название")

    # Связи
    user: Mapped["Users"] = relationship(  # type: ignore
        argument="Users",
        back_populates="car",
        lazy="joined"
    )
    game_progress: Mapped["GameProgressUsers"] = relationship(  # type: ignore
        argument="GameProgressUsers",
        back_populates="car",
        lazy="joined",
        uselist=False
    )

    # Индексы
    idx_cars_full = Index("idx_cars_full", full)

    def __str__(self):
        return f"{self.brand_name} {self.model_name} {self.year} года"
