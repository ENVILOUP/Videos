from typing import Dict, Optional
from app.application.use_cases.get_file_upload_status import GetOrCreateFileUploadStatusUseCase
import pytest
from unittest.mock import Mock
from uuid import UUID
from app.core.entities.files import FileMetadata, FileStatus
from app.core.ports.file_upload_repository import FileUploadRepository


class InMemoryFileUploadRepository(FileUploadRepository, Mock):
    def __init__(self, data: Optional[Dict[str, FileStatus]] = None):
        self.file_statuses: Dict[str, FileStatus] = {
        } if data is None else data

    def get_file_status(self, file_hash: str) -> Optional[FileStatus]:
        return self.file_statuses.get(file_hash)

    def save_file_status(self, file_status: FileStatus) -> FileStatus:
        self.file_statuses[file_status.file_hash] = file_status
        return file_status


class TestGetFileUploadStatus:
    def test_execute_returns_existing_file_status(self):
        file_metadata = FileMetadata(file_hash="test_hash", total_bytes=1000)
        existing_file_status = FileStatus(
            file_uuid=UUID("12345678-1234-5678-1234-567812345678"),
            file_hash="test_hash",
            writed_bytes=500,
            total_bytes=1000
        )
        file_upload_repository = InMemoryFileUploadRepository({
            'test_hash': existing_file_status
        })
        use_case = GetOrCreateFileUploadStatusUseCase(
            file_upload_repository,
            lambda: UUID("12345678-1234-5678-1234-567812345678")
        )

        result = use_case.execute(file_metadata)

        assert result == existing_file_status
        file_upload_repository.get_file_status.assert_called_once_with(
            "test_hash")
        file_upload_repository.save_file_status.assert_not_called()

    def test_execute_creates_and_saves_new_file_status(self):
        file_metadata = FileMetadata(file_hash="new_hash", total_bytes=2000)
        file_upload_repository = InMemoryFileUploadRepository()
        use_case = GetOrCreateFileUploadStatusUseCase(
            file_upload_repository,
            lambda: UUID("12345678-1234-5678-1234-567812345678")
        )

        result = use_case.execute(file_metadata)

        assert result == FileStatus(
            file_uuid=UUID("12345678-1234-5678-1234-567812345678"),
            file_hash="new_hash",
            writed_bytes=0,
            total_bytes=2000
        )
        file_upload_repository.get_file_status.assert_called_once_with("new_hash")
        file_upload_repository.save_file_status.assert_called_once_with(result)
