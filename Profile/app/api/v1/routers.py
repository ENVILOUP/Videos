from fastapi import APIRouter
from api.v1.profile.views import router as profile_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(profile_router)