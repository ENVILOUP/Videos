from typing import Optional
from uuid import UUID

from app.core.entities.video import Video
from app.core.ports.get_video_by_uuid import GetVideoByUUIDPort


class GetVideoByUUIDUseCase:
    """
    Use case for retrieving a video by its UUID.
    """

    def __init__(
        self,
        get_video_by_uuid: GetVideoByUUIDPort
    ):
        self._get_video_by_uuid_port = get_video_by_uuid

    async def execute(
        self,
        video_uuid: UUID
    ) -> Optional[Video]:
        if not isinstance(video_uuid, UUID):
            raise ValueError("Invalid UUID format")
        
        video = await self._get_video_by_uuid_port.get_video_by_uuid(video_uuid)

        return video
