from typing import List
from uuid import UUID

from pydantic import BaseModel


class VideoModel(BaseModel):
    video_uuid: UUID
