from typing import final
from app.core.ports.file_storage_repository import FileStorageRepository
from app.core.ports.file_upload_status_repository import FileUploadStatusRepository


@final
class SaveFileChunkUseCase:
    def __init__(
        self,
        file_upload_status_repository: FileUploadStatusRepository,
        file_storage_repository: FileStorageRepository
    ):
        self._file_upload_status_repository = file_upload_status_repository
        self._file_storage_repository = file_storage_repository

    async def execute(self, file_hash: str, chunk: bytes):
        file_status = await self._file_upload_status_repository.get_file_status(file_hash)
        if file_status is None:
            raise ValueError(f"File status not found for hash: {file_hash}")

        if file_status.writed_bytes == file_status.total_bytes:
            raise ValueError(f"File already fully uploaded. Hash: {file_hash}")

        writed_bytes = await self._file_storage_repository.save(file_status.file_name, chunk)

        if writed_bytes != len(chunk):
            raise ValueError(
                f"Failed to write the entire chunk. Expected {len(chunk)}, got {writed_bytes}"
            )

        file_status.writed_bytes += writed_bytes

        if file_status.writed_bytes > file_status.total_bytes:
            raise ValueError(
                f"Uploaded bytes exceed total bytes. Hash: {file_hash}, "
                f"Uploaded: {file_status.writed_bytes}, Total: {file_status.total_bytes}"
            )

        file_status = await self._file_upload_status_repository.save_file_status(file_status)

        return file_status
