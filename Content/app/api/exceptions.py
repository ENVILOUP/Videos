from app.api.statuses import StatusCodes


class BaseAppException(Exception):
    def __init__(self, http_status_code: int, app_status_code: StatusCodes):
        self.http_status_code = http_status_code
        self.app_status_code = app_status_code


class NotFoundException(BaseAppException):
    """ Not found exception. HTTP status code 404. """

    def __init__(self, status_code: StatusCodes):
        super().__init__(
            http_status_code=404,
            app_status_code=status_code
        )


class ConflictException(BaseAppException):
    """ Conflict exception. HTTP status code 409. """

    def __init__(self, status_code: StatusCodes):
        super().__init__(
            http_status_code=409,
            app_status_code=status_code
        )


class DeprecatedException(BaseAppException):
    """ Use for deprecated methods. HTTP status code 410. """

    def __init__(self):
        super().__init__(
            http_status_code=410,
            app_status_code=StatusCodes.DEPRECATED
        )


class ServiceUnavailableException(BaseAppException):
    """ Service unavailable exception. HTTP status code 503. """

    def __init__(self, status_code: StatusCodes):
        super().__init__(
            http_status_code=503,
            app_status_code=status_code
        )
