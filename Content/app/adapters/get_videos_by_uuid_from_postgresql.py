from typing import Optional
from uuid import UUID

from asyncpg import Connection
from app.core.entities.video import Video
from app.core.ports.get_video_by_uuid import GetVideoByUUIDPort


class GetVideosByUuidFromPostgreSQL(GetVideoByUUIDPort):
    """
    Implementation of GetVideoByUUIDPort for PostgreSQL.
    """

    def __init__(
        self,
        db: Connection
    ):
        self._db = db

    async def get_video_by_uuid(
        self,
        video_uuid: UUID
    ) -> Optional[Video]:
        query = """
            SELECT
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at,
                is_deleted
            FROM videos
            WHERE video_uuid = $1;
        """
        result = await self._db.fetchrow(query, video_uuid)

        if not result:
            return None

        return Video(
            video_uuid = result['video_uuid'],
            yt_id = result['yt_id'],
            title = result['title'],
            description = result['description'],
            created_at = result['created_at'],
            modified_at = result['modified_at'],
            is_deleted = result['is_deleted']
        )
