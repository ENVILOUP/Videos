from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.utils import try_init_kafka_connect
from app.config import config
from app.videos.views import router as videos_router
from app.views import router as root_router
from app.migrations import apply_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    apply_migrations()
    await try_init_kafka_connect()
    yield

app = FastAPI(
    title='Content Service',
    lifespan=lifespan, 
    debug=config.debug
)

app.include_router(root_router, prefix="")
app.include_router(videos_router, prefix='/videos')
