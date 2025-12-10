"""Error messages."""

from ...enums import MessageType, ErrorType
from ..base import Message


class ErrorMessage(Message):
    """Error notification."""

    def __init__(self, channel: int, error: str, message: str | None = None) -> None:
        """
        Initialize an error message.

        Args:
            channel: The channel ID.
            error: Error code or type.
            message: Error message description.
        """
        super().__init__(MessageType.ERROR, channel)
        self.error = ErrorType(error) if isinstance(error, str) else error
        self.message = message
