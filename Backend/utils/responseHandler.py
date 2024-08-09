from typing import Optional, Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    data: Optional[Any]
    message: str
    success: bool
