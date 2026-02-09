from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    price = Column(Float, nullable=False)
    is_offer = Column(Boolean, default=False)
