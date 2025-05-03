from typing import Callable, Optional, final
from app.core.entities.files import FileMetadata, FileStatus
from app.core.ports.file_upload_status_repository import FileUploadStatusRepository


@final
class GetOrCreateFileUploadStatusUseCase:
    def __init__(
        self,
        file_upload_status_repository: FileUploadStatusRepository,
        generate_file_name: Callable[[], str]
    ):
        self._file_upload_status_repository = file_upload_status_repository
        self._generate_filename = generate_file_name

    async def execute(self, file: FileMetadata) -> Optional[FileStatus]:
        file_status = await self._file_upload_status_repository.get_file_status(file.file_hash)

        if file_status is None:
            file_status = FileStatus(
                file_name=self._generate_filename(),
                file_hash=file.file_hash,
                writed_bytes=0,
                total_bytes=file.total_bytes
            )
            file_status = await self._file_upload_status_repository.save_file_status(file_status)

        return file_status
