from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, field_validator

from app.config import config

VIDEO_TITLE_MAX_LENGTH = 255
VIDEO_DESCRIPTION_MAX_LENGTH = 4095
VIDEO_TAG_MAX_LENGTH = 255


class Video(BaseModel):
    video_uuid: UUID
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    modified_at: Optional[datetime] = None

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
    
    @field_validator('video_url', 'thumbnail_url', mode='before')
    def concat_cdn_base_url(cls, value):
        return f'{config.cdn_base_url}{value}'


class VideoTag(BaseModel):
    video_uuid: UUID
    tag: str

    @field_validator('tag')
    def tag_max_length(cls, value):
        if len(value) > VIDEO_TAG_MAX_LENGTH:
            raise ValueError(f"Tag must be at most {VIDEO_TAG_MAX_LENGTH} characters")
        return value
