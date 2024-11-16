from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Config:
    database: str = getenv("DATABASE", "postgres://postgres:postgres@pg:5432/postgres")
    cdn_base_url: str = getenv("CDN_BASE_URL", "http://cdn.enviloup.local:8080/")


config = Config()
