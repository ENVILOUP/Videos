from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.core.entities.tag import Tag


class GetTagsByVideoUUIDPort(ABC):
    """Port for retrieving video tags by video UUID."""

    @abstractmethod
    async def get_tags_by_video_uuid(self, video_uuid: UUID) -> List[Tag]:
        """Get tags by video UUID."""
        raise NotImplementedError

