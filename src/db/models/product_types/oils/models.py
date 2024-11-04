from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.db_config import Base


class Oils(Base):
    __tablename__ = 'oils'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(ForeignKey('products_types.id'))
    maker = Column(String, nullable=False)
    name = Column(String, nullable=False)
    liter = Column(Float, nullable=False)
    comment = Column(String, nullable=False)
    structure = Column(String, nullable=False)
