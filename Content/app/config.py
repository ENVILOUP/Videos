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
    database: str = getenv(
        'DATABASE', 
        'postgres://postgres:postgres@pg:5432/contentdb'
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
    cdn_base_url: str = getenv(
        'CDN_BASE_URL',
        'http://cdn.enviloup.localhost'
    )
    kafka_connect_url: str = getenv(
        'KAFKA_CONNECT_URL',
        'http://cdc:8083/connectors'
    )


config = Config()
