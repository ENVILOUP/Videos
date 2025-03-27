from typing import Annotated
from fastapi import APIRouter, Depends, Query

import redis.asyncio as aioredis

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
    page_size: Annotated[int, Query(ge=1, le=50)] = 20,
    page: Annotated[int, Query(ge=1)] = 1,
):
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
