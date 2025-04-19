from typing import List, Optional
import datetime
from uuid import UUID
from pydantic import BaseModel, computed_field

from app.infrastructure.config.config import config


class VideoModel(BaseModel):
    video_uuid: UUID
    title: str
    is_deleted: bool
    description: Optional[str] = None
    created_at: datetime.datetime
    modified_at: datetime.datetime

    @computed_field
    @property
    def video_url(self) -> str:
        return f'{config.cdn_base_url}/videos/{self.video_uuid}/master.m3u8'

    @computed_field
    @property
    def thumbnail_url(self) -> str:
        return f'{config.cdn_base_url}/thumbnails/{self.video_uuid}/default.webp'
    
    @computed_field
    @property
    def publication_date(self) -> datetime.datetime:
        return self.created_at


class VideoModelWithTags(VideoModel):
    tags: List[str]


class VideoCreationModel(BaseModel):
    title: str
    description: Optional[str] = None


class VideoTagModel(BaseModel):
    tag: str
