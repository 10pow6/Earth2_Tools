from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, unique=True, index=True)
    update_time = Column(DateTime)
    trade_average = Column(Float)
    final = Column(Float)
    total_tiles_sold = Column(Integer)
