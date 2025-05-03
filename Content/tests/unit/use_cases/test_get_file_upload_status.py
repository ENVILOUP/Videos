from app.application.use_cases.get_or_create_file_upload_status import GetOrCreateFileUploadStatusUseCase
import pytest
from app.core.entities.files import FileMetadata, FileStatus
from tests.unit.mocks.file_upload_repository import InMemoryFileUploadRepository



class TestGetOrCreateFileUploadStatusUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_existing_file_status(self):
        file_metadata = FileMetadata(file_hash="test_hash", total_bytes=1000)
        existing_file_status = FileStatus(
            file_name='12345678-1234-5678-1234-567812345678',
            file_hash="test_hash",
            writed_bytes=500,
            total_bytes=1000
        )
        file_upload_repository = InMemoryFileUploadRepository({
            'test_hash': existing_file_status
        })
        use_case = GetOrCreateFileUploadStatusUseCase(
            file_upload_repository,
            lambda: '12345678-1234-5678-1234-567812345678'
        )

        result = await use_case.execute(file_metadata)

        assert result == existing_file_status

    @pytest.mark.asyncio
    async def test_execute_creates_and_saves_new_file_status(self):
        file_metadata = FileMetadata(file_hash="new_hash", total_bytes=2000)
        file_upload_repository = InMemoryFileUploadRepository(data={})
        use_case = GetOrCreateFileUploadStatusUseCase(
            file_upload_repository,
            lambda: '12345678-1234-5678-1234-567812345678'
        )

        result = await use_case.execute(file_metadata)

        assert result == FileStatus(
            file_name='12345678-1234-5678-1234-567812345678',
            file_hash="new_hash",
            writed_bytes=0,
            total_bytes=2000
        )
