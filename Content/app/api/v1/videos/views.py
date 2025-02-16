import logging
from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from asyncpg import Connection

from app.api.v1.videos.models import VideoTag
from app.helpers.schemas import SuccessResponse
from app.helpers.statuses import StatusCodes
from app.helpers.exceptions import DeprecatedException, NotFoundException
from app.api.v1.videos.schemas import VideoCreationModel, VideoModel, VideoTagModel
from app.api.v1.videos.repositories import VideosRespository, VideosTagsRespository
from app.dependencies.postgresql import database_сonnection


logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/videos",
    tags=["videos"]
)


@router.get(
    path="/{uuid}",
    response_model=SuccessResponse[VideoModel]
)
async def get_video(
    uuid: UUID,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    video = await VideosRespository(db).get_video_by_uuid(uuid)

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
    db: Annotated[Connection, Depends(database_сonnection)],
    video_uuids: List[UUID],
):
    videos = await VideosRespository(db).get_videos_by_uuid_in(video_uuids)

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
    db: Annotated[Connection, Depends(database_сonnection)]
):
    raise DeprecatedException()  # TODO: refactor this method in DEV-46


@router.get(
    path='/{video_uuid}/tags/',
    response_model=SuccessResponse[List[str]]
)
async def get_tags_for_video(
    video_uuid: UUID,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    videos_tags = await VideosTagsRespository(db).get_tags_for_video(video_uuid)

    return {
        'status_code': StatusCodes.OK,
        'data': [videos_tag.tag for videos_tag in videos_tags]
    }


@router.post(
    path='/{video_uuid}/tags/',
    response_model=SuccessResponse[List[str]]
)
async def add_tags_to_video(
    video_uuid: UUID,
    tags: List[str],
    db: Annotated[Connection, Depends(database_сonnection)]
):
    videos_tags = [VideoTag(video_uuid=video_uuid, tag=tag)
                    for tag in tags]  # TODO refactor this in DEV-46
    videos_tags = await VideosTagsRespository(db).add_tags_to_video(videos_tags)

    return {
        'status_code': StatusCodes.TAGS_ADDED,
        'data': [videos_tag.tag for videos_tag in videos_tags]
    }
