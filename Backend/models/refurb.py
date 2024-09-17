from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Enum, Float, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class Refurbishment(Base):
    __tablename__ = 'refurbishments'

    refurbishment_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, nullable=False)
    vehicle_id = Column(Integer, nullable=False)
    service_description = Column(String, nullable=False)
    service_type = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    
