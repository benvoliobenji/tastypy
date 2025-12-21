"""Base message class for DXLink protocol."""

from typing import Any

from ..enums import MessageType


class Message:
    """Base class for all DXLink messages."""

    def __init__(self, message_type: MessageType, channel: int = 0) -> None:
        """
        Initialize a message.

        Args:
            message_type: The type of the message.
            channel: The channel ID (0 for main channel).
        """
        self.type = message_type
        self.channel = channel

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary for JSON serialization."""
        return {"type": self.type.value, "channel": self.channel}
