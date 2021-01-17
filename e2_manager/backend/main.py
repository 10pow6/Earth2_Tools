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
    return {"Made with love": "by Dworak and butt"}

@app.get("/countries/e2")
def read_e2_countries( c: List[str] = Query(None, min_length=1)):
    return E2Q.get_countries_data( c )


@app.get("/countries/db", response_model=List[schemas.Country])
def read_db_countries(skip: int = 0, limit: int = 100, country_code: Optional[str] = None, db: Session = Depends(get_db)):
    if country_code is None:
        return crud.get_countries(db, skip=skip, limit=limit)
    else:
        return [ crud.get_country_by_code(db=db, country_code=country_code) ]
    

@app.get("/countries_historical/db", response_model=List[schemas.CountryHistorical])
def read_db_countries_historical(skip: int = 0, limit: int = 100, country_code: Optional[str] = None, db: Session = Depends(get_db)):
    if country_code is None:
        return crud.get_countries_historical(db, skip=skip, limit=limit)
    else:
        return crud.get_country_historical_by_code(db=db, country_code=country_code)

@app.post("/countries/db", response_model=schemas.Country)
def mod_country( country: schemas.CountryMod, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_code(db, country_code=country.country_code)
    if db_country:
        return crud.update_country(db=db, country=country, historical_country=db_country)

    return crud.create_country(db=db, country=country)