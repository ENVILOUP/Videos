from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.core.entities.video import VideoStatus, VideoStatuses


class VideoStatusesRepository(ABC):

    @abstractmethod
    async def get_current_video_status(self, video_uuid: UUID) -> VideoStatus:
        """Get the current status of a video."""
        pass

    @abstractmethod
    async def get_video_status_history(self, video_uuid: UUID) -> List[VideoStatus]:
        """Get the status history of a video (new first)."""
        pass

    @abstractmethod
    async def add_video_status(self, video_uuid: UUID, video_status: VideoStatuses) -> VideoStatus:
        """Add a new status to the video status history."""
        pass
