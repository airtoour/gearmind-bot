from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db.db import Base


class Busbars(Base):
    __tablename__ = 'busbars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    diameter = Column(Integer, nullable=False)
    thorns = Column(Boolean, nullable=False)
