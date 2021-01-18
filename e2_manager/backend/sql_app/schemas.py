from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

class CountryBase(BaseModel):
    country_code: str
    update_time: datetime
    trade_average: float
    final: float
    total_tiles_sold: int


class CountryMod(CountryBase):
    pass


class Country(CountryBase):
    id: int

    class Config:
        orm_mode = True


class CountryHistoricalBase(CountryBase):
    pass

class CountryHistoricalMod(CountryBase):
    pass

class CountryHistorical(CountryBase):
    id: int

    class Config:
        orm_mode = True





class PropertyBase(BaseModel):
    for_sale: bool
    description: str
    location: str
    center: str
    price: float
    country: str
    tile_count: int
    current_value: float
    trading_value: float
    tile_class: int

class PropertyMod(PropertyBase):
    landfield_id: str
    update_time: datetime
    profile_id: str


class Property(PropertyBase):
    id: int

    class Config:
        orm_mode = True


class PropertyHistoricalBase(PropertyBase):
    pass

class PropertyHistoricalMod(PropertyBase):
    pass

class PropertyHistorical(PropertyBase):
    id: int

    class Config:
        orm_mode = True
