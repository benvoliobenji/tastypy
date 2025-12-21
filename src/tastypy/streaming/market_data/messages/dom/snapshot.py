"""DOM snapshot message."""

from typing import Any

from ...enums import MessageType
from ..base import Message


class DomSnapshotMessage(Message):
    """Depth of market snapshot with order book data."""

    def __init__(
        self,
        channel: int,
        time: int,
        bids: list[dict[str, Any]],
        asks: list[dict[str, Any]],
    ) -> None:
        """
        Initialize a DOM snapshot message.

        Args:
            channel: The channel ID.
            time: Timestamp of the snapshot in milliseconds.
            bids: List of bid orders (price/size pairs).
            asks: List of ask orders (price/size pairs).
        """
        super().__init__(MessageType.DOM_SNAPSHOT, channel)
        self.time = time
        self.bids = bids
        self.asks = asks
