from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserProfile(BaseModel):
    profile_uuid: UUID
    user_id: UUID
    name: str
    created: Optional[datetime] = datetime.now()
    updated: Optional[datetime] = datetime.now()