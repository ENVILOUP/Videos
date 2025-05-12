from datetime import datetime
from typing import Callable, Dict, List
from uuid import UUID
from app.core.entities.video import VideoStatus, VideoStatuses
from app.core.ports.video_statuses_repository import VideoStatusesRepository


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
