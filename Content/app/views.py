import logging
from typing import Annotated
from asyncpg import Connection
from fastapi import APIRouter, Depends
from app.api.dependencies.postgresql import database_сonnection
from app.api.schemas import SuccessResponse
from app.api.statuses import StatusCodes

router = APIRouter()

logger = logging.getLogger('uvicorn.error')


@router.get(
    path="/health-check",
    response_model=SuccessResponse[str]
)
async def health_check(
    db: Annotated[Connection, Depends(database_сonnection)]
):
    try:
        await db.fetchval('SELECT 1')
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e

    return {
        'status_code': StatusCodes.OK,
        'data': "Didn't fall down =)"
    }
