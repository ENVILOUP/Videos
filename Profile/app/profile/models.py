from typing import Optional
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserProfile:
    profile_uuid: Optional[UUID] = None
    user_uuid: Optional[UUID] = None
    name: str = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted: bool = False


@dataclass
class Channel:
    channel_uuid: Optional[UUID] = None
    owner_uuid: Optional[UUID] = None
    name: str = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted: bool = False
