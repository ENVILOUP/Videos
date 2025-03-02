from dataclasses import dataclass
from os import getenv


def getenv_bool(key: str, default: bool) -> bool:
    value = getenv(key)
    if not value:
        return default
    if value.lower() == 'true':
        return True
    return False


def getenv_int(key: str, default: int) -> int:
    value = getenv(key)
    if not value:
        return default
    return int(value)


@dataclass(frozen=True)
class Config:
    debug: bool = getenv_bool('DEBUG', True)
    jwt_key: str = getenv(
        'JWT_KEY', '18Z0Vmuq5j99VY0X1xkIVlZ499t3SqHha7siBG29tnb4WAuR')
    database: str = getenv(
        'DATABASE',
        'postgres://postgres:postgres@pg:5432/profiledb'
    )
    database_connection_timeout: int = getenv_int(
        'DATABASE_CONNECTION_TIMEOUT',
        10
    )
    database_pool_min_size: int = getenv_int(
        'DATABASE_POOL_MIN_SIZE',
        10
    )
    database_pool_max_size: int = getenv_int(
        'DATABASE_POOL_MAX_SIZE',
        10
    )


config = Config()
