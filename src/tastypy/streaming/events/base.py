"""Base class for all market events."""

import datetime
from typing import Any


class MarketEvent:
    """Base class for all market events."""

    def __init__(
        self, data: dict[str, Any] | list[Any], fields: list[str] | None = None
    ) -> None:
        """
        Initialize a market event.

        Args:
            data: Event data (dict for FULL format, list for COMPACT format).
            fields: Field names for COMPACT format.
        """
        if isinstance(data, dict):
            self._data = data
        elif isinstance(data, list) and fields:
            # COMPACT format: convert list to dict using field names
            self._data = dict(zip(fields, data))
        else:
            self._data = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a field value with a default."""
        return self._data.get(key, default)

    @property
    def event_type(self) -> str:
        """The type of the event."""
        return str(self._data.get("eventType", ""))

    @property
    def event_symbol(self) -> str:
        """The symbol for this event."""
        return str(self._data.get("eventSymbol", ""))

    @property
    def event_time(self) -> datetime.datetime | None:
        """The time of the event."""
        value = self._data.get("eventTime")
        if value and value != "NaN":
            return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert the event to a dictionary."""
        return self._data.copy()
