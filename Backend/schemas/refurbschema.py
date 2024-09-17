from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List
from enum import Enum


class RefurbishmentStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RefurbishmentBase(BaseModel):
    user_id: int
    vehicle_id: int
    service_description: str
    service_type: str
    status: str

    class Config:
        orm_mode = True


class RefurbishmentCreate(RefurbishmentBase):
    pass

    class Config:
        orm_mode = True


class RefurbishmentCreateResponse(BaseModel):
    refurbishment_id: int
