from uuid import UUID
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class UserProfile:
    profile_uuid: UUID
    user_id: UUID
    name: str
    created: Optional[datetime] = datetime.now()
    updated: Optional[datetime] = datetime.now()