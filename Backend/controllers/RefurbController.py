from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas.refurbschema import RefurbishmentCreate, RefurbishmentRead, RefurbishmentUpdate
from ..services.refurbservice import RefurbService
from ..repositories.refurbrepository import RefurbRepository
from ..database.config import get_db
from ..utils.logger import setup_logger
from ..utils.responseHandler import ApiResponse

refurbishment_router = APIRouter()
logger = setup_logger(__name__)


@refurbishment_router.post("/", response_model=ApiResponse)
def create_refurbishment(refurbishment: RefurbishmentCreate, db: Session = Depends(get_db)):
    try:
        refurbishment_service = RefurbService(RefurbRepository(db))
        created_refurbishment = refurbishment_service.create_refurbishment(refurbishment)
        return ApiResponse(data=created_refurbishment, message="Refurbishment created successfully", success=True)
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@refurbishment_router.get("/{refurbishment_id}", response_model=ApiResponse)
def get_refurbishment(refurbishment_id: int, db: Session = Depends(get_db)):
    try:
        refurbishment_service = RefurbService(RefurbRepository(db))
        refurbishment = refurbishment_service.get_refurbishment(refurbishment_id)
        if not refurbishment:
            raise HTTPException(status_code=404, detail="Refurbishment not found")
        return ApiResponse(data=refurbishment, message="Refurbishment retrieved successfully", success=True)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@refurbishment_router.get("/user/{user_id}", response_model=ApiResponse)
def get_refurbishments_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        refurbishment_service = RefurbService(RefurbRepository(db))
        refurbishments = refurbishment_service.get_refurbishments_by_user(user_id)
        return ApiResponse(data=refurbishments, message="Refurbishments retrieved successfully", success=True)
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@refurbishment_router.put("/{refurbishment_id}", response_model=ApiResponse)
def update_refurbishment(refurbishment_id: int, refurbishment_update: RefurbishmentUpdate,
                         db: Session = Depends(get_db)):
    try:
        refurbishment_service = RefurbService(RefurbRepository(db))
        updated_refurbishment = refurbishment_service.update_refurbishment(refurbishment_id, refurbishment_update)
        if not updated_refurbishment:
            raise HTTPException(status_code=404, detail="Refurbishment not found")
        return ApiResponse(data=updated_refurbishment, message="Refurbishment updated successfully", success=True)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)


@refurbishment_router.delete("/{refurbishment_id}", response_model=ApiResponse)
def delete_refurbishment(refurbishment_id: int, db: Session = Depends(get_db)):
    try:
        refurbishment_service = RefurbService(RefurbRepository(db))
        deleted_refurbishment = refurbishment_service.delete_refurbishment(refurbishment_id)
        if not deleted_refurbishment:
            raise HTTPException(status_code=404, detail="Refurbishment not found")
        return ApiResponse(data=deleted_refurbishment, message="Refurbishment deleted successfully", success=True)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(data=None, message=str(e), success=False)
