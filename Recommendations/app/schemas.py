from typing import Generic, List, TypeVar
from uuid import UUID

from pydantic import BaseModel

T = TypeVar('T')

class VideoModel(BaseModel):
    video_uuid: UUID


class PagedResponse(BaseModel, Generic[T]):
    page: int
    page_size: int
    items: List[T]
