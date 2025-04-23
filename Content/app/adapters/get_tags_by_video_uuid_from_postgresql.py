
from typing import List
from uuid import UUID

from asyncpg import Connection
from app.core.entities.tag import Tag
from app.core.ports.get_tags_by_video_uuid import GetTagsByVideoUUIDPort


class GetTagsByVideoUUIDPortFromPostgreSQL(GetTagsByVideoUUIDPort):
    """
    Implementation of the GetTagsByVideoUUIDPort for PostgreSQL.
    This class retrieves video tags by video UUID from a PostgreSQL database.
    """

    def __init__(
        self,
        db: Connection
    ):
        self._db = db

    async def get_tags_by_video_uuid(self, video_uuid: UUID) -> List[Tag]:
        query = """
            SELECT
                tag,
                created_at,
                modified_at
            FROM videos_tags
            WHERE video_uuid = $1::uuid;
        """

        rows = await self._db.fetch(query, video_uuid)
        tags = [
            Tag(
                tag=row['tag'],
                created_at=row['created_at'],
                modified_at=row['modified_at']
            )
            for row in rows
        ]
        return tags
