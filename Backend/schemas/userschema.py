# schemas/userschema.py
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserRead(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
