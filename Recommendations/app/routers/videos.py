from typing import Annotated
from fastapi import APIRouter, Depends
import redis.asyncio as aioredis

from app.dependencies import get_redis
from app.services.ml import get_recommendations_for_videos


router = APIRouter()


@router.get("/")
async def get_videos(user: str, redis: Annotated[aioredis.Redis, Depends(get_redis)]):
    redis_key = f'recommendations:{user}:videos'
    redis_expire = 60 # sec.
    videos = await redis.lrange(redis_key, 0, -1)

    if not videos:
        videos = await get_recommendations_for_videos()
        await redis.rpush(redis_key, *videos)
        await redis.expire(redis_key, redis_expire)

    videos = list(map(int, videos))

    return {'videos': videos}


