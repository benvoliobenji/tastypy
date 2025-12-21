"""Setup and Keepalive messages."""

from typing import Any

from ...enums import MessageType
from ..base import Message


class SetupMessage(Message):
    """Setup message to initiate connection."""

    def __init__(
        self,
        channel: int = 0,
        keepalive_timeout: int = 60,
        accept_keepalive_timeout: int = 60,
        version: str = "0.1-py/1.0.0",
    ) -> None:
        """
        Initialize a setup message.

        Args:
            channel: The channel ID (always 0 for setup).
            keepalive_timeout: Client's keepalive timeout in seconds.
            accept_keepalive_timeout: Accepted server keepalive timeout.
            version: Client version string.
        """
        super().__init__(MessageType.SETUP, channel)
        self.keepalive_timeout = keepalive_timeout
        self.accept_keepalive_timeout = accept_keepalive_timeout
        self.version = version

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary for JSON serialization."""
        return {
            "type": self.type.value,
            "channel": self.channel,
            "keepaliveTimeout": self.keepalive_timeout,
            "acceptKeepaliveTimeout": self.accept_keepalive_timeout,
            "version": self.version,
        }


class KeepaliveMessage(Message):
    """Keepalive message to maintain connection."""

    def __init__(self, channel: int = 0) -> None:
        """
        Initialize a keepalive message.

        Args:
            channel: The channel ID (0 for main channel).
        """
        super().__init__(MessageType.KEEPALIVE, channel)
