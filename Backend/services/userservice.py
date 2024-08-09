# services/userservice.py
from sqlalchemy.orm import Session
from ..schemas.userschema import UserCreate, UserUpdate, Login
from ..repositories.userRepository import UserRepository
from ..utils.authhandler import create_access_token, get_password_hash, verify_password
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        logger.debug("UserService initialized")

    def get_user_by_username(self, username: str):
        """Retrieve a user by their username."""
        logger.debug(f"Retrieving user by username: {username}")
        return self.user_repository.get_user_by_username(username)

    def add_user(self, user: UserCreate):
        """Add a new user with a hashed password."""
        logger.debug(f"Adding user with username: {user.username}")
        existing_user = self.get_user_by_username(user.username)
        if existing_user:
            logger.error("Username already registered")
            raise ValueError("Username already registered")

        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        created_user = self.user_repository.create_user(user)
        logger.debug(f"User added: {created_user}")
        return created_user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        logger.debug("Verifying password")
        return verify_password(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        """Create a JWT access token."""
        logger.debug(f"Creating access token for data: {data}")
        return create_access_token(data=data)

    def login_user(self, username: str, password: str):
        """Authenticate a user and return a JWT token."""
        logger.debug(f"Logging in user with username: {username}")
        user = self.get_user_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            logger.error("Invalid credentials")
            raise ValueError("Invalid credentials")

        access_token = self.create_access_token(data={"sub": username})
        logger.debug(f"User logged in, token created: {access_token}")
        return {"access_token": access_token, "token_type": "bearer"}

    def update_user(self, user_id: int, user_update: UserUpdate):
        """Update user information."""
        logger.debug(f"Updating user with id: {user_id}")
        return self.user_repository.update_user(user_id, user_update)

    def delete_user(self, user_id: int):
        """Delete a user."""
        logger.debug(f"Deleting user with id: {user_id}")
        return self.user_repository.delete_user(user_id)

    def get_users(self):
        """Retrieve all users."""
        logger.debug("Retrieving all users")
        return self.user_repository.get_users()
