"""Types of errors in DXLink protocol."""

from enum import Enum


class ErrorType(str, Enum):
    """Types of errors in DXLink protocol."""

    UNSUPPORTED_PROTOCOL = "UNSUPPORTED_PROTOCOL"
    TIMEOUT = "TIMEOUT"
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_MESSAGE = "INVALID_MESSAGE"
    BAD_ACTION = "BAD_ACTION"
    UNKNOWN = "UNKNOWN"
