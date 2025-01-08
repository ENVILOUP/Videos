from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, computed_field, field_validator

from app.config import config

VIDEO_TITLE_MAX_LENGTH = 255
VIDEO_DESCRIPTION_MAX_LENGTH = 4095
VIDEO_TAG_MAX_LENGTH = 255


class Video(BaseModel):
    id: Optional[int] = None
    video_uuid: UUID
    yt_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    modified_at: Optional[datetime] = datetime.now()

    @computed_field
    @property
    def video_url(self) -> str:
        return f'{config.cdn_base_url}/videos/{self.video_uuid}/master.m3u8'

    @computed_field
    @property
    def thumbnail_url(self) -> str:
        return f'{config.cdn_base_url}/thumbnails/{self.video_uuid}/default.webp'

    @field_validator('title')
    def title_max_len(cls, value):
        if len(value) > VIDEO_TITLE_MAX_LENGTH:
            raise ValueError(f"Title must be at most {VIDEO_TITLE_MAX_LENGTH} characters")
        return value
    
    @field_validator('description')
    def description_max_len(cls, value):
        if len(value) > VIDEO_DESCRIPTION_MAX_LENGTH:
            raise ValueError(f"Title must be at most {VIDEO_DESCRIPTION_MAX_LENGTH} characters")
        return value


class VideoTag(BaseModel):
    id: Optional[int] = None
    video_uuid: UUID
    tag: str
    created_at: Optional[datetime] = datetime.now()
    modified_at: Optional[datetime] = datetime.now()

    @field_validator('tag')
    def tag_max_length(cls, value):
        if len(value) > VIDEO_TAG_MAX_LENGTH:
            raise ValueError(f"Tag must be at most {VIDEO_TAG_MAX_LENGTH} characters")
        return value
