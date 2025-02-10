from dataclasses import dataclass
from os import getenv


def getenv_bool(key: str, default: bool) -> bool:
    value = getenv(key)
    if not value:
        return default
    if value.lower() == 'true':
        return True
    return False


@dataclass(frozen=True)
class Config:
    debug: bool = getenv_bool('DEBUG', True)
    database: str = getenv('DATABASE', 'postgres://postgres:postgres@pg:5432/contentdb')
    cdn_base_url: str = getenv('CDN_BASE_URL', 'http://cdn.enviloup.localhost')   
    debezium_url: str = getenv('DEBEZIUM_CONNECTOR_URL', 'http://debezium:8083/connectors')  


config = Config()
