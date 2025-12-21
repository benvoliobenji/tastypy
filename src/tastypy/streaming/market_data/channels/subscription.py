"""Subscription representation for market events."""

from ..enums import EventType
from typing import Any


class Subscription:
    """Represents a subscription to market events for a symbol."""

    def __init__(
        self,
        symbol: str,
        event_type: EventType,
        from_time: int | None = None,
    ) -> None:
        """
        Initialize a subscription.

        Args:
            symbol: The symbol to subscribe to.
            event_type: The type of event (Quote, Trade, Candle, etc.).
            from_time: For time-series events, the start time in epoch milliseconds.
        """
        self.symbol = symbol
        self.event_type = event_type
        self.from_time = from_time

    def to_dict(self) -> dict[str, Any]:
        """Convert subscription to dictionary for API."""
        result: dict[str, Any] = {
            "symbol": self.symbol,
            "type": self.event_type.value,
        }
        if self.from_time is not None:
            result["fromTime"] = self.from_time
        return result
