from unittest.mock import AsyncMock, MagicMock

from asyncpg import Connection
import pytest


@pytest.fixture
def connection():
    mock_connection = MagicMock(spec=Connection)
    mock_connection.fetchrow = AsyncMock()
    mock_connection.fetch = AsyncMock()
    return mock_connection
