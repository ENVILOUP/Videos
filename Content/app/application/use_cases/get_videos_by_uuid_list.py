

from typing import List
from uuid import UUID

from app.core.entities.video import Video
from app.core.ports.get_videos_list_by_uuids import GetVideosListByUUIDsPort


class GetVideosByUUIDsListUseCase:
    def __init__(self, get_videos_list_by_uuids_port: GetVideosListByUUIDsPort):
        self._get_videos_list_by_uuids_port = get_videos_list_by_uuids_port

    async def execute(self, video_uuids: List[UUID]) -> List[Video]:
        if not all(isinstance(uuid, UUID) for uuid in video_uuids):
            raise ValueError("Invalid UUID format")

        videos = await self._get_videos_list_by_uuids_port.get_videos(video_uuids)

        return videos