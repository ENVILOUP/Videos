from abc import ABC, abstractmethod


class ExternalSystemHealthCheckPort(ABC):
    """
    Port for checking the health of an external system.
    """

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check the health of the external system.
        """
        raise NotImplementedError
