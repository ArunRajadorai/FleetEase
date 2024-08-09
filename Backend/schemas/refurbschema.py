from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from enum import Enum

class RefurbishmentStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RefurbishmentBase(BaseModel):
    user_id: int
    center_id: int
    service_type: str
    spare_parts: Optional[str] = None  # Comma-separated list of spare parts
    estimated_cost: float
    date: date
    time: time
    status: Optional[RefurbishmentStatusEnum] = RefurbishmentStatusEnum.SCHEDULED

class RefurbishmentCreate(RefurbishmentBase):
    pass

class RefurbishmentUpdate(BaseModel):
    service_type: Optional[str]
    spare_parts: Optional[str]
    estimated_cost: Optional[float]
    date: Optional[date]
    time: Optional[time]
    status: Optional[RefurbishmentStatusEnum]

class RefurbishmentRead(RefurbishmentBase):
    refurbishment_id: int

    class Config:
        orm_mode = True
