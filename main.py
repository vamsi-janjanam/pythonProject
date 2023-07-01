from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from aircraft import schemas, crud, database

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/aircraft/", response_model=schemas.Aircraft)
def create_aircraft(aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    return crud.create_aircraft(db=db, aircraft=aircraft)


@app.get("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def read_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db=db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return db_aircraft


@app.put("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def update_aircraft(
    aircraft_id: int, aircraft: schemas.AircraftUpdate, db: Session = Depends(get_db)
):
    updated_aircraft = crud.update_aircraft(
        db=db, aircraft_id=aircraft_id, aircraft=aircraft
    )
    if updated_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return updated_aircraft


@app.delete("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def delete_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.delete_aircraft(db=db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return db_aircraft


@app.get("/aircraft/", response_model=list[schemas.Aircraft])
def read_aircrafts(
    range: float = None,
    speed: float = None,
    cabin_size: float = None,
    engine: str = None,
    db: Session = Depends(get_db),
):
    return crud.get_aircrafts(
        db=db, range=range, speed=speed, cabin_size=cabin_size, engine=engine
    )
