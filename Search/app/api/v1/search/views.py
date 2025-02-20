import logging
from typing import List

from fastapi import APIRouter, Query
from elasticsearch import Elasticsearch

from app.helpers.exceptions import NotFoundException
from app.helpers.schemas import SuccessResponse
from app.helpers.statuses import StatusCodes
from app.config import config

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/search",
)


@router.get(path="/", response_model=SuccessResponse[List[str]])
async def search(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=50), query: str = Query("")):

    start_index = (page - 1) * size
    end_index = start_index + size

    es = Elasticsearch(config.elasticsearch_database)
    results = es.search(index="cdc.public.videos",
                        body={
                            "query": {
                                "match": {
                                    "title": {
                                        "query": query,
                                        "fuzziness": "auto"
                                    }
                                }
                            }
                        })

    hits = [result["_source"]["video_uuid"]
            for result in results['hits']['hits']]

    if hits == []:
        raise NotFoundException(StatusCodes.NOT_FOUND)

    paginated_ids = hits[start_index:end_index]

    return {
        'status_code': StatusCodes.OK,
        'data': paginated_ids
    }
