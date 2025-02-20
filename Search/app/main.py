from fastapi import FastAPI, Request
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.views import router as root_router
from app.api.routers import router as api_router
from app.config import config
from app.helpers.swagger import RESPONSES_TYPES_DOC
from app.helpers.exceptions import BaseAppException
from app.helpers.schemas import ErrorResponse
from app.helpers.statuses import StatusCodes

logger = logging.getLogger('uvicorn.error')


def create_app() -> FastAPI:
    app = FastAPI(
        title="Search Service",
        debug=config.debug,
        responses=RESPONSES_TYPES_DOC
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(root_router)
    app.include_router(api_router)

    @app.exception_handler(BaseAppException)
    async def base_application_exception_handler(request: Request, exc: BaseAppException):
        logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=exc.http_status_code,
            content=ErrorResponse(
                status_code=exc.app_status_code
            ).model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                status_code=StatusCodes.VALIDATION_ERROR
            ).model_dump()
        )

    return app


app = create_app()
