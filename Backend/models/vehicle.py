from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from Backend.database.config import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    make = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    price = Column(Float)
    location = Column(String)
    mileage = Column(Float)
    description = Column(Text)
    service_history = Column(Text)
    photos = Column(JSON)
