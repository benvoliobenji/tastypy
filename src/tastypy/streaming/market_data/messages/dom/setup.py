"""DOM setup message."""

from typing import Any

from ...enums import DomDataFormat, MessageType
from ..base import Message


class DomSetupMessage(Message):
    """Configure the DOM (Depth of Market) service."""

    def __init__(
        self,
        channel: int,
        accept_aggregation_period: float | None = None,
        accept_depth_limit: int | None = None,
        accept_data_format: DomDataFormat = DomDataFormat.FULL,
        accept_order_fields: list[str] | None = None,
    ) -> None:
        """
        Initialize a DOM setup message.

        Args:
            channel: The channel ID.
            accept_aggregation_period: Aggregation period in seconds.
            accept_depth_limit: Maximum depth of order book to receive.
            accept_data_format: Data format (FULL or COMPACT).
            accept_order_fields: Order fields to receive (e.g., ["price", "size"]).
        """
        super().__init__(MessageType.DOM_SETUP, channel)
        self.accept_aggregation_period = accept_aggregation_period
        self.accept_depth_limit = accept_depth_limit
        self.accept_data_format = accept_data_format
        self.accept_order_fields = accept_order_fields or ["price", "size"]

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary for JSON serialization."""
        result: dict[str, Any] = {
            "type": self.type.value,
            "channel": self.channel,
            "acceptDataFormat": self.accept_data_format.value,
        }

        if self.accept_aggregation_period is not None:
            result["acceptAggregationPeriod"] = self.accept_aggregation_period

        if self.accept_depth_limit is not None:
            result["acceptDepthLimit"] = self.accept_depth_limit

        if self.accept_order_fields:
            result["acceptOrderFields"] = self.accept_order_fields

        return result
