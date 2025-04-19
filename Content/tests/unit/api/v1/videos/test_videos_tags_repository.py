from datetime import datetime
from unittest.mock import call
from uuid import UUID
from asyncpg import ForeignKeyViolationError
import pytest

from app.api.v1.videos.repositories import VideosTagsRespository
from app.helpers.sql import clean_query
from app.models.videos_tags import VideoTag


@pytest.skip("This should not be tested in unit tests", allow_module_level=True)
class TestVideosTagsRepository:

    @pytest.mark.asyncio
    async def test_get_tags_for_video(self, connection):
        connection.fetch.return_value = [
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag': 'tag1',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            },
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag': 'tag2',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            }
        ]
        tags_repository = VideosTagsRespository(connection)

        tags = await tags_repository.get_tags_for_video(UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'))

        connection.fetch.assert_called_once_with(
            clean_query("""
                SELECT
                    video_uuid,
                    tag,
                    created_at,
                    modified_at
                FROM videos_tags
                WHERE video_uuid = $1;
            """),
            UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38')
        )

        assert tags == [
            VideoTag(
                video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                tag='tag1',
                created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
            ),
            VideoTag(
                video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                tag='tag2',
                created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
            )
        ]

    @pytest.mark.asyncio
    async def test_add_tags_to_video(self, connection):
        connection.fetchrow.side_effect = [
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag': 'tag1',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            },
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag': 'tag2',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            }
        ]
        tags_repository = VideosTagsRespository(connection)

        tags = await tags_repository.add_tags_to_video(
            UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
            ['tag1', 'tag2']
        )

        connection.fetchrow.assert_has_calls([
            call(
                clean_query("""
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
                """),
                UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag1'
            ),
            call(
                clean_query("""
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
                """),
                UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag2'
            )
        ])

        assert tags == [
            VideoTag(
                video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                tag='tag1',
                created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
            ),
            VideoTag(
                video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                tag='tag2',
                created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
            )
        ]

    @pytest.mark.asyncio
    async def test_add_tags_to_video_empty_tags(self, connection):
        tags_repository = VideosTagsRespository(connection)

        tags = await tags_repository.add_tags_to_video(
            UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
            []
        )

        assert tags == []

    @pytest.mark.asyncio
    async def test_add_tags_to_video_no_tags(self, connection):
        connection.fetchrow.side_effect = ForeignKeyViolationError()
        tags_repository = VideosTagsRespository(connection)

        tags = await tags_repository.add_tags_to_video(
            UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
            ['tag1', 'tag2']
        )

        assert tags == []

    @pytest.mark.asyncio
    async def test_delete_video_tags(self, connection):
        connection.fetch.return_value = [
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag': 'tag1',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            },
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'tag': 'tag2',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            }
        ]
        tags_repository = VideosTagsRespository(connection)

        deleted_tags = await tags_repository.delete_video_tags(UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'))

        connection.fetch.assert_called_once_with(
            clean_query("""
                DELETE FROM videos_tags
                WHERE video_uuid = $1
                RETURNING
                    video_uuid,
                    tag,
                    created_at,
                    modified_at;
            """),
            UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38')
        )

        assert deleted_tags == [
            VideoTag(
                video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                tag='tag1',
                created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
            ),
            VideoTag(
                video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                tag='tag2',
                created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
            )
        ]
