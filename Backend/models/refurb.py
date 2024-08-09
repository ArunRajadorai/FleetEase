from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RefurbishmentStatusEnum(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Refurbishment(Base):
    __tablename__ = 'refurbishments'

    refurbishment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    center_id = Column(Integer, ForeignKey('service_centers.center_id'), nullable=False)
    service_type = Column(String, nullable=False)
    spare_parts = Column(String, nullable=True)  # Comma-separated list of spare parts
    estimated_cost = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(Enum(RefurbishmentStatusEnum), default=RefurbishmentStatusEnum.SCHEDULED, nullable=False)

    user = relationship("User", back_populates="refurbishments")
    center = relationship("ServiceCenter", back_populates="refurbishments")

    def __repr__(self):
        return f"<Refurbishment(refurbishment_id={self.refurbishment_id}, user_id={self.user_id}, center_id={self.center_id}, status={self.status})>"
