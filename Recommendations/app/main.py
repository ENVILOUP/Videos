from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import redis.asyncio as aioredis

from app.routers import videos
from app.dependencies import get_redis


class BaseMessage(BaseModel):
    status: int
    message: str


app = FastAPI(
    title='Recommendations service',    
    redirect_slashes=False
)


@app.get("/health-check")
async def health_check(redis: Annotated[aioredis.Redis, Depends(get_redis)]):
    return BaseMessage(status=200, message='Ok')


app.include_router(videos.router, prefix='/api/v1/videos')
