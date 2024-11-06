import os

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from redis.asyncio import Redis


router = APIRouter(prefix='/recommendations')

app = FastAPI()

# Redis creds
redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))

redis_client = Redis(host=redis_host, port=redis_port, db=redis_db)

class BaseMessage(BaseModel):
    status: int
    message: str


@router.get("/")
async def health_check():
    return BaseMessage(status=200, message='Ok')

@router.post("/cache/{key}")
async def cache_key(key: str):
    await redis_client.set(key, f"Value for {key}")
    return {"message": f"Cached {key}"}

@router.get("/get/{key}")
async def get_from_cache(key: str):
    value = await redis_client.get(key)
    return {"value": value} if value else {"message": "Key not found"}

app.include_router(router)
