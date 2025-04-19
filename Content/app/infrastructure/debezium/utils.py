import logging
import httpx

from app.infrastructure.config.config import config


logger = logging.getLogger('uvicorn.error')


DEBEZIUM_SOURCE_CONFIG = {
    'name': 'content-connector',
    'config': {
        'connector.class': 'io.debezium.connector.postgresql.PostgresConnector',
        'topic.prefix': 'cdc',
        'tasks.max': '1',
        'database.hostname': 'pg',
        'database.port': '5432',
        'database.user': 'postgres',
        'database.password': 'postgres',
        'database.dbname': 'contentdb',
        'database.server.name': 'content_db',
        'schema.include.list': 'public',
        'table.include.list': 'public.videos_tags, public.videos',
        'snapshot.mode': 'initial', 
        'plugin.name': 'pgoutput'
    }
}


ELASTICSEARCH_SINK_CONFIG = {
    'name': 'content-es-sink-connector',
    'config': {
        'connector.class': 'io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
        'tasks.max': '1',
        'topics': 'cdc.public.videos, cdc.public.videos_tags',
        'connection.url': 'http://elasticsearch:9200',
        'type.name': '_doc',
        'key.ignore': 'true',
        'schema.ignore': 'true',
        'transforms': 'unwrap',
        'transforms.unwrap.type': 'io.debezium.transforms.ExtractNewRecordState'
    }
}


async def try_init_kafka_connect():
    async with httpx.AsyncClient(
        transport=httpx.AsyncHTTPTransport(retries=10),
        headers={'Content-Type': 'application/json'}
    ) as client:
        logger.info(f"Creating debezium connector")
        response = await client.post(
            config.kafka_connect_url,
            json=DEBEZIUM_SOURCE_CONFIG
        )
        if response.status_code == 201:
            logger.info(f"Created debezium connector")
        else:
            logger.warning(
                f"Failed to create connector: Status Code: {response.status_code}")
        
        logger.info(f"Creating elasticsearch sink connector")
        response = await client.post(
            config.kafka_connect_url,
            json=ELASTICSEARCH_SINK_CONFIG
        )
        if response.status_code == 201:
            logger.info(f"Created elasticsearch sink connector")
        else:
            logger.warning(
                f"Failed to create connector: Status Code: {response.status_code}")
