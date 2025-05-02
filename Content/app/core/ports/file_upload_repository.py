from abc import ABC, abstractmethod
from typing import Optional
from app.core.entities.files import FileStatus


class FileUploadRepository(ABC):

    @abstractmethod
    def get_file_status(self, file_hash: str) -> Optional[FileStatus]:
        pass

    @abstractmethod
    def save_file_status(self, file_status: FileStatus) -> FileStatus:
        pass
