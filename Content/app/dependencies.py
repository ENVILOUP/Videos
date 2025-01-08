from contextlib import asynccontextmanager

from asyncpg import connect, Connection

from app.config import config


@asynccontextmanager
async def get_connection() -> Connection:
    try:
        connection = await connect(config.database)
        yield connection
    finally:
        await connection.close()
