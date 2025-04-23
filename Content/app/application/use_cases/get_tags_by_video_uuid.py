

from typing import List
from uuid import UUID
from app.core.entities.tag import Tag
from app.core.ports.get_tags_by_video_uuid import GetTagsByVideoUUIDPort


class GetTagsByVideoUUIDUseCase:
    """Use case for retrieving video tags by video UUID."""
    def __init__(self, get_video_tags_by_video_uuid: GetTagsByVideoUUIDPort):
        self._get_video_tags_by_video_uuid_port = get_video_tags_by_video_uuid

    async def execute(self, video_uuid: UUID) -> List[Tag]:
        if not isinstance(video_uuid, UUID):
            raise ValueError("Invalid UUID format")

        tags = await self._get_video_tags_by_video_uuid_port.get_tags_by_video_uuid(video_uuid)

        return tags