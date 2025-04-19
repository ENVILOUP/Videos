from asyncpg import Connection
from app.core.ports.external_system_heath_check import ExternalSystemHealthCheckPort


class PostgreSQLHealthCheck(ExternalSystemHealthCheckPort):
    def __init__(
        self,
        db: Connection
    ):
        self._db = db

    async def check_health(self) -> bool:
        try:
            await self._db.execute('SELECT 1')
            return True
        except Exception as e:
            return False

