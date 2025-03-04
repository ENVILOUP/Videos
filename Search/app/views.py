import logging
from fastapi import APIRouter, Depends
from elasticsearch import AsyncElasticsearch

from app.dependencies.elasticsearch import elasticsearch_instance
from app.helpers.schemas import SuccessResponse
from app.helpers.statuses import StatusCodes

router = APIRouter()

logger = logging.getLogger('uvicorn.error')


@router.get(
    path="/health-check",
    response_model=SuccessResponse[str]
)
async def health_check(elasticsearch: AsyncElasticsearch = Depends(elasticsearch_instance)):
    try:
        await elasticsearch.ping()
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e

    return {
        "status_code": StatusCodes.OK,
        "data": "Didn't fall down :0"
    }
