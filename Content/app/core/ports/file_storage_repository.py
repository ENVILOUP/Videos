

from abc import ABC, abstractmethod


class FileStorageRepository(ABC):

    @abstractmethod
    async def save(self, file_name: str, chunk: bytes) -> int:
        """
        Save a file chunk to the storage.
        :param file_name: The name of the file to save the chunk to.
        :param chunk: The chunk of data to save.
        :return: The number of bytes written.
        """
        pass