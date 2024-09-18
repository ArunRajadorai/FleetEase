from typing import List

from fastapi import APIRouter, Depends, HTTPException, APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session

from ..schemas.buyerschema import VehicleBuyerRequest
from ..schemas.filterschema import VehicleFilterRequest
from ..schemas.vehicleschema import VehicleCreate, PurchaseRequest
from ..services.vehicleservice import VehicleService
from ..repositories.vehicleRepository import VehicleRepository
from ..database.config import get_db
from ..utils.responseHandler import ApiResponse

vehicle_router = APIRouter()


def get_vehicle_service(db: Session = Depends(get_db)):
    return VehicleService(VehicleRepository(db))


@vehicle_router.get("/vehicles", response_model=ApiResponse)
def fetch_vehicles(vehicle_service: VehicleService = Depends(get_vehicle_service)):
    try:
        vehicles = vehicle_service.get_all_vehicles()
        if vehicles:
            return ApiResponse(data=vehicles, message="Vehicles retrieved successfully", success=True)
        else:
            return ApiResponse(data=[], message="No vehicles Found", success=False)
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@vehicle_router.post("/filter-vehicles", response_model=ApiResponse)
def filter_vehicles(request: VehicleFilterRequest, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    try:
        vehicles = vehicle_service.filter_vehicles(
            make=request.make,
            model=request.model,
            year=request.year,
            minPrice=request.minPrice,
            maxPrice=request.maxPrice,
            transmission=request.transmission
        )
        if vehicles:
            return ApiResponse(data=vehicles, message="Vehicles retrieved successfully", success=True)
        else:
            return ApiResponse(data=[], message="No vehicles Found", success=False)
    except Exception as e:
        return ApiResponse(data=[], message=str(e), success=False)


@vehicle_router.get("/vehicles/{vehicle_id}", response_model=ApiResponse)
def fetch_vehicle_details(vehicle_id: int, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    try:
        vehicle = vehicle_service.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return ApiResponse(data=vehicle, message="Vehicle details retrieved successfully", success=True)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@vehicle_router.post("/buyer-vehicles", response_model=ApiResponse)
def fetch_vehicles(request: VehicleBuyerRequest,
                   vehicle_service: VehicleService = Depends(get_vehicle_service)):  # Service dependency
    try:
        buyer_id = request.buyer_id
        vehicles = vehicle_service.get_vehicles_by_buyer_id(buyer_id)
        return ApiResponse(data=vehicles, message="Vehicles retrieved successfully", success=True)
    except Exception as e:
        return ApiResponse(data=[], message=str(e), success=False)


@vehicle_router.post("/purchase_vehicle", response_model=ApiResponse)
def purchase_vehicle(request: PurchaseRequest,
                     vehicle_service: VehicleService = Depends(get_vehicle_service)):  # Service dependency
    try:
        vehicle_id = request.vehicleId
        buyer_id = request.userId
        success = vehicle_service.process_purchase(vehicle_id, buyer_id)
        if success:
            return ApiResponse(data={}, message="Purchase successful", success=True)
        else:
            return ApiResponse(data={}, message="Purchase failed", success=False)
    except Exception as e:
        return ApiResponse(data={}, message=str(e), success=False)


@vehicle_router.post("/create_vehicle", response_model=ApiResponse)
async def create_vehicle(
        vehicle_name: str = Form(...),
        year: int = Form(...),
        make: str = Form(...),
        model: str = Form(...),
        mileage: str = Form(...),
        transmission: str = Form(...),
        regular_price: str = Form(...),
        sale_price: str = Form(...),
        description: str = Form(...),
        service_history: str = Form(...),
        user_id: int = Form(...),
        location: str = Form(...),
        img_src: List[UploadFile] = File(...),
        vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    try:
        # Save images and get URLs
        img_urls = []
        for image in img_src:
            # Implement image saving logic here
            image_url = await vehicle_service.save_image(image)
            img_urls.append(image_url)

        vehicle_data = VehicleCreate(
            vehicle_name=vehicle_name,
            year=year,
            make=make,
            model=model,
            mileage=mileage,
            transmission=transmission,
            regular_price=regular_price,
            sale_price=sale_price,
            description=description,
            service_history=service_history,
            location=location

        )

        created_vehicle = await vehicle_service.add_vehicle(vehicle_data, img_urls, user_id)
        return ApiResponse(message="Vehicle created successfully", success=True, data=created_vehicle)
    except Exception as e:
        return ApiResponse(message=str(e), success=False, data=None)


@vehicle_router.delete("/delete_vehicle/{vehicle_id}", response_model=ApiResponse)
def delete_vehicle(vehicle_id: int, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    try:
        deleted_vehicle = vehicle_service.delete_vehicle(vehicle_id)
        if not deleted_vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return ApiResponse(data=deleted_vehicle, message="Vehicle deleted successfully", success=True)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)
