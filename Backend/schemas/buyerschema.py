from pydantic import BaseModel
from typing import List


class VehicleBuyerResponse(BaseModel):
    vehicle_id: int
    vehicle_name: str


class VehicleBuyerRequest(BaseModel):
    buyer_id: int



