from typing import Dict, Optional
from app.core.entities.files import FileStatus
from app.core.ports.file_upload_status_repository import FileUploadStatusRepository


class InMemoryFileUploadRepository(FileUploadStatusRepository):
    def __init__(self, data: Dict[str, FileStatus]):
        self.file_statuses = data

    async def get_file_status(self, file_hash: str) -> Optional[FileStatus]:
        return self.file_statuses.get(file_hash)

    async def save_file_status(self, file_status: FileStatus) -> FileStatus:
        self.file_statuses[file_status.file_hash] = file_status
        return file_status
