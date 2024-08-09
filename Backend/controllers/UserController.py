# api/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.userschema import UserCreate, UserRead, UserUpdate, Login
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
        existing_user = user_service.get_user_by_username(user.username)
        if existing_user:
            logger.error("Username already registered")
            raise HTTPException(status_code=400, detail="Username already registered")

        created_user = user_service.add_user(user)
        logger.info("User registered successfully")
        return ApiResponse(data=created_user, message="User registered successfully", success=True)
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
