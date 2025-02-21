from app.helpers.statuses import StatusCodes


class BaseAppException(Exception):
    def __init__(self, http_status_code: int, app_status_code: StatusCodes):
        self.http_status_code = http_status_code
        self.app_status_code = app_status_code
