from fastapi import APIRouter, Query
import random

from app.config import config

router = APIRouter()

@router.post("/find")
async def search(page: int = Query(1, ge=1), size: int = Query(10, gt=0), query: str = Query("")):

    start_index = (page - 1) * size
    end_index = start_index + size
    paginated_ids = config.enviloup_ids[start_index:end_index]

    random.shuffle(paginated_ids)

    return paginated_ids 