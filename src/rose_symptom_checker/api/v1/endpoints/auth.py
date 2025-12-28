from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from rose_symptom_checker.schemas.auth import Token, LoginRequest
from rose_symptom_checker.schemas.user import UserCreate, UserResponse
from rose_symptom_checker.schemas.base import BaseResponse
from rose_symptom_checker.services.auth import AuthService, get_current_user
from rose_symptom_checker.services.user import UserService
from rose_symptom_checker.db.models.user import User
from rose_symptom_checker.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=BaseResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user = UserService.create_user(db, user_data)
    return BaseResponse.success_response(
        data=UserResponse.model_validate(user),
        message="User registered successfully"
    )


@router.post("/login", response_model=BaseResponse[Token])
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token"""
    user = AuthService.authenticate_user(db, login_data.email, login_data.password)
    access_token = AuthService.create_token(user)
    
    return BaseResponse.success_response(
        data=Token(access_token=access_token),
        message="Login successful"
    )


@router.get("/me", response_model=BaseResponse[UserResponse])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return BaseResponse.success_response(
        data=UserResponse.model_validate(current_user),
        message="User info retrieved successfully"
    )
