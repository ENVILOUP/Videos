import pytest
from app.application.use_cases.save_file_chunk import SaveFileChunkUseCase
from app.core.entities.files import FileStatus
from tests.unit.mocks.file_storage_repository import InMemoryFileStorageRepository
from tests.unit.mocks.file_upload_repository import InMemoryFileUploadRepository


class TestSaveFileChunkUseCase:

    @pytest.mark.asyncio
    async def test_save_file_chunk(self):
        file_upload_status_repostory = InMemoryFileUploadRepository(data={
            "test_hash": FileStatus(
                file_name="test_file",
                file_hash="test_hash",
                writed_bytes=0,
                total_bytes=10
            )
        })
        file_storage_repository = InMemoryFileStorageRepository(storage={})
        use_case = SaveFileChunkUseCase(
            file_upload_status_repository=file_upload_status_repostory,
            file_storage_repository=file_storage_repository
        )

        result = await use_case.execute(
            file_hash="test_hash",
            chunk=b"0123456789"
        )

        assert result == FileStatus(
            file_name="test_file",
            file_hash="test_hash",
            writed_bytes=10,
            total_bytes=10
        )
        assert file_storage_repository.storage["test_file"] == bytearray(
            b"0123456789"
        )

    @pytest.mark.asyncio
    async def test_save_file_chunk_with_partial_write(self):
        file_upload_status_repostory = InMemoryFileUploadRepository(data={
            "test_hash": FileStatus(
                file_name="test_file",
                file_hash="test_hash",
                writed_bytes=0,
                total_bytes=10
            )
        })
        file_storage_repository = InMemoryFileStorageRepository(storage={})
        use_case = SaveFileChunkUseCase(
            file_upload_status_repository=file_upload_status_repostory,
            file_storage_repository=file_storage_repository
        )

        result = await use_case.execute(
            file_hash="test_hash",
            chunk=b"01234"
        )

        assert result == FileStatus(
            file_name="test_file",
            file_hash="test_hash",
            writed_bytes=5,
            total_bytes=10
        )
        assert file_storage_repository.storage["test_file"] == bytearray(
            b"01234"
        )

        result = await use_case.execute(
            file_hash="test_hash",
            chunk=b"56789"
        )
        assert result == FileStatus(
            file_name="test_file",
            file_hash="test_hash",
            writed_bytes=10,
            total_bytes=10
        )
        assert file_storage_repository.storage["test_file"] == bytearray(
            b"0123456789"
        )

    @pytest.mark.asyncio
    async def test_save_file_chunk_with_not_found_file_status(self):
        file_upload_status_repostory = InMemoryFileUploadRepository(data={})
        file_storage_repository = InMemoryFileStorageRepository(storage={})
        use_case = SaveFileChunkUseCase(
            file_upload_status_repository=file_upload_status_repostory,
            file_storage_repository=file_storage_repository
        )

        with pytest.raises(ValueError) as excinfo:
            await use_case.execute(
                file_hash="test_hash",
                chunk=b"0123456789"
            )

        assert str(excinfo.value) == "File status not found for hash: test_hash"

    @pytest.mark.asyncio
    async def test_save_file_chunk_with_already_uploaded_file(self):
        file_upload_status_repostory = InMemoryFileUploadRepository(data={
            "test_hash": FileStatus(
                file_name="test_file",
                file_hash="test_hash",
                writed_bytes=10,
                total_bytes=10
            )
        })
        file_storage_repository = InMemoryFileStorageRepository(storage={})
        use_case = SaveFileChunkUseCase(
            file_upload_status_repository=file_upload_status_repostory,
            file_storage_repository=file_storage_repository
        )

        with pytest.raises(ValueError) as excinfo:
            await use_case.execute(
                file_hash="test_hash",
                chunk=b"0123456789"
            )

        assert str(
            excinfo.value) == "File already fully uploaded. Hash: test_hash"

    @pytest.mark.asyncio
    async def test_save_file_chunk_with_exceeding_bytes(self):
        file_upload_status_repostory = InMemoryFileUploadRepository(data={
            "test_hash": FileStatus(
                file_name="test_file",
                file_hash="test_hash",
                writed_bytes=0,
                total_bytes=10
            )
        })
        file_storage_repository = InMemoryFileStorageRepository(storage={})
        use_case = SaveFileChunkUseCase(
            file_upload_status_repository=file_upload_status_repostory,
            file_storage_repository=file_storage_repository
        )

        with pytest.raises(ValueError) as excinfo:
            await use_case.execute(
                file_hash="test_hash",
                chunk=b"01234567890123456789"
            )

        assert str(excinfo.value) == (
            "Uploaded bytes exceed total bytes. Hash: test_hash, "
            "Uploaded: 20, Total: 10"
        )

    @pytest.mark.asyncio
    async def test_save_file_chunk_with_not_written_bytes(self):
        file_upload_status_repostory = InMemoryFileUploadRepository(data={
            "test_hash": FileStatus(
                file_name="test_file",
                file_hash="test_hash",
                writed_bytes=0,
                total_bytes=10
            )
        })

        async def currupted_save(file_name: str, chunk: bytes) -> int:
            # Simulate a failure in writing the chunk
            return 0

        file_storage_repository = InMemoryFileStorageRepository(storage={})
        file_storage_repository.save = currupted_save
        use_case = SaveFileChunkUseCase(
            file_upload_status_repository=file_upload_status_repostory,
            file_storage_repository=file_storage_repository
        )

        with pytest.raises(ValueError) as excinfo:
            await use_case.execute(
                file_hash="test_hash",
                chunk=b"0123456789"
            )

        assert str(excinfo.value) == (
            "Failed to write the entire chunk. Expected 10, got 0"
        )
