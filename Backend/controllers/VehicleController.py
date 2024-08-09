from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas.vehicleschema import VehicleCreate, VehicleRead, VehicleUpdate
from ..services.vehicleservice import VehicleService
from ..repositories.vehicleRepository import VehicleRepository
from ..database.config import get_db
from ..utils.responseHandler import ApiResponse

vehicle_router = APIRouter()

vehicle_service = VehicleService(VehicleRepository())


@vehicle_router.post("/create_vehicle", response_model=ApiResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    try:
        created_vehicle = vehicle_service.add_vehicle(vehicle)
        return ApiResponse(data=created_vehicle, message="Vehicle created successfully", success=True)
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@vehicle_router.get("/user_vehicle/{user_id}", response_model=ApiResponse)
def list_vehicles(user_id: int, db: Session = Depends(get_db)):
    try:
        vehicles = vehicle_service.get_vehicles_by_user(user_id)
        return ApiResponse(data=vehicles, message="Vehicles retrieved successfully", success=True)
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@vehicle_router.put("/update_vehicle/{vehicle_id}", response_model=ApiResponse)
def update_vehicle(vehicle_id: int, vehicle: VehicleUpdate, db: Session = Depends(get_db)):
    try:
        updated_vehicle = vehicle_service.update_vehicle(vehicle_id, vehicle)
        if not updated_vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return ApiResponse(data=updated_vehicle, message="Vehicle updated successfully", success=True)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@vehicle_router.delete("/delete_vehicle/{vehicle_id}", response_model=ApiResponse)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    try:
        deleted_vehicle = vehicle_service.delete_vehicle(vehicle_id)
        if not deleted_vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return ApiResponse(data=deleted_vehicle, message="Vehicle deleted successfully", success=True)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)
