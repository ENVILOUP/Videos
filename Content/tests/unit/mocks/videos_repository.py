from typing import List, Optional
from app.core.entities.video import Video
from app.core.ports.videos_repository import VideosRepository


class InMemoryVideosRepository(VideosRepository):
    def __init__(self, videos: List[Video]):
        self.videos = videos

    async def create_video(self, video: Video) -> Optional[Video]:
        # Simulate video creation
        for existing_video in self.videos:
            # Check conflict with existing video UUID
            if existing_video.video_uuid == video.video_uuid:
                return None
        self.videos.append(video)
        return video
