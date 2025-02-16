from fastapi import APIRouter

from app.api.v1.videos.views import router as videos_router


api_v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

api_v1_router.include_router(videos_router)
