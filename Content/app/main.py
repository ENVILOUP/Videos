from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.helpers.swagger import RESPONSES_TYPES_DOC
from app.helpers.exceptions import BaseAppException
from app.helpers.schemas import ErrorResponse
from app.helpers.statuses import StatusCodes
from app.utils import try_init_kafka_connect
from app.config import config
from app.videos.views import router as videos_router
from app.views import router as root_router
from app.migrations import apply_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    apply_migrations()
    await try_init_kafka_connect()
    yield

app = FastAPI(
    title='Content Service',
    lifespan=lifespan,
    debug=config.debug,
    responses=RESPONSES_TYPES_DOC
)

app.include_router(root_router, prefix="")
app.include_router(videos_router, prefix='/videos')


# TODO: to be moved to a separate module (DEV-46)
@app.exception_handler(BaseAppException)
async def base_application_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.http_status_code,
        content=ErrorResponse(
            status_code=exc.app_status_code
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status_code=StatusCodes.VALIDATION_ERROR
        ).model_dump()
    )
