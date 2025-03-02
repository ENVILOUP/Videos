from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class UserProfile:
    profile_uuid: Optional[UUID] = None
    user_uuid: Optional[UUID] = None
    name: str = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted: bool = False