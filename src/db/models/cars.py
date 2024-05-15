from sqlalchemy import Column, Integer, String, ForeignKey

from src.db.db import Base


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(Integer, nullable=False, unique=True)
    model_name = Column(String, nullable=False, unique=True)
    gen_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    user_id = Column(ForeignKey("users.id"))
