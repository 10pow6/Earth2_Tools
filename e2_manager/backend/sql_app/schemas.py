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
