from sqlalchemy.orm import Session

from . import models, schemas


############## COUNTRY CRUD
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
    db_historical = models.CountryHistorical(
        country_code=historical_country.country_code,
        update_time=historical_country.update_time, 
        trade_average=historical_country.trade_average,
        final=historical_country.final,
        total_tiles_sold=historical_country.total_tiles_sold)
    db_country = models.Country(
        id=historical_country.id, 
        country_code=country.country_code,
        update_time=country.update_time, 
        trade_average=country.trade_average,
        final=country.final,
        total_tiles_sold=country.total_tiles_sold)
    
    db.merge(db_country)
    db.add(db_historical)
    db.commit()
    db.refresh(historical_country)

    return db_country


############## PROPERTY CRUD
def get_properties(db: Session, skip: int = 0, limit: int = 100, profile_id: str = None):
    if profile_id is None:
        return db.query(models.Property).offset(skip).limit(limit).all()
    else:
        return db.query(models.Property).filter(models.PropertyMod.profile_id == profile_id).offset(skip).limit(limit).all()

def get_property_by_landfield_id(db: Session, landfield_id: str):
    return db.query(models.Property).filter(models.Property.landfield_id == landfield_id).first()

def create_property(db: Session, prop: schemas.PropertyMod ):
    db_property =  models.Property( 
        landfield_id=prop.landfield_id, 
        for_sale=prop.for_sale, 
        description=prop.description,
        location=prop.location,
        center=prop.center,
        price=prop.price,
        country=prop.country,
        tile_count=prop.tile_count,
        current_value=prop.current_value,
        trading_value=prop.trading_value,
        tile_class=prop.tile_class,
        tile_class_revenue=prop.tile_class_revenue,
        update_time=prop.update_time,
        profile_id=prop.profile_id
        )

    db.add(db_property)
    db.commit()
    db.refresh(db_property)

    return db_property

def update_property(db: Session, prop: schemas.PropertyMod, historical_prop: schemas.PropertyMod ):
    db_historical_property =  models.PropertyHistorical( 
        landfield_id=historical_prop.landfield_id, 
        for_sale=historical_prop.for_sale, 
        description=historical_prop.description,
        location=historical_prop.location,
        center=historical_prop.center,
        price=historical_prop.price,
        country=historical_prop.country,
        tile_count=historical_prop.tile_count,
        current_value=historical_prop.current_value,
        trading_value=historical_prop.trading_value,
        tile_class=historical_prop.tile_class,
        tile_class_revenue=historical_prop.tile_class_revenue,
        update_time=historical_prop.update_time,
        profile_id=historical_prop.profile_id
        )

    db_property =  models.Property( 
        id = historical_prop.id,
        landfield_id=prop.landfield_id, 
        for_sale=prop.for_sale, 
        description=prop.description,
        location=prop.location,
        center=prop.center,
        price=prop.price,
        country=prop.country,
        tile_count=prop.tile_count,
        current_value=prop.current_value,
        trading_value=prop.trading_value,
        tile_class=prop.tile_class,
        tile_class_revenue=prop.tile_class_revenue,
        update_time=prop.update_time,
        profile_id=prop.profile_id
        )

    db.merge(db_property)
    db.add(db_historical_property)
    db.commit()
    db.refresh(historical_prop)

    return db_property
