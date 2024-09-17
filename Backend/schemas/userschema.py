from pydantic import BaseModel, EmailStr
from typing import Optional


#Schema for Profile PAGE DATATABLE
class UserVehicleResponse(BaseModel):
    name: str
    make_model: str
    year: int
    date: Optional[str]  # ISO format date or None
    status: str


class GetUserProfile(BaseModel):
    user_id: int


class UserProfileResponse(BaseModel):
    name: str
    email: str
    phone: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: str
    #address: str
    mobile_number: int
    #email: str

    # @classmethod
    # def normalize_role(cls, user_type: str) -> str:
    #     # Ensure the role is in uppercase
    #     return user_type.upper()


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


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


class Login(BaseModel):
    username: str
    password: str
