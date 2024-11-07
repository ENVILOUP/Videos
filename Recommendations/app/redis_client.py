import os
import redis.asyncio as aioredis

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))

client = aioredis.Redis(host=redis_host, port=redis_port, db=redis_db)
