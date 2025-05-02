from typing import Callable, Optional
from uuid import UUID, uuid4
from app.core.entities.files import FileMetadata, FileStatus
from app.core.ports.file_upload_repository import FileUploadRepository


class GetOrCreateFileUploadStatusUseCase:
    def __init__(
        self,
        file_upload_repository: FileUploadRepository,
        generate_uuid: Callable[[], UUID]
    ):
        self._file_upload_repository = file_upload_repository
        self._generate_uuid = generate_uuid

    def execute(self, file: FileMetadata) -> Optional[FileStatus]:
        file_status = self._file_upload_repository.get_file_status(file.file_hash)

        if file_status is None:
            file_status = FileStatus(
                file_uuid=self._generate_uuid(),
                file_hash=file.file_hash,
                writed_bytes=0,
                total_bytes=file.total_bytes
            )
            file_status = self._file_upload_repository.save_file_status(file_status)

        return file_status
