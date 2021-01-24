from typing import List, Optional

from fastapi import FastAPI, Query, Depends, HTTPException
from queries import E2Queries




from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
E2Q = E2Queries()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"Made with love": "for the E2 community"}

@app.get("/e2/countries")
def get_country_data_from_e2( c: List[str] = Query(None, min_length=1)):
    return E2Q.get_countries_data( c )

@app.get("/e2/countries/all")
def get_all_country_data_from_e2( c: List[str] = Query(None, min_length=1)):
    return E2Q.get_countries_data_all()

@app.get("/e2/properties/count")
def get_properties_count_by_id_from_e2( profile_id: str ):
    return E2Q.get_properties_count( profile_id )

@app.get("/e2/properties")
def get_properties_by_id_from_e2( profile_id: str, page: int = 1, property_count: int = 60 ):
    return E2Q.get_properties( profile_id, page, property_count )



@app.get("/db/countries/", response_model=List[schemas.Country])
def get_countries_from_db(skip: int = 0, limit: int = 100, country_code: Optional[str] = None, db: Session = Depends(get_db)):
    if country_code is None:
        return crud.get_countries(db, skip=skip, limit=limit)
    else:
        return [ crud.get_country_by_code(db=db, country_code=country_code) ]

@app.get("/db/properties", response_model=List[schemas.Property])
def get_properties_from_db(skip: int = 0, limit: int = 100, profile_id: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_properties(db, skip=skip, limit=limit, profile_id=profile_id)


@app.get("/db/countries/historical", response_model=List[schemas.CountryHistorical])
def get_countries_historical_data_from_db(skip: int = 0, limit: int = 100, country_code: Optional[str] = None, db: Session = Depends(get_db)):
    if country_code is None:
        return crud.get_countries_historical(db, skip=skip, limit=limit)
    else:
        return crud.get_country_historical_by_code(db=db, country_code=country_code)

@app.get("/db/properties/by_profile_id")
def get_all_properties_by_id_from_db( db: Session = Depends(get_db), skip: int = 0, limit: int = 0, profile_id: str = None ):
    return crud.get_properties( db=db, skip=skip,limit=limit, profile_id=profile_id )


@app.get("/db/properties/profile_ids")
def get_all_profile_id_from_db( db: Session = Depends(get_db) ):
    return crud.get_properties_profile_ids( db=db )

@app.get("/db/properties/profile_ids/count")
def get_properties_by_id_count_from_db( db: Session = Depends(get_db), profile_id: str = None ):
    return crud.get_properties_profile_ids_count( db=db, profile_id=profile_id )


@app.post("/db/countries/save", response_model=List[schemas.Country])
def save_countries_to_db( countries: List[schemas.CountryMod], db: Session = Depends(get_db)):
    saved_countries = []
    for country in countries:
        db_country = crud.get_country_by_code(db, country_code=country.country_code)
        if db_country:
            saved_countries.append( crud.update_country(db=db, country=country, historical_country=db_country) )
        else:
            saved_countries.append( crud.create_country(db=db, country=country) )


    return saved_countries

@app.post("/db/properties/save", response_model=List[schemas.Property])
def save_properties_to_db( properties: List[schemas.PropertyMod], db: Session = Depends(get_db)):
    post_result = []
    for prop in properties:
        db_property = crud.get_property_by_landfield_id(db, landfield_id=prop.landfield_id)
        if db_property:
            post_result.append( crud.update_property(db=db, prop=prop,historical_prop=db_property) )
        else:
            post_result.append( crud.create_property(db=db, prop=prop) )

    return post_result