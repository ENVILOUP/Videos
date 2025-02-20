from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

VIDEO_TITLE_MAX_LENGTH = 255
VIDEO_DESCRIPTION_MAX_LENGTH = 4095


@dataclass
class Video:
    video_uuid: UUID
    yt_id: Optional[str]
    title: str
    description: Optional[str]
    created_at: datetime
    modified_at: datetime
    is_deleted: bool
