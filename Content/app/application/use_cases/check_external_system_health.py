
from app.core.ports.external_system_heath_check import ExternalSystemHealthCheckPort


class CheckExternalSystemHealthUseCase:
    """
    Use case for checking the health of an external system.
    """

    def __init__(self, external_system_heath_check_port: ExternalSystemHealthCheckPort):
        self._external_system_heath_check_port = external_system_heath_check_port

    async def execute(self) -> bool:
        is_healthy = await self._external_system_heath_check_port.check_health()
        return is_healthy
