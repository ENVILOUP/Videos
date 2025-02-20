from typing import List

from dataclasses import dataclass
from os import getenv


def getenv_bool(key: str, default: bool) -> bool:
    value = getenv(key)
    if not value:
        return default
    if value.lower() == 'true':
        return True
    return False


@dataclass
class Config:
    debug: bool = getenv_bool('DEBUG', False)
    elasticsearch_database: str = getenv(
        'ELASTIC_DATABASE', 'http://elasticsearch:9200')


config = Config()
