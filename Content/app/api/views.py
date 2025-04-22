import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.dependencies.postgresql import get_postgresql_health_check
from app.api.exceptions import ServiceUnavailableException
from app.api.schemas import SuccessResponse
from app.api.statuses import StatusCodes
from app.application.use_cases.check_external_system_health import CheckExternalSystemHealthUseCase

router = APIRouter()

logger = logging.getLogger('uvicorn.error')


@router.get(
    path="/health-check",
    response_model=SuccessResponse[str]
)
async def health_check(
    use_case: Annotated[CheckExternalSystemHealthUseCase, Depends(get_postgresql_health_check)],
):
    is_healthy = await use_case.execute()

    if not is_healthy:
        logger.critical("Health check failed")
        raise ServiceUnavailableException(StatusCodes.EXTERNAL_SERVICE_UNAVAILABLE)

    return {
        'status_code': StatusCodes.OK,
        'data': "Didn't fall down =)"
    }
