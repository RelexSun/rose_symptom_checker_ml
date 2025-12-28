from sqlalchemy.orm import Session
from rose_symptom_checker.db.models.user import User
from rose_symptom_checker.schemas.user import UserCreate
from rose_symptom_checker.core.security import get_password_hash
from rose_symptom_checker.core.exceptions import ConflictException, NotFoundException
from typing import Optional


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise ConflictException("Email already registered")
            raise ConflictException("Username already taken")
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found")
        return user