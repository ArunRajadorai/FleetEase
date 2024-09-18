from typing import List, Optional

from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..schemas.buyerschema import VehicleBuyerResponse
from ..schemas.vehicleschema import VehicleCreate, VehicleRead, VehicleResponse, FilterVehicle
from ..models.vehicle import Vehicle
from ..repositories import vehicleRepository
from fastapi import UploadFile
import aiofiles
import os

from ..utils.urlhelpers import appurl


class VehicleService:
    def __init__(self, repository: vehicleRepository):
        self.repository = repository

    async def add_vehicle(self, vehicle_data: VehicleCreate, img_urls: List[str], user_id) -> VehicleRead | None:
        try:
            created_vehicle = await self.repository.add_vehicle(vehicle_data, img_urls, user_id)
            return created_vehicle
        except Exception as e:
            print(f"Error in service layer: {e}")
            return None

    def get_vehicles_by_user(self, user_id: int) -> List[Vehicle]:
        return self.repository.get_vehicles_by_user(user_id)

    # def update_vehicle(self, vehicle_id: int, vehicle_update: VehicleUpdate) -> Optional[Vehicle]:
    #     return self.repository.update_vehicle(vehicle_id, vehicle_update)

    def delete_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return (self.repository.
                delete_vehicle(vehicle_id))

    def get_all_vehicles(self) -> List[Vehicle]:
        return self.repository.get_all_vehicles()

    # def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
    #     return self.repository.get_vehicle_by_id(vehicle_id)

    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[VehicleResponse]:
        # Retrieve the vehicle details from the repository by ID
        vehicle = self.repository.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return None

        # Construct the attributes list
        attributes = [
            {"title": "Make", "specification": str(vehicle.make)},
            {"title": "Model", "specification": str(vehicle.model)},
            {"title": "Mileage", "specification": str(vehicle.mileage)},
            {"title": "Year", "specification": str(vehicle.year)},
            {"title": "Transmission", "specification": str(vehicle.transmission)},
            {"title": "Location", "specification": str(vehicle.location)},

        ]

        # Return the VehicleResponse object
        return VehicleResponse(
            user_id=vehicle.user_id,
            vehicle_name=vehicle.vehicle_name,
            make=vehicle.make,
            model=vehicle.model,
            year=vehicle.year,
            regular_price=vehicle.regular_price,
            sale_price=vehicle.sale_price,
            location=vehicle.location,
            mileage=vehicle.mileage,
            description=vehicle.description,
            service_history=vehicle.service_history,
            transmission=vehicle.transmission,
            img_src=vehicle.img_src,
            attributes=attributes
        )
    @staticmethod
    async def save_image(image: UploadFile) -> str:
        # Define the directory where images will be saved
        directory = "Backend/static/images"

        # Check if the directory exists; if not, create it
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Define the file location
        file_location = os.path.join(directory, image.filename)

        # Save the image to the directory
        async with aiofiles.open(file_location, 'wb') as out_file:
            content = await image.read()
            await out_file.write(content)

        # Construct the full URL for the saved image
        # Assuming that your domain is 'https://yourdomain.com' and images are served under '/static/images/'
        base_url = appurl.BASE_URL
        relative_path = f"/static/images/{image.filename}".replace("\\", "/")

        # Return the full URL path
        full_url = f"{base_url}{relative_path}"
        return full_url

    def get_vehicles_by_buyer_id(self, buyer_id: int) -> List[VehicleBuyerResponse]:
        # Get the data from the repository layer
        try:
            vehicles = self.repository.get_vehicles_by_buyer_id(buyer_id)
            return [VehicleBuyerResponse(vehicle_id=row.vehicle_id, vehicle_name=row.vehicle_name)
                    for row in vehicles]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def process_purchase(self, vehicle_id: int, buyer_id: int) -> bool:
        vehicle = self.repository.get_vehicle_by_id(vehicle_id)

        if vehicle is None:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        # Example: Update the vehicle status to "sold" or similar
        vehicle.status = 'Purchased'
        vehicle.user_id = buyer_id

        success = self.repository.update_vehicle(vehicle)
        return success

    def filter_vehicles(self, make, model, year,
                        minPrice,
                        maxPrice,transmission) -> List[VehicleRead]:
        vehicles = self.repository.filter_vehicles(
            make=make,
            model=model,
            year=year,
            minPrice=minPrice,
            maxPrice=maxPrice,
            transmission=transmission
        )
        # Convert ORM models to Pydantic models
        car_list = []

        for vehicle in vehicles:
            attributes = [
                {"title": "Mileage", "specification": vehicle.mileage},
                {"title": "Year", "specification": str(vehicle.year)},
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
            print(car_list)
        return car_list

    # def get_all_filtervehicles(self):
    #     try:
    #         vehicles = self.repository.get_all_filtervehicles(buyer_id)
    #         return [VehicleBuyerResponse(vehicle_id=row.vehicle_id, vehicle_name=row.vehicle_name)
    #                 for row in vehicles]
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
