
from typing import Generic, TypeVar
from pydantic import BaseModel

from app.helpers.statuses import StatusCodes

T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    status_code: StatusCodes
    data: T


class ErrorResponse(BaseModel, Generic[T]):
    success: bool = False
    status_code: StatusCodes
