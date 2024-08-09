# services/authservice.py
from sqlalchemy.orm import Session
from ..schemas.userschema import UserCreate, Login
from ..repositories.userRepository import UserRepository
from ..utils.authhandler import create_access_token, get_password_hash, verify_password

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_username(self, username: str):
        """Retrieve a user by their username."""
        return self.user_repository.get_user_by_username(username)

    def register_user(self, user: UserCreate):
        """Register a new user with a hashed password."""
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        return self.user_repository.create_user(user)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return verify_password(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        """Create a JWT access token."""
        return create_access_token(data=data)
