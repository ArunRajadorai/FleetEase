from xmlrpc.client import DateTime

from sqlalchemy import Column, Integer, String, Float, Text, JSON, func, DATETIME
from Backend.database.config import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  # Removed ForeignKey constraint
    vehicle_name = Column(String)
    make = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    regular_price = Column(Integer)
    sale_price = Column(Integer)
    location = Column(String)
    mileage = Column(String)
    description = Column(Text)
    service_history = Column(Text)
    img_src = Column(String)
    created_at = Column(DATETIME, default=func.now())
    transmission = Column(String)
