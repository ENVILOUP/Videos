from typing import Dict, List
from uuid import UUID
from app.core.ports.videos_queue import VideosQueue


class InMemoryVideosQueue(VideosQueue):
    def __init__(self, queue: List[Dict[str, str]]):
        self.queue = queue

    async def add_video_to_process(self, video_uuid: UUID, thumbnail_raw_url: str, video_raw_url: str) -> str:
        task_id = str(len(self.queue) + 1)
        self.queue.append({
            "video_uuid": str(video_uuid),
            "thumbnail_raw_url": thumbnail_raw_url,
            "video_raw_url": video_raw_url,
            "task_id": task_id
        })
        return task_id
