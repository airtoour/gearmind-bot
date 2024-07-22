from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.db import Base


class Batteries(Base):
    __tablename__ = 'batteries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    voltage = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    toque = Column(Float, nullable=False)
