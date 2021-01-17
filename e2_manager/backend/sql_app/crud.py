from sqlalchemy.orm import Session

from . import models, schemas



def get_country_by_code(db: Session, country_code: str):
    return db.query(models.Country).filter(models.Country.country_code == country_code).first()

def get_countries(db: Session, skip: int = 0, limit: int = 100 ):
    return db.query(models.Country).offset(skip).limit(limit).all()

def get_country_historical_by_code(db: Session, country_code: str):
    return db.query(models.CountryHistorical).filter(models.CountryHistorical.country_code == country_code).all()

def get_countries_historical(db: Session, skip: int = 0, limit: int = 100 ):
    return db.query(models.CountryHistorical).offset(skip).limit(limit).all()

def create_country(db: Session, country: schemas.CountryMod):
    db_country = models.Country(country_code=country.country_code,update_time=country.update_time, trade_average=country.trade_average,final=country.final,total_tiles_sold=country.total_tiles_sold)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def update_country(db: Session, country: schemas.CountryMod, historical_country: schemas.CountryHistoricalMod):
    db_historical = models.CountryHistorical(country_code=historical_country.country_code,update_time=historical_country.update_time, trade_average=historical_country.trade_average,final=historical_country.final,total_tiles_sold=historical_country.total_tiles_sold)
    db_country = models.Country(id=historical_country.id, country_code=country.country_code,update_time=country.update_time, trade_average=country.trade_average,final=country.final,total_tiles_sold=country.total_tiles_sold)
    
    db.merge(db_country)
    db.add(db_historical)
    db.commit()
    db.refresh(historical_country)

    return db_country
