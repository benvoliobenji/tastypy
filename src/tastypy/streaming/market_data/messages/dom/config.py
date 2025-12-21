"""DOM config message."""

from ...enums import DomDataFormat, MessageType
from ..base import Message


class DomConfigMessage(Message):
    """Notification of DOM service configuration."""

    def __init__(
        self,
        channel: int,
        data_format: DomDataFormat,
        aggregation_period: float | None = None,
        depth_limit: int | None = None,
        order_fields: list[str] | None = None,
    ) -> None:
        """
        Initialize a DOM config message.

        Args:
            channel: The channel ID.
            data_format: Data format being used.
            aggregation_period: Aggregation period in seconds.
            depth_limit: Maximum depth of order book.
            order_fields: Order fields being sent.
        """
        super().__init__(MessageType.DOM_CONFIG, channel)
        self.data_format = data_format
        self.aggregation_period = aggregation_period
        self.depth_limit = depth_limit
        self.order_fields = order_fields or []
