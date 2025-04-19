

from typing import Annotated
from asyncpg import Connection
from fastapi import Depends
from app.adapters.get_tags_by_video_uuid.get_tags_by_video_uuid_from_postgresql import GetTagsByVideoUUIDPortFromPostgreSQL
from app.adapters.get_video_by_uuid.get_videos_by_uuid_from_postgresql import GetVideosByUuidFromPostgreSQL
from app.application.use_cases.get_tags_by_video_uuid import GetTagsByVideoUUIDUseCase
from app.application.use_cases.get_video_by_uuid import GetVideoByUUIDUseCase
from app.dependencies.postgresql import database_сonnection


async def get_video_by_uuid_use_case(
    database: Annotated[Connection, Depends(database_сonnection)],
) -> GetVideoByUUIDUseCase:
    """
    Dependency to get the GetVideoByUUIDUseCase instance.
    """
    return GetVideoByUUIDUseCase(
        get_video_by_uuid=GetVideosByUuidFromPostgreSQL(database)
    )

async def get_tags_by_video_uuid_use_case(
    database: Annotated[Connection, Depends(database_сonnection)],
) -> GetTagsByVideoUUIDUseCase:
    """
    Dependency to get the GetTagsByVideoUUIDUseCase instance.
    """
    return GetTagsByVideoUUIDUseCase(
        get_video_tags_by_video_uuid=GetTagsByVideoUUIDPortFromPostgreSQL(database)
    )
