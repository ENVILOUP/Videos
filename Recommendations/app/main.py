from typing import Annotated
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import redis.asyncio as aioredis

from app.routers import videos
from app.dependencies import get_redis
from app.helpers.exceptions import BaseAppException
from app.helpers.schemas import ErrorResponse
from app.helpers.statuses import StatusCodes
from app.helpers.swagger import RESPONSES_TYPES_DOC


class BaseMessage(BaseModel):
    status: int
    message: str


app = FastAPI(
    title='Recommendations service',
    responses=RESPONSES_TYPES_DOC
)


@app.get("/health-check")
async def health_check(redis: Annotated[aioredis.Redis, Depends(get_redis)]):
    return BaseMessage(status=200, message='Ok')


app.include_router(videos.router, prefix='/api/v1/videos')


@app.exception_handler(BaseAppException)
async def base_application_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.http_status_code,
        content=ErrorResponse(
            status_code=exc.app_status_code
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status_code=StatusCodes.VALIDATION_ERROR
        ).model_dump()
    )
