from sqlalchemy.orm import Session

from . import models, schemas



def get_country_by_code(db: Session, country_code: str):
    return db.query(models.Country).filter(models.Country.country_code == country_code).first()

def get_countries(db: Session, skip: int = 0, limit: int = 100 ):
    return db.query(models.Country).offset(skip).limit(limit).all()

def create_country(db: Session, country: schemas.CountryMod):
    db_country = models.Country(country_code=country.country_code,update_time=country.update_time, trade_average=country.trade_average,final=country.final,total_tiles_sold=country.total_tiles_sold)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def update_country(db: Session, id: int, country: schemas.CountryMod):
    db_country = models.Country(id=id, country_code=country.country_code,update_time=country.update_time, trade_average=country.trade_average,final=country.final,total_tiles_sold=country.total_tiles_sold)
    db.merge(db_country)
    db.commit()
    return db_country
