from abc import ABC, abstractmethod
from typing import TypeAlias
from uuid import UUID


TaskId: TypeAlias = str


class VideosQueue(ABC):

    @abstractmethod
    async def add_video_to_process(
        self,
        video_uuid: UUID,
        thumbnail_raw_url: str,
        video_raw_url: str
    ) -> TaskId:
        """Add a video to the processing queue."""
        pass

    