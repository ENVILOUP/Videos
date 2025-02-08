from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asyncpg import connect, Connection

from app.config import config


@asynccontextmanager
async def get_connection() -> AsyncGenerator[Connection, None]:
    try:
        connection = await connect(config.database)
        yield connection
    finally:
        await connection.close()
