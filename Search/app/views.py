from fastapi import APIRouter

from app.helpers.statuses import StatusCodes

router = APIRouter()


@router.get("/health-check")
async def health_check():
    return {
        "status_code": StatusCodes.OK,
        "data": "Didn't fall down :0"
    }
