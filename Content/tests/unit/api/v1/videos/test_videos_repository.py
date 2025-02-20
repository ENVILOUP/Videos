from unittest.mock import call, patch
from uuid import UUID
from datetime import datetime
import pytest
from app.models.videos import Video
from app.api.v1.videos.repositories import VideosRespository
from app.helpers.sql import clean_query


class TestVideosRespository:

    @pytest.mark.asyncio
    async def test_valid_get_video_by_uuid(self, connection):
        connection.fetchrow.return_value = {
            'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
            'yt_id': 'test',
            'title': 'test',
            'description': 'test',
            'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
            'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
        }
        video_repository = VideosRespository(connection)

        video = await video_repository.get_video_by_uuid(UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'))

        connection.fetchrow.assert_called_once_with(
            clean_query("""
                SELECT
                    video_uuid,
                    yt_id,
                    title,
                    description,
                    created_at,
                    modified_at
                FROM videos
                WHERE video_uuid = $1;
            """),
            UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38')
        )

        assert video == Video(
            video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
            yt_id='test',
            title='test',
            description='test',
            created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
            modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
        )

    @pytest.mark.asyncio
    async def test_not_valid_value_get_video_by_uuid(self, connection):
        video_repository = VideosRespository(connection)

        with pytest.raises(AssertionError):
            await video_repository.get_video_by_uuid('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38')

        connection.fetchrow.assert_not_called()

    @pytest.mark.asyncio
    async def test_valid_get_videos_by_uuids_list(self, connection):
        connection.fetch.return_value = [
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'yt_id': None,
                'title': 'test1',
                'description': 'test1',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            },
            {
                'video_uuid': UUID('4686f6cd-fb8b-44fd-8ac6-8d04a6f8ce39'),
                'yt_id': 'test2',
                'title': 'test2',
                'description': 'test2',
                'created_at': datetime.fromisoformat('2025-02-13T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-13T00:00:00')
            }
        ]
        video_repository = VideosRespository(connection)

        videos = await video_repository.get_videos_by_uuids_list([
            UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
            UUID('4686f6cd-fb8b-44fd-8ac6-8d04a6f8ce39')
        ])

        connection.fetch.assert_called_once_with(
            clean_query("""
                SELECT
                    video_uuid,
                    yt_id,
                    title,
                    description,
                    created_at,
                    modified_at
                FROM videos
                WHERE video_uuid = ANY($1::uuid[]);
            """),
            [
                '3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38',
                '4686f6cd-fb8b-44fd-8ac6-8d04a6f8ce39'
            ]
        )

        assert videos == [
            Video(
                video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                yt_id=None,
                title='test1',
                description='test1',
                created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
            ),
            Video(
                video_uuid=UUID('4686f6cd-fb8b-44fd-8ac6-8d04a6f8ce39'),
                yt_id='test2',
                title='test2',
                description='test2',
                created_at=datetime.fromisoformat('2025-02-13T00:00:00'),
                modified_at=datetime.fromisoformat('2025-02-13T00:00:00')
            )
        ]

    @pytest.mark.asyncio
    async def test_empty_get_videos_by_uuids_list(self, connection):
        connection.fetch.return_value = []
        video_repository = VideosRespository(connection)

        videos = await video_repository.get_videos_by_uuids_list([])

        connection.fetch.assert_not_called()

        assert videos == []

    @pytest.mark.asyncio
    async def test_invalid_get_videos_by_uuids_list(self, connection):
        video_repository = VideosRespository(connection)

        with pytest.raises(AssertionError):
            await video_repository.get_videos_by_uuids_list([
                '3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38',
                '4686f6cd-fb8b-44fd-8ac6-8d04a6f8ce39'
            ])

        connection.fetch.assert_not_called()

    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_create_video(self, connection):
        connection.fetchrow.side_effect = [
            {
                'video_uuid': UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
                'yt_id': 'test',
                'title': 'test',
                'description': 'test',
                'created_at': datetime.fromisoformat('2025-02-12T00:00:00'),
                'modified_at': datetime.fromisoformat('2025-02-12T00:00:00')
            },
            None  # Conflict
        ]
        video_repository = VideosRespository(connection)

        video = Video(
            video_uuid=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38'),
            yt_id='test',
            title='test',
            description='test',
            created_at=datetime.fromisoformat('2025-02-12T00:00:00'),
            modified_at=datetime.fromisoformat('2025-02-12T00:00:00')
        )

        with patch('uuid.uuid4', return_value=UUID('3686f6cd-fb8b-44fd-8ac6-8d04a6f8ce38')):
            created_video1 = await video_repository.create_video(title=video.title, description=video.description)
            created_video2 = await video_repository.create_video(title=video.title, description=video.description)

        connection.fetchrow.assert_has_calls([
            call(
                clean_query("""
                    INSERT INTO videos(
                        video_uuid,
                        title,
                        description,
                        created_at,
                        modified_at
                    )
                    VALUES
                        ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (video_uuid) DO NOTHING
                    RETURNING
                        video_uuid,
                        yt_id,
                        title,
                        description,
                        created_at,
                        modified_at;
                """),
                video.video_uuid,
                video.yt_id,
                video.title,
                video.description,
                video.created_at,
                video.modified_at
            ),
            call(
                clean_query("""
                    INSERT INTO videos(
                        video_uuid,
                        title,
                        description,
                        created_at,
                        modified_at
                    )
                    VALUES
                        ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (video_uuid) DO NOTHING
                    RETURNING
                        video_uuid,
                        yt_id,
                        title,
                        description,
                        created_at,
                        modified_at;
                """),
                video.video_uuid,
                video.yt_id,
                video.title,
                video.description,
                video.created_at,
                video.modified_at
            )
        ])

        assert created_video1 == video
        assert created_video2 is None
