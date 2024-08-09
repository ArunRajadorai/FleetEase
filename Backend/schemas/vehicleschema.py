from pydantic import BaseModel
from typing import List


class VehicleBase(BaseModel):
    user_id: int
    make: str
    model: str
    year: int
    price: float
    location: str
    mileage: float
    description: str
    service_history: str
    photos: List[str]  # List of photo URLs


class VehicleCreate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    vehicle_id: int

    class Config:
        orm_mode = True


class VehicleUpdate(VehicleBase):
    pass
