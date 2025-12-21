"""FEED setup message."""

from typing import Any

from ...enums import FeedDataFormat, MessageType
from ..base import Message


class FeedSetupMessage(Message):
    """Configure the FEED service."""

    def __init__(
        self,
        channel: int,
        accept_aggregation_period: float | None = None,
        accept_data_format: FeedDataFormat = FeedDataFormat.COMPACT,
        accept_event_fields: dict[str, list[str]] | None = None,
    ) -> None:
        """
        Initialize a feed setup message.

        Args:
            channel: The channel ID.
            accept_aggregation_period: Aggregation period in seconds.
            accept_data_format: Data format (FULL or COMPACT).
            accept_event_fields: Event fields to subscribe to.
        """
        super().__init__(MessageType.FEED_SETUP, channel)
        self.accept_aggregation_period = accept_aggregation_period
        self.accept_data_format = accept_data_format
        self.accept_event_fields = accept_event_fields or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary for JSON serialization."""
        result: dict[str, Any] = {
            "type": self.type.value,
            "channel": self.channel,
            "acceptDataFormat": self.accept_data_format.value,
        }

        if self.accept_aggregation_period is not None:
            result["acceptAggregationPeriod"] = self.accept_aggregation_period

        if self.accept_event_fields:
            result["acceptEventFields"] = self.accept_event_fields

        return result
