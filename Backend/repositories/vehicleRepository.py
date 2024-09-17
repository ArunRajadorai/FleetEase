import json
from typing import List, Optional, Type, Dict, Any, Sequence

from fastapi import HTTPException
from sqlalchemy import select, Row
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.vehicleschema import VehicleCreate, VehicleRead
from ..models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_vehicles(self) -> List[Type[Vehicle]]:
        try:
            vehicles = self.db.query(Vehicle).all()

            if not vehicles:
                raise HTTPException(status_code=404, detail="No vehicles found")

            car_list = []
            for vehicle in vehicles:
                attributes = [
                    {"title": "Mileage", "specification": vehicle.mileage},
                    {"title": "Year", "specification": vehicle.year},
                    {"title": "Transmission", "specification": vehicle.transmission},
                ]
                car_list.append({
                    "id": vehicle.vehicle_id,
                    "vehicle_name": vehicle.vehicle_name,
                    "vehicle_regular_price": vehicle.regular_price,
                    "vehicle_sale_price": vehicle.sale_price,
                    "img_src": vehicle.img_src,
                    "attributes": attributes
                })
                # car_list.append({
                #     "id": vehicle.vehicle_id,
                #     "car_name": vehicle.vehicle_name,
                #     "car_price": vehicle.regular_price,
                #     "car_new_price": vehicle.sale_price,
                #     "img_src": vehicle.img_src,
                #     "attributes": attributes,
                # })

            return car_list
        except SQLAlchemyError as e:
            print(f"Error fetching all vehicles: {e}")
            return []

    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        try:
            # Use the correct column name `vehicle_id`
            vehicle = self.db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
            return vehicle
        except SQLAlchemyError as e:
            print(f"Error fetching vehicle {vehicle_id}: {e}")
            return None

    async def add_vehicle(self, vehicle_data: VehicleCreate, img_urls: List[str], user_id) -> VehicleRead | None:
        try:
            # Manually extract attributes from VehicleCreate
            img_src_json = json.dumps(img_urls)
            vehicle = Vehicle(
                vehicle_name=vehicle_data.vehicle_name,
                year=vehicle_data.year,
                make=vehicle_data.make,
                model=vehicle_data.model,
                mileage=str(vehicle_data.mileage),
                transmission=str(vehicle_data.transmission),
                regular_price=vehicle_data.regular_price,
                sale_price=vehicle_data.sale_price,
                description=vehicle_data.description,
                service_history=vehicle_data.service_history,
                location=vehicle_data.location,
                user_id=user_id,
                img_src=img_src_json  # Add image URLs
            )
            self.db.add(vehicle)
            self.db.commit()
            self.db.refresh(vehicle)
            return VehicleRead.from_orm(vehicle)
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error adding vehicle: {e}")
            return None

    # def add_vehicle(self, vehicle_create: VehicleCreate) -> Optional[Vehicle]:
    #     try:
    #         vehicle = Vehicle(**vehicle_create.dict())
    #         self.db.add(vehicle)
    #         self.db.commit()
    #         self.db.refresh(vehicle)
    #         return vehicle
    #     except SQLAlchemyError as e:
    #         self.db.rollback()
    #         print(f"Error adding vehicle: {e}")
    #         return None

    def get_vehicles_by_user(self, user_id: int) -> List[Vehicle]:
        try:
            return self.db.query(Vehicle).filter(Vehicle.user_id == user_id).all()
        except SQLAlchemyError as e:
            print(f"Error fetching vehicles for user {user_id}: {e}")
            return []

    # def update_vehicle(self, vehicle_id: int, vehicle_update: VehicleUpdate) -> Optional[Vehicle]:
    #     try:
    #         # Use the correct column name `vehicle_id`
    #         vehicle = self.db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    #         if vehicle:
    #             for key, value in vehicle_update.dict().items():
    #                 setattr(vehicle, key, value)
    #             self.db.commit()
    #             self.db.refresh(vehicle)
    #             return vehicle
    #         return None
    #     except SQLAlchemyError as e:
    #         self.db.rollback()
    #         print(f"Error updating vehicle {vehicle_id}: {e}")
    #         return None

    def delete_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        try:
            # Use the correct column name `vehicle_id`
            vehicle = self.db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
            if vehicle:
                self.db.delete(vehicle)
                self.db.commit()
                return vehicle
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error deleting vehicle {vehicle_id}: {e}")
            return None

    def get_vehicles_by_buyer_id(self, buyer_id: int) -> Sequence[Row[Any]] | list[Any]:
        # Query to select only vehicle_id and vehicle_name
        try:
            query = select(Vehicle.vehicle_id, Vehicle.vehicle_name).where(Vehicle.user_id == buyer_id)
            result = self.db.execute(query).fetchall()
            return result
        except SQLAlchemyError as e:
            print(f"Error fetching vehicles for user {buyer_id}: {e}")
            return []

    def filter_vehicles(self, make, model, year,
                        minPrice,
                        maxPrice, transmission) -> list[Type[Vehicle]] | list[Any]:
        try:
            query = self.db.query(Vehicle)

            if make is not None:
                query = query.filter(Vehicle.make == make)
            if model is not None:
                query = query.filter(Vehicle.model == model)
            if year is not None and year != 0:
                query = query.filter(Vehicle.year == year)
            if transmission is not None:
                query = query.filter(Vehicle.transmission == transmission)
            if minPrice is not None:
                query = query.filter(Vehicle.sale_price >= minPrice)
            if maxPrice is not None:
                query = query.filter(Vehicle.sale_price <= maxPrice)

            return query.all()
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error deleting vehicle: {e}")
            return []
