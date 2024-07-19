from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from db.db import Base


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    gen_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    user_id = Column(ForeignKey("users.id"))