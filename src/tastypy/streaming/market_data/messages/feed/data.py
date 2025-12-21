"""FEED data message."""

from typing import Any

from ...enums import MessageType
from ..base import Message


class FeedDataMessage(Message):
    """Market event data from FEED service."""

    def __init__(self, channel: int, data: list[Any]) -> None:
        """
        Initialize a feed data message.

        Args:
            channel: The channel ID.
            data: List of market events.
        """
        super().__init__(MessageType.FEED_DATA, channel)
        self.data = data
