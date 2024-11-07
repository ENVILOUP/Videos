import redis.asyncio as aioredis
from app.redis_client import client

async def get_redis() -> aioredis.Redis:
    return client
