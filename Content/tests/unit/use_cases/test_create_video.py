

from datetime import datetime
from uuid import UUID

import pytest
from app.application.use_cases.create_video import CreateVideoUseCase
from app.core.entities.video import Video, VideoStatus, VideoStatuses
from tests.unit.mocks.video_statuses_repository import InMemoryVideoStatusesRepository
from tests.unit.mocks.videos_queue import InMemoryVideosQueue
from tests.unit.mocks.videos_repository import InMemoryVideosRepository


class TestCreateVideoUseCase:

    @pytest.mark.asyncio
    async def test_create_video_use_case(self):
        videos_repository = InMemoryVideosRepository(videos=[])
        video_statuses_repository = InMemoryVideoStatusesRepository(
            statuses={}, get_time=lambda: datetime(2025, 1, 1, 1))
        videos_queue = InMemoryVideosQueue(queue=[])
        create_video_use_case = CreateVideoUseCase(
            videos_repository=videos_repository,
            video_statuses_repository=video_statuses_repository,
            videos_queue=videos_queue
        )

        video = Video(
            video_uuid=UUID("12345678-1234-5678-1234-567812345678"),
            title="Test Video",
            description="This is a test video.",
            created_at=datetime(2025, 1, 1),
            modified_at=datetime(2025, 1, 1),
            is_deleted=False
        )
        result = await create_video_use_case.execute(
            video=video,
            thumbnail_raw_url="http://example.com/thumbnail.jpg",
            video_raw_url="http://example.com/video.mp4"
        )

        assert result == video
        assert videos_repository.videos == [video]
        assert videos_queue.queue == [{
            "video_uuid": str(video.video_uuid),
            "thumbnail_raw_url": "http://example.com/thumbnail.jpg",
            "video_raw_url": "http://example.com/video.mp4",
            "task_id": "1"
        }]
        assert video_statuses_repository.statuses == {
            video.video_uuid: VideoStatus(
                status=VideoStatuses.PENDING,
                created_at=datetime(2025, 1, 1, 1)
            )
        }

    @pytest.mark.asyncio
    async def test_create_video_use_case_conflict(self):
        video_uuid = UUID("12345678-1234-5678-1234-567812345678")
        existing_video = Video(
            video_uuid=video_uuid,
            title="Existing Video",
            description="This is an existing video.",
            created_at=datetime(2025, 1, 1),
            modified_at=datetime(2025, 1, 1),
            is_deleted=False
        )
        videos_repository = InMemoryVideosRepository(videos=[existing_video])
        video_statuses_repository = InMemoryVideoStatusesRepository(
            statuses={},
            get_time=lambda: datetime(2025, 1, 1, 1)
        )
        videos_queue = InMemoryVideosQueue(queue=[])
        create_video_use_case = CreateVideoUseCase(
            videos_repository=videos_repository,
            video_statuses_repository=video_statuses_repository,
            videos_queue=videos_queue
        )
        video = Video(
            video_uuid=video_uuid,
            title="Test Video",
            description="This is a test video.",
            created_at=datetime(2025, 1, 1),
            modified_at=datetime(2025, 1, 1),
            is_deleted=False
        )

        with pytest.raises(ValueError, match="Video creation failed"):
            await create_video_use_case.execute(
                video=video,
                thumbnail_raw_url="http://example.com/thumbnail.jpg",
                video_raw_url="http://example.com/video.mp4"
            )

        assert videos_repository.videos == [existing_video]
        assert videos_queue.queue == []
        assert video_statuses_repository.statuses == {}
