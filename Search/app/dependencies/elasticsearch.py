import logging
from typing import AsyncGenerator
from elasticsearch import AsyncElasticsearch
from app.config import config

logger = logging.getLogger('uvicorn.error')


class ElasticConnector:
    def __init__(self):
        self._es: AsyncElasticsearch = None

    async def connect(self):
        self._es = AsyncElasticsearch(config.elasticsearch_database)
        logger.debug("Elasticsearch connection established")

    async def get_instance(self) -> AsyncElasticsearch:
        if self._es is None:
            await self.connect()
        logger.debug("Connection acquired")
        return self._es

    async def release(self):
        if self._es is not None:
            await self._es.close()
            self._es = None
            logger.debug("Connection closed")


elasticsearch = ElasticConnector()


async def elasticsearch_connector_instance() -> AsyncGenerator[ElasticConnector, None]:
    if elasticsearch.get_instance() is None:
        await elasticsearch.connect()
    try:
        yield elasticsearch
    finally:
        await elasticsearch.release()
        logger.debug("Connection closed")
