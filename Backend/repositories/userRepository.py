# repositories/userRepository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from ..models.user import User
from ..schemas.userschema import UserCreate, UserUpdate
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        logger.debug("UserRepository initialized")

    def get_user_by_username(self, username: str):
        """Retrieve a user by their username."""
        logger.debug(f"Retrieving user by username: {username}")
        try:
            user = self.db.query(User).filter(User.username == username).one()
            logger.debug(f"User found: {user}")
            return user
        except NoResultFound:
            logger.warning(f"No user found with username: {username}")
            return None

    def create_user(self, user: UserCreate):
        """Create a new user record."""
        logger.debug(f"Creating user with username: {user.username}")
        db_user = User(
            username=user.username,
            hashed_password=user.password,  # Assuming user.password is hashed already
            address=user.address,
            mobile_number=user.mobile_number,
            user_type=user.user_type
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        logger.debug(f"User created: {db_user}")
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate):
        """Update an existing user record."""
        logger.debug(f"Updating user with id: {user_id}")
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            logger.warning(f"No user found with id: {user_id}")
            return None

        if user_update.address is not None:
            db_user.address = user_update.address
        if user_update.mobile_number is not None:
            db_user.mobile_number = user_update.mobile_number
        if user_update.user_type is not None:
            db_user.user_type = user_update.user_type

        self.db.commit()
        self.db.refresh(db_user)
        logger.debug(f"User updated: {db_user}")
        return db_user

    def delete_user(self, user_id: int):
        """Delete a user record."""
        logger.debug(f"Deleting user with id: {user_id}")
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            logger.warning(f"No user found with id: {user_id}")
            return None

        self.db.delete(db_user)
        self.db.commit()
        logger.debug(f"User deleted: {db_user}")
        return db_user

    def get_users(self):
        """Retrieve all users."""
        logger.debug("Retrieving all users")
        users = self.db.query(User).all()
        logger.debug(f"Users retrieved: {users}")
        return users
