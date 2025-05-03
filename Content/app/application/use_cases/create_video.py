from typing import final
from app.core.entities.video import Video, VideoStatuses
from app.core.ports.video_statuses_repository import VideoStatusesRepository
from app.core.ports.videos_queue import VideosQueue
from app.core.ports.videos_repository import VideosRepository


@final
class CreateVideoUseCase:
    """Create a video and add it to the processing queue."""

    def __init__(
        self,
        videos_repository: VideosRepository,
        video_statuses_repository: VideoStatusesRepository,
        videos_queue: VideosQueue
    ) -> None:
        self._videos_repository = videos_repository
        self._video_statuses_repository = video_statuses_repository
        self._videos_queue = videos_queue

    async def execute(
        self,
        video: Video,
        thumbnail_raw_url: str,
        video_raw_url: str
    ) -> Video:
        created_video = await self._videos_repository.create_video(video)

        if created_video is None:
            raise ValueError("Video creation failed")

        video_status = await self._video_statuses_repository.add_video_status(
            video_uuid=created_video.video_uuid,
            video_status=VideoStatuses.PENDING
        )

        await self._videos_queue.add_video_to_process(
            video_uuid=created_video.video_uuid,
            thumbnail_raw_url=thumbnail_raw_url,
            video_raw_url=video_raw_url
        )

        return created_video
