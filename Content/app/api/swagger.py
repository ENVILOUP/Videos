from app.api.schemas import ErrorResponse
from app.api.statuses import StatusCodes


RESPONSES_TYPES_DOC = {
    404: {
        'model': ErrorResponse,
        'description': 'Not found',
        'content': {
            'application/json': {
                'example': ErrorResponse(
                    status_code=StatusCodes.NOT_FOUND
                ).model_dump()
            }
        }
    },
    422: {
        'model': ErrorResponse,
        'description': 'Validation error',
        'content': {
            'application/json': {
                'example': ErrorResponse(
                    status_code=StatusCodes.VALIDATION_ERROR
                ).model_dump()
            }
        }
    },
    410: {
        'model': ErrorResponse,
        'description': 'Deprecated',
        'content': {
            'application/json': {
                'example': ErrorResponse(
                    status_code=StatusCodes.DEPRECATED
                ).model_dump()
            }
        }
    }
}

