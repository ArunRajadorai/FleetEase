from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.userschema import UserCreate, UserRead, UserUpdate, Login, UserResponse
from ..services.userservice import UserService
from ..repositories.userRepository import UserRepository
from ..database.config import get_db
from ..utils.responseHandler import ApiResponse
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
user_router = APIRouter()


# Register a new user
@user_router.post("/register", response_model=ApiResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_service = UserService(UserRepository(db))
        existing_user = user_service.get_user_by_username(user.email)
        if existing_user:
            logger.error("Email already registered")
            raise HTTPException(status_code=400, detail="Email already registered")

        created_user = user_service.add_user(user)
        logger.info("User registered successfully")
        if created_user:
            return ApiResponse(data=UserResponse.from_orm(created_user), message="User registered successfully",
                               success=True)
        else:
            return ApiResponse(message="Error creating User",success=False)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return ApiResponse(data=None, message=str(e), success=False)


# Login an existing user
@user_router.post("/login", response_model=ApiResponse)
def login_user(user: Login, db: Session = Depends(get_db)):
    try:
        user_service = UserService(UserRepository(db))
        login_response = user_service.login_user(user.username, user.password)
        logger.info("Login successful")
        return ApiResponse(data=login_response, message="Login successful", success=True)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        return ApiResponse(data=None, message=str(e), success=False)


@user_router.get("/get-details/{user_id}", response_model=ApiResponse)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service = UserService(UserRepository(db))
        user_details = user_service.get_user_by_id(user_id)
        if user_details:
            return ApiResponse(data=user_details, message="User details fetched successfully", success=True)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user details: {e}")
        return ApiResponse(data=None, message=str(e), success=False)


@user_router.get("/get-uservehicles/{user_id}", response_model=ApiResponse)
def get_user_vehicles(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service = UserService(UserRepository(db))
        user_vehicles = user_service.get_vehicles_with_refurb_status(user_id)
        if user_vehicles:
            return ApiResponse(data=user_vehicles, message="Vehicles fetched successfully", success=True)
        else:
            return ApiResponse(data=[], message="No vehicles found for the user", success=True)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user vehicles: {e}")
        return ApiResponse(data=[], message=str(e), success=False)
