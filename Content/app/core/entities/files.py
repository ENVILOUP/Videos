from dataclasses import dataclass
from uuid import UUID


@dataclass
class FileStatus:
    file_uuid: UUID
    file_hash: str
    writed_bytes: int
    total_bytes: int

@dataclass
class FileMetadata:
    file_hash: str
    total_bytes: int
