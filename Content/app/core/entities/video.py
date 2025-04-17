from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Video:
    video_uuid: UUID
    yt_id: Optional[str]
    title: str
    description: Optional[str]
    created_at: datetime
    modified_at: datetime
    is_deleted: bool
