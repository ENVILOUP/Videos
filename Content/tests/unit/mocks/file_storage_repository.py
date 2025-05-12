from typing import Dict
from app.core.ports.file_storage_repository import FileStorageRepository


class InMemoryFileStorageRepository(FileStorageRepository):
    def __init__(self, storage: Dict[str, bytearray]):
        self.storage = storage

    async def _create_file(self, file_name: str) -> None:
        self.storage[file_name] = bytearray()

    async def save(self, file_name: str, chunk: bytes) -> int:
        if file_name not in self.storage:
            await self._create_file(file_name)

        initial_size = len(self.storage[file_name])
        self.storage[file_name].extend(chunk)
        return len(self.storage[file_name]) - initial_size