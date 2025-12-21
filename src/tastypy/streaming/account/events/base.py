"""Base class for all account streaming events."""

from typing import Any
import datetime
from .event_type import AccountEventType


class AccountEvent:
    """Base class for all account streaming events."""

    def __init__(
        self, event_type: AccountEventType | None, message: dict[str, Any]
    ) -> None:
        """
        Initialize an account event.

        Args:
            message: Raw message from account streamer with 'type', 'data', and 'timestamp'.
        """
        self._event_type = event_type
        self._message = message
        self._data: dict[str, Any] = message.get("data", {})
        self._timestamp_ms: int = message.get("timestamp", 0)

    @property
    def event_type(self) -> AccountEventType | None:
        """The type of event (Order, CurrentPosition, TradingStatus, etc.)."""
        return self._event_type

    @property
    def timestamp(self) -> datetime.datetime:
        """The timestamp when the event was generated."""
        if self._timestamp_ms:
            return datetime.datetime.fromtimestamp(
                self._timestamp_ms / 1000.0, tz=datetime.timezone.utc
            )
        return datetime.datetime.now(datetime.timezone.utc)

    @property
    def data(self) -> dict[str, Any]:
        """The raw data payload of the event."""
        return self._data

    def to_dict(self) -> dict[str, Any]:
        """Convert the event to a dictionary."""
        return self._message.copy()
