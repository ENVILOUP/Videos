import logging
from uuid import uuid4
from fastapi import APIRouter

from app.api.schemas import SuccessResponse
from app.api.statuses import StatusCodes
from app.api.v1.upload.schemas import LastChunk


logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/upload"
)


@router.get(
    path="/",
    response_model=SuccessResponse[LastChunk],
)
async def get_last_chunk(
    file_hash: str
):
    """
    Get the last chunk of a file upload.
    """

    return {
        'status_code': StatusCodes.OK,
        'data': LastChunk(
            file_uuid=uuid4(),
            size=0
        )
    }



