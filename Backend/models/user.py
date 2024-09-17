# models/user.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class UserTypeEnum(PyEnum):
    seller = "seller"
    buyer = "buyer"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    address = Column(String, nullable=True)
    mobile_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    user_type = Column(Enum(UserTypeEnum), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, user_type={self.user_type})>"
