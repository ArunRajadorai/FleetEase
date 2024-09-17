from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class VehicleFilterRequest(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    minPrice: Optional[float] = None
    maxPrice: Optional[float] = None
    transmission: Optional[str] = None


class EnquiryCreate(BaseModel):
    username: str = Field(..., max_length=100)
    email: EmailStr
    message: str
    sellerId: int
    buyerId: int
    vehicle_name: str
