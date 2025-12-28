from fastapi import APIRouter
from rose_symptom_checker.api.v1.endpoints import auth, diagnosis

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(diagnosis.router)