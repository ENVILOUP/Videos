import logging
from typing import Annotated, AsyncGenerator

from asyncpg import Connection, create_pool, Pool
from fastapi import Depends

from app.adapters.external_system_heath_check.postgresql_heath_check import PostgreSQLHealthCheck
from app.application.use_cases.check_external_system_health import CheckExternalSystemHealthUseCase
from app.infrastructure.config.config import config


logger = logging.getLogger('uvicorn.error')


class Database:
    def __init__(
        self,
        dsn: str,
        timeout: int = 10,
        pool_min_size: int = 10,
        pool_max_size: int = 10
    ):
        self._dsn = dsn
        self._pool: Pool = None
        self._timeout = timeout
        self._pool_min_size = pool_min_size
        self._pool_max_size = pool_max_size

    async def connect(self):
        if self._pool:
            logger.warning('Database pool already exists')
            return
        logger.info('Creating database pool')
        self._pool = await create_pool(
            dsn=self._dsn,
            min_size=self._pool_min_size,
            max_size=self._pool_max_size
        )

    async def disconnect(self):
        if not self._pool:
            logger.warning('Database pool does not exist')
            return
        logger.info('Closing database pool')
        await self._pool.close()

    async def get_connection(self) -> Connection:
        connection = await self._pool.acquire(timeout=self._timeout)
        logger.debug('Connection acquired')
        return connection

    async def release(self, connection: Connection):
        await self._pool.release(connection, timeout=self._timeout)


database = Database(
    dsn=config.database,
    timeout=config.database_connection_timeout,
    pool_min_size=config.database_pool_min_size,
    pool_max_size=config.database_pool_max_size
)


async def database_сonnection() -> AsyncGenerator[Connection, None]:
    connection = await database.get_connection()
    try:
        yield connection
    finally:
        await database.release(connection)
        logger.debug('Connection released')


async def get_postgresql_health_check(
    database: Annotated[Connection, Depends(database_сonnection)]
) -> CheckExternalSystemHealthUseCase:
    return CheckExternalSystemHealthUseCase(
        external_system_heath_check_port=PostgreSQLHealthCheck(database)
    )
