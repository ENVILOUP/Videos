from fastapi import APIRouter

from app.api.v1.search.views import router as search_router


router = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

router.include_router(search_router)
