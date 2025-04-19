from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tag:
    tag: str
    created_at: datetime
    modified_at: datetime
