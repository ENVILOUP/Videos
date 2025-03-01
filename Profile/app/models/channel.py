from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class Channel:
    channel_uuid: Optional[UUID] = None
    owner_uuid: Optional[UUID] = None
    name: str = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted: bool = False