from typing import Annotated
from fastapi import APIRouter, Depends

import redis.asyncio as aioredis

from app.helpers.exceptions import ValueException
from app.repository import RedisVideosRecommendation
from app.schemas import PagedResponse, VideoModel
from app.helpers.schemas import SuccessResponse
from app.helpers.statuses import StatusCodes
from app.dependencies import get_redis


router = APIRouter()


@router.get(
    path="/",
    response_model=SuccessResponse[PagedResponse[VideoModel]]
)
async def get_videos(
    redis: Annotated[aioredis.Redis, Depends(get_redis)],
    page_size: int = 20,
    page: int = 1,
):
    if page < 1:
        raise ValueException('Page must be greater than 0')

    if page_size < 1 or page_size > 50:
        raise ValueException('Page size must be between 1 and 50')

    repository = RedisVideosRecommendation(redis)
    videos = await repository.get_random_recommendations(page_size)

    return {
        'status_code': StatusCodes.OK,
        'data': {
            'page': page,
            'page_size': page_size,
            'items': [
                VideoModel(
                    video_uuid=video
                )
                for video in videos
            ]
        }
    }
