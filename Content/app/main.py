from fastapi import Depends, FastAPI
from pydantic import BaseModel

from app.videos.views import router as videos_router

class BaseMessage(BaseModel):
    status: int
    message: str


app = FastAPI(
    root_path='/content'
)


@app.get("/")
async def health_check():
    return BaseMessage(status=200, message='Ok')


app.include_router(videos_router, prefix='/videos')
