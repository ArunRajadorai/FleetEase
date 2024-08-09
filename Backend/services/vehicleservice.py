from typing import List, Optional
from ..schemas.vehicleschema import VehicleCreate, VehicleUpdate
from ..models.vehicle import Vehicle
from ..repositories import vehicleRepository


class VehicleService:
    def __init__(self, repository: vehicleRepository):
        self.repository = repository

    def add_vehicle(self, vehicle_create: VehicleCreate) -> Vehicle:
        return self.repository.add_vehicle(vehicle_create)

    def get_vehicles_by_user(self, user_id: int) -> List[Vehicle]:
        return self.repository.get_vehicles_by_user(user_id)

    def update_vehicle(self, vehicle_id: int, vehicle_update: VehicleUpdate) -> Optional[Vehicle]:
        return self.repository.update_vehicle(vehicle_id, vehicle_update)

    def delete_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return (self.repository.
                delete_vehicle(vehicle_id))
