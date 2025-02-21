import logging
from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, Query

from app.api.v1.search.models import SearchResponseModel
from app.api.v1.search.repositories import SearchService
from app.helpers.statuses import StatusCodes
from app.helpers.schemas import SuccessResponse
from app.dependencies.elasticsearch import ElasticConnector, elasticsearch_instance

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/search",
)


async def get_search_service(connector: ElasticConnector = Depends(elasticsearch_instance)) -> SearchService:
    return SearchService(connector)


@router.get(path="/", response_model=SuccessResponse[SearchResponseModel])
async def search(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=50)] = 10,
    query: Annotated[str, Query()] = "",
    search_service: SearchService = Depends(get_search_service),
):
    result = await search_service.search_videos(query=query, page=page, size=size)
    return {
        "status_code": StatusCodes.OK,
        "data": result
    }
