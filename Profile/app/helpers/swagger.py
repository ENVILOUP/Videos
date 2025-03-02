
from app.helpers.schemas import ErrorResponse
from app.helpers.statuses import StatusCodes


RESPONSES_TYPES_DOC = {
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
    }
}