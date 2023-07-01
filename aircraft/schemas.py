from pydantic import BaseModel


class PerformanceBase(BaseModel):
    range: float
    speed: float


class PerformanceCreate(PerformanceBase):
    pass


class PerformanceUpdate(PerformanceBase):
    pass


class CabinBase(BaseModel):
    total_interior_length: float


class CabinCreate(CabinBase):
    pass


class CabinUpdate(CabinBase):
    pass


class SystemsBase(BaseModel):
    engine: str


class SystemsCreate(SystemsBase):
    pass


class SystemsUpdate(SystemsBase):
    pass


class AircraftBase(BaseModel):
    name: str


class AircraftCreate(AircraftBase):
    performances: PerformanceCreate
    cabins: CabinCreate
    systems: SystemsCreate


class AircraftUpdate(AircraftBase):
    performances: PerformanceUpdate
    cabins: CabinUpdate
    systems: SystemsUpdate


class Aircraft(AircraftBase):
    id: int

    class Config:
        orm_mode = True
