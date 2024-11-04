from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.db_config import Base


class ProductsTypes(Base):
    __tablename__ = "products_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)

    oil = relationship("Oils", backref="products_type")
    busbar = relationship('Busbars', backref="products_type")
    batteries = relationship("Batteries", backref="products_type")
    disks = relationship("Disks", backref="products_type")
