from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class BaseMessage(BaseModel):
    status: int
    message: str


@router.get("/health-check")
async def health_check():
    return BaseMessage(status=200, message="Ok")
