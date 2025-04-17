import logging
from typing import List, Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from asyncpg import Connection

from app.adapters.get_video_by_uuid.get_videos_by_uuid_from_postgresql import GetVideosByUuidFromPostgreSQL
from app.application.use_cases.get_video_by_uuid import GetVideoByUUIDUseCase
from app.helpers.schemas import SuccessResponse
from app.helpers.statuses import StatusCodes
from app.helpers.exceptions import ConflictException, NotFoundException
from app.api.v1.videos.schemas import VideoCreationModel, VideoModel, VideoModelWithTags
from app.api.v1.videos.repositories import VideosRespository, VideosTagsRespository
from app.dependencies.postgresql import database_сonnection


logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/videos"
)


@router.get(
    path="/{uuid}",
    response_model=SuccessResponse[VideoModel]
)
async def get_video(
    uuid: UUID,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    get_video_by_uuid = GetVideoByUUIDUseCase(
        get_video_by_uuid=GetVideosByUuidFromPostgreSQL(db)
    )

    video = await get_video_by_uuid.execute(uuid)

    if not video:
        raise NotFoundException(StatusCodes.NOT_FOUND)

    return {
        'status_code': StatusCodes.OK,
        'data': VideoModel(
            video_uuid=video.video_uuid,
            title=video.title,
            description=video.description,
            is_deleted=video.is_deleted,
            created_at=video.created_at,
            modified_at=video.modified_at
        )
    }


@router.get(
    path="/{uuid}/with-tags/",
    response_model=SuccessResponse[VideoModelWithTags]
)
async def get_video_with_tags(
    uuid: UUID,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    video = await VideosRespository(db).get_video_by_uuid(uuid)

    if not video:
        raise NotFoundException(StatusCodes.NOT_FOUND)

    tags = await VideosTagsRespository(db).get_tags_for_video(uuid)

    return {
        'status_code': StatusCodes.OK,
        'data': VideoModelWithTags(
            video_uuid=video.video_uuid,
            title=video.title,
            description=video.description,
            is_deleted=video.is_deleted,
            tags=[tag.tag for tag in tags]
        )
    }


@router.post(
    path="/get-bulk/",
    response_model=SuccessResponse[List[VideoModel]]
)
async def get_videos_bulk(
    db: Annotated[Connection, Depends(database_сonnection)],
    video_uuids: List[UUID],
):
    videos = await VideosRespository(db).get_videos_by_uuids_list(video_uuids)

    videos = [
        VideoModel(
            video_uuid=video.video_uuid,
            title=video.title,
            description=video.description,
            is_deleted=video.is_deleted
        )
        for video in videos
    ]
    return {
        'status_code': StatusCodes.OK,
        'data': videos
    }


@router.post(
    path="/",
    response_model=SuccessResponse[VideoModel]
)
async def create_video(
    video: VideoCreationModel,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    created_video = await VideosRespository(db).create_video(
        uuid=uuid4(),
        title=video.title,
        description=video.description
    )

    if not created_video:
        raise ConflictException(StatusCodes.VIDEO_CREATION_FAILED)
    
    return {
        'status_code': StatusCodes.VIDEO_CREATION_SUCCESS,
        'data': VideoModel(
            video_uuid=created_video.video_uuid,
            title=created_video.title,
            description=created_video.description,
            is_deleted=created_video.is_deleted
        )
    }


@router.put(
    path="/{uuid}/",
    response_model=SuccessResponse[VideoModel]
)
async def update_video(
    uuid: UUID,
    video: VideoCreationModel,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    updated_video = await VideosRespository(db).update_video(
        video_uuid=uuid,
        title=video.title,
        description=video.description
    )
    
    if not updated_video:
        raise NotFoundException(StatusCodes.NOT_FOUND)
    
    return {
        'status_code': StatusCodes.OK,
        'data': VideoModel(
            video_uuid=updated_video.video_uuid,
            title=updated_video.title,
            description=updated_video.description,
            is_deleted=updated_video.is_deleted
        )
    }


@router.delete(
    path="/{uuid}/",
    response_model=SuccessResponse[VideoModel]
)
async def delete_video(
    uuid: UUID,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    deleted_video = await VideosRespository(db).delete_video(uuid)

    if not deleted_video:
        raise NotFoundException(StatusCodes.NOT_FOUND)

    return {
        'status_code': StatusCodes.OK,
        'data': VideoModel(
            video_uuid=deleted_video.video_uuid,
            title=deleted_video.title,
            description=deleted_video.description,
            is_deleted=deleted_video.is_deleted
        )
    }


@router.get(
    path="/{video_uuid}/tags/",
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


@router.delete(
    path="/{video_uuid}/tags/",
    response_model=SuccessResponse[List[str]]
)
async def delete_video_tags(
    uuid: UUID,
    db: Annotated[Connection, Depends(database_сonnection)]
):
    videos_tags = await VideosTagsRespository(db).delete_video_tags(uuid)

    return {
        'status_code': StatusCodes.OK,
        'data': [videos_tag.tag for videos_tag in videos_tags]
    }


@router.post(
    path="/{video_uuid}/tags/",
    response_model=SuccessResponse[List[str]]
)
async def add_tags_to_video(
    video_uuid: UUID,
    tags: List[str],
    db: Annotated[Connection, Depends(database_сonnection)]
):
    videos_tags = await VideosTagsRespository(db).add_tags_to_video(video_uuid, tags)

    return {
        'status_code': StatusCodes.OK,
        'data': [videos_tag.tag for videos_tag in videos_tags]
    }
