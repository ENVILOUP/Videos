from dataclasses import dataclass


@dataclass
class FileStatus:
    file_name: str
    file_hash: str
    writed_bytes: int
    total_bytes: int

@dataclass
class FileMetadata:
    file_hash: str
    total_bytes: int
