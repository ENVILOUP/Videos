
from typing import List
from uuid import UUID

from asyncpg import Connection
from app.core.entities.video import Video
from app.core.ports.get_videos_list_by_uuids import GetVideosListByUUIDsPort


class GetVideosListByUUIDsFromPostgreSQL(GetVideosListByUUIDsPort):

    def __init__(
        self,
        db: Connection
    ):
        self._db = db

    async def get_videos(self, video_uuids: List[UUID]) -> List[Video]:
        query = """
            select
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at,
                is_deleted
            from videos
            where video_uuid = ANY($1);
        """

        rows = await self._db.fetch(query, video_uuids)
        videos = [
            Video(
                video_uuid=row['video_uuid'],
                yt_id=row['yt_id'],
                title=row['title'],
                description=row['description'],
                created_at=row['created_at'],
                modified_at=row['modified_at'],
                is_deleted=row['is_deleted']
            )
            for row in rows
        ]
        return videos
