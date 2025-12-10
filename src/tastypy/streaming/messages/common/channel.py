"""Channel management messages."""

from typing import Any

from ...enums import MessageType, ServiceType
from ..base import Message


class ChannelRequestMessage(Message):
    """Request to open a new channel."""

    def __init__(
        self,
        channel: int,
        service: ServiceType,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize a channel request message.

        Args:
            channel: The channel ID to open.
            service: The service type (FEED or DOM).
            parameters: Service-specific parameters.
        """
        super().__init__(MessageType.CHANNEL_REQUEST, channel)
        self.service = service
        self.parameters = parameters or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary for JSON serialization."""
        return {
            "type": self.type.value,
            "channel": self.channel,
            "service": self.service.value,
            "parameters": self.parameters,
        }


class ChannelOpenedMessage(Message):
    """Notification that a channel has been opened."""

    def __init__(
        self, channel: int, service: ServiceType, parameters: dict[str, Any]
    ) -> None:
        """
        Initialize a channel opened message.

        Args:
            channel: The channel ID that was opened.
            service: The service type.
            parameters: Service parameters.
        """
        super().__init__(MessageType.CHANNEL_OPENED, channel)
        self.service = service
        self.parameters = parameters


class ChannelClosedMessage(Message):
    """Notification that a channel has been closed."""

    def __init__(self, channel: int) -> None:
        """
        Initialize a channel closed message.

        Args:
            channel: The channel ID that was closed.
        """
        super().__init__(MessageType.CHANNEL_CLOSED, channel)


class ChannelCancelMessage(Message):
    """Request to close a channel."""

    def __init__(self, channel: int) -> None:
        """
        Initialize a channel cancel message.

        Args:
            channel: The channel ID to close.
        """
        super().__init__(MessageType.CHANNEL_CANCEL, channel)
