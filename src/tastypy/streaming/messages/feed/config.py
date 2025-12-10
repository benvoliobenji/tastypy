"""FEED config message."""

from ...enums import FeedDataFormat, MessageType
from ..base import Message


class FeedConfigMessage(Message):
    """Notification of FEED service configuration."""

    def __init__(
        self,
        channel: int,
        data_format: FeedDataFormat,
        aggregation_period: float | None = None,
        event_fields: dict[str, list[str]] | None = None,
    ) -> None:
        """
        Initialize a feed config message.

        Args:
            channel: The channel ID.
            data_format: Data format being used.
            aggregation_period: Aggregation period in seconds.
            event_fields: Event fields being sent.
        """
        super().__init__(MessageType.FEED_CONFIG, channel)
        self.data_format = data_format
        self.aggregation_period = aggregation_period
        self.event_fields = event_fields or {}
