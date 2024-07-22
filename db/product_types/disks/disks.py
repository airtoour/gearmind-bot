from sqlalchemy import Column, Integer, String, ForeignKey
from db.db import Base


class Disks(Base):
    __tablename__ = 'disks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    diameter = Column(Integer, nullable=False)
    material = Column(String, nullable=False)
