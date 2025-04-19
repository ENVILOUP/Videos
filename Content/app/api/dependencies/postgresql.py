import logging
from typing import Annotated, AsyncGenerator

from asyncpg import Connection
from fastapi import Depends

from app.adapters.external_system_heath_check.postgresql_heath_check import PostgreSQLHealthCheck
from app.application.use_cases.check_external_system_health import CheckExternalSystemHealthUseCase
from app.infrastructure.postgresql.database import database


logger = logging.getLogger('uvicorn.error')


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
