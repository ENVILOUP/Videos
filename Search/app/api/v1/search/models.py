from pydantic import BaseModel
from typing import List


class VideoResultModel(BaseModel):
    video_uuid: str


class SearchResponseModel(BaseModel):
    page: int
    total_pages: int
    results: List[str]
