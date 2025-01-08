import logging
from typing import List, Optional, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from asyncpg import Connection

from app.dependencies import get_connection
from app.videos.models import Video, VideoTag
from app.videos.repositories import VideosRespository, VideosTagsRespository


logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("/{uuid}")
async def get_video(uuid: UUID, db: Annotated[Connection, Depends(get_connection)]) -> Optional[Video]:
    async with db as connection:
        video = await VideosRespository.get_video_by_uuid(connection, uuid)
        return video


@router.get("/")
async def get_videos_list(videos_uuids: List[UUID], db: Annotated[Connection, Depends(get_connection)]) -> List[Video]:
    async with db as conn:
        videos = await VideosRespository.get_videos_by_uuid_in(conn, videos_uuids)
        return videos


@router.post("/")
async def update_video(video: Video, db: Annotated[Connection, Depends(get_connection)]) -> Optional[UUID]:
    async with db as conn:
        uuid = await VideosRespository.add_video(conn, video)
        return uuid


@router.get('/{uuid}/tags/')
async def get_tags_for_video(uuid: UUID, db: Annotated[Connection, Depends(get_connection)]) -> List[VideoTag]:
    async with db as conn:
        videos_tags = await VideosTagsRespository.get_tags_for_video(conn, uuid)
        return videos_tags


@router.post('/{uuid}/tags/')
async def add_tags_for_video(uuid: UUID, tags: List[str], db: Annotated[Connection, Depends(get_connection)]) -> List[VideoTag]:
    async with db as conn:
        videos_tags = [VideoTag(video_uuid=uuid, tag=tag) for tag in tags]
        videos_tags = await VideosTagsRespository.add_tags_to_video(conn, videos_tags)
        return videos_tags
