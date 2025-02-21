from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

VIDEO_TAG_MAX_LENGTH = 32


@dataclass
class VideoTag:
    video_uuid: UUID
    tag: str
    created_at: datetime
    modified_at: datetime
