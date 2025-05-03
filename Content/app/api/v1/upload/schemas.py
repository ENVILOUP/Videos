from uuid import UUID
from pydantic import BaseModel


class LastChunk(BaseModel):
    file_uuid: UUID
    size: int

