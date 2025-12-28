from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[Any] = None

    @classmethod
    def success_response(cls, data: T, message: str = "Success"):
        return cls(success=True, message=message, data=data, errors=None)
    
    @classmethod
    def error_response(cls, message: str, errors: Any = None):
        return cls(success=False, message=message, data=None, errors=errors)