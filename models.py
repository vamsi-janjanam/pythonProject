from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    range = Column(Float)
    speed = Column(Float)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"))

    aircraft = relationship("Aircraft", back_populates="performance")


class Cabin(Base):
    __tablename__ = "cabin"

    id = Column(Integer, primary_key=True, index=True)
    total_interior_length = Column(Float)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"))

    aircraft = relationship("Aircraft", back_populates="cabin")


class Systems(Base):
    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, index=True)
    engine = Column(String)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"))

    aircraft = relationship("Aircraft", back_populates="systems")


class Aircraft(Base):
    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    performances = relationship("Performance", back_populates="aircraft")
    cabins = relationship("Cabin", back_populates="aircraft")
    systems = relationship("Systems", back_populates="aircraft")
