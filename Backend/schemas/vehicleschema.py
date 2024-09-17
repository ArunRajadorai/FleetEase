from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class VehicleBase(BaseModel):
    vehicle_name: str
    make: str
    model: str
    year: int
    regular_price: int
    sale_price: int
    location: Optional[str] = None  # Make optional if it can be empty
    mileage: int
    description: str
    service_history: str
    transmission: str


class VehicleResponse(BaseModel):
    user_id: int
    vehicle_name: str
    make: str
    model: str
    year: int
    regular_price: int
    sale_price: int
    location: Optional[str] = None  # Make optional if it can be empty
    mileage: str
    description: str
    service_history: str
    transmission: str
    img_src: str
    attributes: List[Dict[str, str]]  # List of attribute dictionaries

    class Config:
        orm_mode = True
        from_attributes = True


class Attribute(BaseModel):
    title: str
    specification: str


# class VehicleResponse(BaseModel):
#     id: int
#     car_name: str
#     car_price: int
#     car_new_price: int
#     img_src: str
#     attributes: List[Attribute]
#
#     class Config:
#         orm_mode = True


class VehicleListResponse(BaseModel):
    vehicle: List[VehicleResponse]


class VehicleCreate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    vehicle_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class FilterVehicle(BaseModel):
    id: int
    vehicle_name: str
    vehicle_regular_price: int
    vehicle_sale_price: int
    vehicle_img_src: str
    attributes: List[Any]
