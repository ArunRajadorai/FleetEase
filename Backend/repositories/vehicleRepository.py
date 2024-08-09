from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.vehicleschema import VehicleCreate, VehicleUpdate
from ..models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_vehicle(self, vehicle_create: VehicleCreate) -> Optional[Vehicle]:
        try:
            vehicle = Vehicle(**vehicle_create.dict())
            self.db.add(vehicle)
            self.db.commit()
            self.db.refresh(vehicle)
            return vehicle
        except SQLAlchemyError as e:
            self.db.rollback()
            # Log the exception here if needed
            print(f"Error adding vehicle: {e}")
            return None

    def get_vehicles_by_user(self, user_id: int) -> List[Vehicle]:
        try:
            return self.db.query(Vehicle).filter(Vehicle.user_id == user_id).all()
        except SQLAlchemyError as e:
            # Log the exception here if needed
            print(f"Error fetching vehicles for user {user_id}: {e}")
            return []

    def update_vehicle(self, vehicle_id: int, vehicle_update: VehicleUpdate) -> Optional[Vehicle]:
        try:
            vehicle = self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
            if vehicle:
                for key, value in vehicle_update.dict().items():
                    setattr(vehicle, key, value)
                self.db.commit()
                self.db.refresh(vehicle)
                return vehicle
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            # Log the exception here if needed
            print(f"Error updating vehicle {vehicle_id}: {e}")
            return None

    def delete_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        try:
            vehicle = self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
            if vehicle:
                self.db.delete(vehicle)
                self.db.commit()
                return vehicle
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            # Log the exception here if needed
            print(f"Error deleting vehicle {vehicle_id}: {e}")
            return None
