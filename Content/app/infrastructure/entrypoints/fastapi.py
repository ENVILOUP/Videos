from contextlib import asynccontextmanager
import asyncio
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.dependencies.postgresql import database
from app.api.swagger import RESPONSES_TYPES_DOC
from app.api.exceptions import BaseAppException
from app.api.schemas import ErrorResponse
from app.api.statuses import StatusCodes
from app.infrastructure.debezium.utils import try_init_kafka_connect
from app.infrastructure.config.config import config
from app.api.routers import api_router
from app.api.views import router as root_router
from app.infrastructure.postgresql.migrations import apply_migrations


logger = logging.getLogger('uvicorn.error')


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await database.connect()
        apply_migrations()
        asyncio.create_task(try_init_kafka_connect())
        yield
        await database.disconnect()

    app = FastAPI(
        title='Content Service',
        lifespan=lifespan,
        debug=config.debug,
        responses=RESPONSES_TYPES_DOC  # type: ignore
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
