import logging
from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.v1.videos.dependencies import get_tags_by_video_uuid_use_case, get_video_by_uuid_use_case, get_videos_by_uuid_list_use_case
from app.application.use_cases.get_tags_by_video_uuid import GetTagsByVideoUUIDUseCase
from app.application.use_cases.get_video_by_uuid import GetVideoByUUIDUseCase
from app.application.use_cases.get_videos_by_uuid_list import GetVideosByUUIDsListUseCase
from app.api.schemas import SuccessResponse
from app.api.statuses import StatusCodes
from app.api.exceptions import NotFoundException
from app.api.v1.videos.schemas import VideoCreationModel, VideoModel


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
    use_case: Annotated[GetVideoByUUIDUseCase, Depends(get_video_by_uuid_use_case)],
):
    video = await use_case.execute(uuid)

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


@router.post(
    path="/get-bulk/",
    response_model=SuccessResponse[List[VideoModel]]
)
async def get_videos_bulk(
    use_case: Annotated[GetVideosByUUIDsListUseCase, Depends(get_videos_by_uuid_list_use_case)],
    video_uuids: List[UUID],
):
    videos = await use_case.execute(video_uuids)

    return {
        'status_code': StatusCodes.OK,
        'data': [
            VideoModel(
                video_uuid=video.video_uuid,
                title=video.title,
                description=video.description,
                is_deleted=video.is_deleted,
                created_at=video.created_at,
                modified_at=video.modified_at
            )
            for video in videos
        ]
    }


@router.post(
    path="/",
    response_model=SuccessResponse[VideoModel]
)
async def create_video(
    video: VideoCreationModel
):
    raise NotImplementedError("Create video functionality is not implemented yet.")


@router.put(
    path="/{uuid}/",
    response_model=SuccessResponse[VideoModel]
)
async def update_video(
    uuid: UUID,
    video: VideoCreationModel
):
    raise NotImplementedError("Update video functionality is not implemented yet.")


@router.delete(
    path="/{uuid}/",
    response_model=SuccessResponse[VideoModel]
)
async def delete_video(
    uuid: UUID
):
    raise NotImplementedError("Delete video functionality is not implemented yet.")


@router.get(
    path="/{video_uuid}/tags/",
    response_model=SuccessResponse[List[str]]
)
async def get_tags_for_video(
    video_uuid: UUID,
    use_case: Annotated[GetTagsByVideoUUIDUseCase, Depends(get_tags_by_video_uuid_use_case)]
):
    videos_tags = await use_case.execute(video_uuid)

    return {
        'status_code': StatusCodes.OK,
        'data': [videos_tag.tag for videos_tag in videos_tags]
    }


@router.delete(
    path="/{video_uuid}/tags/",
    response_model=SuccessResponse[List[str]]
)
async def delete_video_tags(
    uuid: UUID
):
    raise NotImplementedError("Delete video tags functionality is not implemented yet.")


@router.post(
    path="/{video_uuid}/tags/",
    response_model=SuccessResponse[List[str]]
)
async def add_tags_to_video(
    video_uuid: UUID,
    tags: List[str]
):
    raise NotImplementedError("Add tags to video functionality is not implemented yet.")
