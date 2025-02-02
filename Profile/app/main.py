from fastapi import FastAPI
from pydantic import BaseModel

from app.views import router as root_router
from app.profile.views import router as profile_router
from app.profile.channel.views import router as channel_router
#from app.config import config

app = FastAPI(
    title="Profile Service",
    #debug=config.debug
)

class BaseMessage(BaseModel):
    status: int
    message: str


app.include_router(root_router, prefix="")
app.include_router(profile_router, prefix="/profile")
app.include_router(channel_router, prefix="/profile/{profile_uuid}/channel")