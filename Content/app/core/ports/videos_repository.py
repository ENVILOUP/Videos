from abc import ABC, abstractmethod
from typing import Optional

from app.core.entities.video import Video


class VideosRepository(ABC):

    @abstractmethod
    async def create_video(self, video: Video) -> Optional[Video]:
        pass
