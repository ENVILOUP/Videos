from fastapi import Depends, FastAPI

from app.config import config
from app.videos.views import router as videos_router
from app.views import router as root_router


app = FastAPI(
    title='Content Service',
    debug=config.debug,
    root_path='/content'
)

app.include_router(root_router, prefix="")
app.include_router(videos_router, prefix='/videos')
