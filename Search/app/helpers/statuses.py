from enum import IntEnum


class StatusCodes(IntEnum):
    OK = 1000
    VALIDATION_ERROR = 1001
    NOT_FOUND = 1002
    DEPRECATED = 1003
