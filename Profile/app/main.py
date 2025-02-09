from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.migrations import apply_migrations
from app.views import router as root_router
from app.profile.views import router as profile_router
from app.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    apply_migrations()
    yield

app = FastAPI(
    title="Profile Service",
    debug=config.debug,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BaseMessage(BaseModel):
    status: int
    message: str


app.include_router(root_router, prefix="")
app.include_router(profile_router, prefix="/profile")
