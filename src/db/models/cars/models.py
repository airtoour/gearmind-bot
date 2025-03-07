import uuid

from sqlalchemy import UUID, Integer, String, ForeignKey
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

    # Связи
    user: Mapped["Users"] = relationship(
        argument="Users",
        back_populates="cars",
        lazy="joined"
    )
