from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class Channel(BaseModel):
    channel_uuid: UUID
    owner_id: UUID
    name: str
    created: Optional[datetime] = datetime.now()
    updated: Optional[datetime] = datetime.now()