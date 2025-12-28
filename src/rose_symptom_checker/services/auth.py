from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from rose_symptom_checker.core.security import verify_password, create_access_token, decode_access_token
from rose_symptom_checker.core.config import get_settings
from rose_symptom_checker.core.exceptions import UnauthorizedException
from rose_symptom_checker.services.user import UserService
from rose_symptom_checker.db.models.user import User
from rose_symptom_checker.db.session import get_db

settings = get_settings()
security = HTTPBearer()


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = UserService.get_user_by_email(db, email)
        if not user:
            raise UnauthorizedException("Invalid email or password")
        
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")
        
        if not user.is_active:
            raise UnauthorizedException("User account is inactive")
        
        return user
    
    @staticmethod
    def create_token(user: User) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        return access_token


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise UnauthorizedException()
    
    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise UnauthorizedException()
    
    user = UserService.get_user_by_id(db, user_id)
    return user