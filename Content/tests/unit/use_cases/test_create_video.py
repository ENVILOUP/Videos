

from datetime import datetime
from typing import Callable, Dict, List, Optional
from uuid import UUID

import pytest
from app.application.use_cases.create_video import CreateVideoUseCase
from app.core.entities.video import Video, VideoStatus, VideoStatuses
from app.core.ports.video_statuses_repository import VideoStatusesRepository
from app.core.ports.videos_queue import TaskId, VideosQueue
from app.core.ports.videos_repository import VideosRepository


class InMemoryVideosRepository(VideosRepository):
    def __init__(self, videos: List[Video]):
        self.videos = videos

    async def create_video(self, video: Video) -> Optional[Video]:
        # Simulate video creation
        for existing_video in self.videos:
            # Check conflict with existing video UUID
            if existing_video.video_uuid == video.video_uuid:
                return None
        self.videos.append(video)
        return video


class InMemoryVideoStatusesRepository(VideoStatusesRepository):
    def __init__(self, statuses: Dict[UUID, VideoStatus], get_time: Callable[[], datetime] = datetime.now):
        self.statuses = statuses
        self.get_time = get_time

    async def add_video_status(self, video_uuid: UUID, video_status: VideoStatuses) -> VideoStatus:
        new_status = VideoStatus(
            status=video_status,
            created_at=self.get_time()
        )
        self.statuses[video_uuid] = new_status
        return new_status

    async def get_current_video_status(self, video_uuid: UUID) -> VideoStatus:
        raise NotImplementedError

    async def get_video_status_history(self, video_uuid: UUID) -> List[VideoStatus]:
        raise NotImplementedError


class InMemoryVideosQueue(VideosQueue):
    def __init__(self, queue: List[Dict[str, str]]):
        self.queue = queue

    async def add_video_to_process(self, video_uuid: UUID, thumbnail_raw_url: str, video_raw_url: str) -> str:
        task_id = str(len(self.queue) + 1)
        self.queue.append({
            "video_uuid": str(video_uuid),
            "thumbnail_raw_url": thumbnail_raw_url,
            "video_raw_url": video_raw_url,
            "task_id": task_id
        })
        return task_id


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
