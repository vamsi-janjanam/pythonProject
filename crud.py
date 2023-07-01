from sqlalchemy.orm import Session
import models
import schemas


def create_aircraft(db: Session, aircraft: schemas.AircraftCreate):
    db_aircraft = models.Aircraft(name=aircraft.name)
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft


def get_aircraft(db: Session, aircraft_id: int):
    return db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()


def update_aircraft(db: Session, aircraft_id: int, aircraft: schemas.AircraftUpdate):
    db_aircraft = db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()
    if db_aircraft:
        db_aircraft.name = aircraft.name
        db.commit()
        db.refresh(db_aircraft)
    return db_aircraft


def delete_aircraft(db: Session, aircraft_id: int):
    db_aircraft = db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()
    if db_aircraft:
        db.delete(db_aircraft)
        db.commit()
        return db_aircraft


def get_aircrafts(db: Session, range: float = None, speed: float = None, cabin_size: float = None, engine: str = None):
    query = db.query(models.Aircraft)
    if range is not None:
        query = query.join(models.Performance).filter(models.Performance.range >= range)
    if speed is not None:
        query = query.join(models.Performance).filter(models.Performance.speed >= speed)
    if cabin_size is not None:
        query = query.join(models.Cabin).filter(models.Cabin.total_interior_length >= cabin_size)
    if engine is not None:
        query = query.join(models.Systems).filter(models.Systems.engine == engine)
    return query.all()
