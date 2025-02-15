import logging
from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from asyncpg import Connection

from app.videos.models import VideoTag
from app.helpers.schemas import SuccessResponse
from app.helpers.statuses import StatusCodes
from app.helpers.exceptions import DeprecatedException, NotFoundException
from app.videos.schemas import VideoCreationModel, VideoModel, VideoTagModel
from app.dependencies import get_connection
from app.videos.repositories import VideosRespository, VideosTagsRespository


logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get(
    path="/{uuid}",
    response_model=SuccessResponse[VideoModel]
)
async def get_video(
    uuid: UUID,
    db: Annotated[Connection, Depends(get_connection)]
):
    async with db as connection:
        video = await VideosRespository.get_video_by_uuid(connection, uuid)

    if not video:
        raise NotFoundException(StatusCodes.NOT_FOUND)

    video = video.model_dump()  # TODO: refactor database model in DEV-46
    return {
        'status_code': StatusCodes.OK,
        'data': VideoModel(**video)
    }


@router.post(
    path="/get-bulk/",
    response_model=SuccessResponse[List[VideoModel]]
)
async def get_videos_bulk(
    db: Annotated[Connection, Depends(get_connection)],
    video_uuids: List[UUID],
):
    async with db as conn:
        videos = await VideosRespository.get_videos_by_uuid_in(conn, video_uuids)

    # TODO: refactor database model in DEV-46
    videos = [video.model_dump() for video in videos]
    return {
        'status_code': StatusCodes.OK,
        'data': [VideoModel(**video) for video in videos]
    }


@router.post(
    path="/",
    response_model=SuccessResponse[VideoModel]
)
async def update_video(
    video: VideoCreationModel,
    db: Annotated[Connection, Depends(get_connection)]
):
    raise DeprecatedException()  # TODO: refactor this method in DEV-46


@router.get(
    path='/{video_uuid}/tags/',
    response_model=SuccessResponse[List[VideoTagModel]]
)
async def get_tags_for_video(
    video_uuid: UUID,
    db: Annotated[Connection, Depends(get_connection)]
):
    async with db as conn:
        videos_tags = await VideosTagsRespository.get_tags_for_video(conn, video_uuid)
        
    return {
        'status_code': StatusCodes.TAGS_ADDED,
        'data': [VideoTagModel(**videos_tag.model_dump()) for videos_tag in videos_tags]
    }


@router.post(
    path='/{video_uuid}/tags/',
    response_model=SuccessResponse[List[VideoTagModel]]
)
async def add_tags_to_video(
    video_uuid: UUID,
    tags: List[str],
    db: Annotated[Connection, Depends(get_connection)]
):
    async with db as conn:
        videos_tags = [VideoTag(video_uuid=video_uuid, tag=tag) for tag in tags]  # TODO refactor this in DEV-46
        videos_tags = await VideosTagsRespository.add_tags_to_video(conn, videos_tags)
    
    return {
        'status_code': StatusCodes.TAGS_ADDED,
        'data': [VideoTagModel(**videos_tag.model_dump()) for videos_tag in videos_tags]
    }
