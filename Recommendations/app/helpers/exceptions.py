import logging
from typing import Optional
from app.helpers.statuses import StatusCodes

logger = logging.getLogger('uvicorn.error')


class BaseAppException(Exception):
    def __init__(self, http_status_code: int, app_status_code: StatusCodes):
        self.http_status_code = http_status_code
        self.app_status_code = app_status_code


class ValueException(BaseAppException):
    """ Value exception """

    def __init__(self, doc: Optional[str] = None):
        logger.error(f'Value exception: {doc}')
        super().__init__(
            http_status_code=422,
            app_status_code=StatusCodes.VALIDATION_ERROR
        )
