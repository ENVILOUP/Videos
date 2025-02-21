import logging
from uuid import UUID, uuid4
from typing import List, Optional

from asyncpg import Connection
from asyncpg.exceptions import ForeignKeyViolationError

from app.models.videos import Video
from app.models.videos_tags import VideoTag
from app.helpers.sql import clean_query


logger = logging.getLogger('uvicorn.error')


class VideosRespository:

    def __init__(self, conn: Connection):
        self._conn = conn

    async def get_video_by_uuid(self, uuid: UUID) -> Optional[Video]:
        assert isinstance(uuid, UUID), 'uuid must be an instance of UUID'

        query = clean_query("""
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
        """)

        result = await self._conn.fetchrow(query, uuid)

        if not result:
            return None

        return Video(
            video_uuid=result['video_uuid'],
            yt_id=result['yt_id'],
            title=result['title'],
            description=result['description'],
            created_at=result['created_at'],
            modified_at=result['modified_at'],
            is_deleted=result['is_deleted']
        )

    async def get_videos_by_uuids_list(self, uuids: List[UUID]) -> List[Video]:
        query = clean_query("""
            SELECT
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at,
                is_deleted
            FROM videos
            WHERE video_uuid = ANY($1::uuid[]);
        """)

        if not uuids:
            return []

        assert all(isinstance(uuid, UUID)
                   for uuid in uuids), 'uuids must be a list of UUID instances'

        results = await self._conn.fetch(
            query,
            [str(uuid) for uuid in uuids]
        )

        return [
            Video(
                video_uuid=result['video_uuid'],
                yt_id=result['yt_id'],
                title=result['title'],
                description=result['description'],
                created_at=result['created_at'],
                modified_at=result['modified_at'],
                is_deleted=result['is_deleted']
            )
            for result in results
        ]

    async def create_video(
        self,
        uuid: UUID,
        title: str,
        description: str
    ) -> Optional[Video]:
        query = clean_query("""
            INSERT INTO videos(
                video_uuid,
                title,
                description
            )
            VALUES
                ($1, $2, $3)
            ON CONFLICT (video_uuid) DO NOTHING
            RETURNING
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at,
                is_deleted;
        """)

        args = (uuid,
                title,
                description)

        result = await self._conn.fetchrow(query, *args)

        if not result:
            return None

        return Video(
            video_uuid=result['video_uuid'],
            yt_id=result['yt_id'],
            title=result['title'],
            description=result['description'],
            created_at=result['created_at'],
            modified_at=result['modified_at'],
            is_deleted=result['is_deleted']
        )

    async def update_video(
        self,
        video_uuid: UUID,
        title: str,
        description: str
    ) -> Optional[Video]:
        query = clean_query("""
            UPDATE videos
            SET
                title = $2,
                description = $3,
                modified_at = NOW()
            WHERE video_uuid = $1
            RETURNING
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at,
                is_deleted;
        """)

        result = await self._conn.fetchrow(query, video_uuid, title, description)

        if not result:
            return None

        return Video(
            video_uuid=result['video_uuid'],
            yt_id=result['yt_id'],
            title=result['title'],
            description=result['description'],
            created_at=result['created_at'],
            modified_at=result['modified_at'],
            is_deleted=result['is_deleted']
        )

    async def delete_video(self, video_uuid: UUID) -> Optional[Video]:
        query = clean_query("""
            UPDATE videos
            SET
                is_deleted = TRUE,
                modified_at = NOW()
            WHERE video_uuid = $1
            RETURNING
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at,
                is_deleted;
        """)

        result = await self._conn.fetchrow(query, video_uuid)

        if not result:
            return None

        return Video(
            video_uuid=result['video_uuid'],
            yt_id=result['yt_id'],
            title=result['title'],
            description=result['description'],
            created_at=result['created_at'],
            modified_at=result['modified_at'],
            is_deleted=result['is_deleted']
        )


class VideosTagsRespository:

    def __init__(self, conn: Connection):
        self._conn = conn

    async def get_tags_for_video(self, video_uuid: UUID) -> List[VideoTag]:
        query = clean_query("""
            SELECT
                video_uuid,
                tag,
                created_at,
                modified_at
            FROM videos_tags
            WHERE video_uuid = $1;
        """)

        results = await self._conn.fetch(query, video_uuid)

        return [
            VideoTag(
                video_uuid=result['video_uuid'],
                tag=result['tag'],
                created_at=result['created_at'],
                modified_at=result['modified_at']
            )
            for result in results
        ]

    async def add_tags_to_video(self, video_uuid: UUID, tags: List[str]) -> List[VideoTag]:
        query = clean_query("""
            INSERT INTO videos_tags(
                video_uuid,
                tag
            )
            VALUES
                ($1, $2)
            ON CONFLICT DO NOTHING
            RETURNING
                video_uuid,
                tag,
                created_at,
                modified_at;
        """)

        if not tags:
            return []

        results = []

        try:
            async with self._conn.transaction() as t:
                for tag in tags:
                    result = await self._conn.fetchrow(query, video_uuid, tag)
                    if result:
                        results.append(result)
        except ForeignKeyViolationError:
            return []

        return [
            VideoTag(
                video_uuid=result['video_uuid'],
                tag=result['tag'],
                created_at=result['created_at'],
                modified_at=result['modified_at']
            )
            for result in results
        ]

    async def delete_video_tags(self, video_uuid: UUID) -> List[VideoTag]:
        query = clean_query("""
            DELETE FROM videos_tags
            WHERE video_uuid = $1
            RETURNING
                video_uuid,
                tag,
                created_at,
                modified_at;
        """)

        results = await self._conn.fetch(query, video_uuid)

        return [
            VideoTag(
                video_uuid=result['video_uuid'],
                tag=result['tag'],
                created_at=result['created_at'],
                modified_at=result['modified_at']
            )
            for result in results
        ]
