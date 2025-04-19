import logging
from yoyo import read_migrations
from yoyo import get_backend

from app.infrastructure.config.config import config


logger = logging.getLogger('uvicorn.error')

backend = get_backend(config.database)
migrations = read_migrations('/app/migrations/')


def apply_migrations():
    logger.info('Applying migrations')
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
