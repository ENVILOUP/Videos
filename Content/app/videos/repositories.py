import logging
from uuid import UUID
from typing import List, Optional

from asyncpg import Connection
from asyncpg.exceptions import ForeignKeyViolationError

from app.videos.models import Video, VideoTag


logger = logging.getLogger('uvicorn.error')


class VideosRespository:

    @staticmethod
    async def get_video_by_uuid(conn: Connection, uuid: UUID) -> Optional[Video]:
        query = """
            SELECT
                id,
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at
            FROM videos
            WHERE video_uuid = $1;
        """

        result = await conn.fetchrow(query, uuid)
        
        if not result:
            return None
        
        return Video(**result)
    
    @staticmethod
    async def get_videos_by_uuid_in(conn: Connection, uuids: List[UUID]) -> List[Video]:
        query = """
            SELECT
                id,
                video_uuid,
                yt_id,
                title,
                description,
                created_at,
                modified_at
            FROM videos
            WHERE video_uuid = ANY($1::uuid[]);
        """

        if not uuids:
            return []
        
        results = await conn.fetch(query, [str(uuid) for uuid in uuids])

        return [Video(**result) for result in results]
    
    @staticmethod
    async def add_video(conn: Connection, video: Video) -> Optional[UUID]:
        query = """
            INSERT INTO videos
                (video_uuid,
                 title,
                 description,
                 created_at,
                 modified_at)
            VALUES
	            ($1, $2, $3, $4, $5)
            ON CONFLICT (video_uuid) DO UPDATE 
            SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                modified_at = NOW()
            WHERE videos.video_uuid = EXCLUDED.video_uuid
            RETURNING videos.video_uuid;
        """

        args = (video.video_uuid,
                video.title,
                video.description,
                video.created_at,
                video.modified_at)

        result = await conn.fetchrow(query, *args)

        return result.get('video_uuid')


class VideosTagsRespository:

    @staticmethod
    async def get_tags_for_video(conn: Connection, video_uuid: UUID) -> List[VideoTag]:
        query = """
            SELECT
                id,
                video_uuid,
                tag,
                created_at,
                modified_at
            FROM videos_tags
            WHERE video_uuid = $1;
        """

        results = await conn.fetch(query, video_uuid)

        return [VideoTag(**result) for result in results]
    
    @staticmethod
    async def add_tags_to_video(conn: Connection, tags: List[VideoTag]) -> List[VideoTag]:
        query = """
            INSERT INTO videos_tags 
                (video_uuid, tag)
            VALUES
                ($1, $2)
            ON CONFLICT (video_uuid, tag) DO UPDATE 
                SET video_uuid = EXCLUDED.video_uuid,
                    tag = EXCLUDED.tag
            RETURNING videos_tags.video_uuid, videos_tags.tag;
        """

        if not tags:
            return []

        results = []

        try:
            async with conn.transaction() as t:
                for tag in tags:
                    result = await conn.fetchrow(query, tag.video_uuid, tag.tag)
                    if result:
                        results.append(result)
        except ForeignKeyViolationError:
            return []

        return [VideoTag(**result) for result in results]
