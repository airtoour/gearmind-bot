from sqlalchemy import Column, Integer, String, ForeignKey
from db.db_config import Base


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.tg_user_id"))
    brand_name = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    gen_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
