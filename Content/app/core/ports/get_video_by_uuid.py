from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.core.entities.video import Video


class GetVideoByUUIDPort(ABC):
    """
    Port for retrieving a video by its UUID.
    """

    @abstractmethod
    async def get_video_by_uuid(
        self,
        video_uuid: UUID
    ) -> Optional[Video]:
        """
        Retrieve a video by its UUID.
        """
        raise NotImplementedError
