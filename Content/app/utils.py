import logging
import httpx

from app.config import config


logger = logging.getLogger('uvicorn.error')


DEBEZIUM_CONFIG = {
    'name': 'content-connector',
    'config': {
        'connector.class': 'io.debezium.connector.postgresql.PostgresConnector',
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


async def try_init_debezium():
    async with httpx.AsyncClient(transport=httpx.AsyncHTTPTransport(retries=10)) as client:
        response = await client.post(
            config.debezium_url,
            headers={'Content-Type': 'application/json'},
            json=DEBEZIUM_CONFIG
        )
        if response.status_code == 201:
            logger.info(f"Created debezium connector")
        else:
            logger.warning(
                f"Failed to create connector: Status Code: {response.status_code}")
