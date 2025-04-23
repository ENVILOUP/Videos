

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.core.entities.video import Video


class GetVideosListByUUIDsPort(ABC):

    @abstractmethod
    async def get_videos(self, video_uuids: List[UUID]) -> List[Video]:
        """
        Retrieves a list of videos based on their UUIDs.
        """
        raise NotImplementedError
