import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from elasticsearch import AsyncElasticsearch

from app.api.v1.search.shemas import SearchResponseModel
from app.api.v1.search.repositories import SearchRepository
from app.helpers.statuses import StatusCodes
from app.helpers.schemas import SuccessResponse
from app.dependencies.elasticsearch import elasticsearch_instance

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/search",
)


@router.get(path="/videos/", response_model=SuccessResponse[SearchResponseModel])
async def search_videos(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=50)] = 10,
    query: Annotated[str, Query(min_length=1)] = ...,
    elasticsearch: AsyncElasticsearch = Depends(
        elasticsearch_instance),
):
    search_repository = SearchRepository(elasticsearch)
    result = await search_repository.search_videos(query=query, page=page, size=size)
    return {
        "status_code": StatusCodes.OK,
        "data": result
    }
