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

class CountryHistorical(Base):
    __tablename__ = "countries_historical"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, index=True)
    update_time = Column(DateTime, index=True)
    trade_average = Column(Float)
    final = Column(Float)
    total_tiles_sold = Column(Integer)


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    landfield_id = Column(String, unique=True, index=True)
    for_sale = Column(Boolean)
    description = Column(String)
    location = Column(String)
    center = Column(String)
    price = Column(Float)
    country = Column(String)
    tile_count = Column(Integer)
    current_value = Column(Float)
    trading_value = Column(Float)
    tile_class = Column(Integer)
    tile_class_revenue = Column(Float)
    update_time = Column(DateTime, index=True)
    profile_id = Column(String)

class PropertyHistorical(Base):
    __tablename__ = "properties_historical"

    id = Column(Integer, primary_key=True, index=True)
    landfield_id = Column(String, index=True)
    for_sale = Column(Boolean)
    description = Column(String)
    location = Column(String)
    center = Column(String)
    price = Column(Float)
    country = Column(String)
    tile_count = Column(Integer)
    current_value = Column(Float)
    trading_value = Column(Float)
    tile_class = Column(Integer)
    tile_class_revenue = Column(Float)
    update_time = Column(DateTime, index=True)
    profile_id = Column(String)