"""FEED subscription message."""

from typing import Any

from ...enums import MessageType
from ..base import Message


class FeedSubscriptionMessage(Message):
    """Manage subscriptions in the FEED service."""

    def __init__(
        self,
        channel: int,
        add: list[dict[str, Any]] | None = None,
        remove: list[dict[str, Any]] | None = None,
        reset: bool = False,
    ) -> None:
        """
        Initialize a feed subscription message.

        Args:
            channel: The channel ID.
            add: List of subscriptions to add.
            remove: List of subscriptions to remove.
            reset: Whether to reset all subscriptions.
        """
        super().__init__(MessageType.FEED_SUBSCRIPTION, channel)
        self.add = add or []
        self.remove = remove or []
        self.reset = reset

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary for JSON serialization."""
        result: dict[str, Any] = {
            "type": self.type.value,
            "channel": self.channel,
        }

        if self.reset:
            result["reset"] = True
        if self.add:
            result["add"] = self.add
        if self.remove:
            result["remove"] = self.remove

        return result
