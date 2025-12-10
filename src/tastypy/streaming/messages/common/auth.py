"""Authentication messages."""

from typing import Any

from ...enums import AuthState, MessageType
from ..base import Message


class AuthMessage(Message):
    """Authentication message."""

    def __init__(self, token: str, channel: int = 0) -> None:
        """
        Initialize an auth message.

        Args:
            token: The API quote token for authentication.
            channel: The channel ID (0 for main channel).
        """
        super().__init__(MessageType.AUTH, channel)
        self.token = token

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary for JSON serialization."""
        return {
            "type": self.type.value,
            "channel": self.channel,
            "token": self.token,
        }


class AuthStateMessage(Message):
    """Authentication state notification from server."""

    def __init__(self, state: AuthState, user_id: str | None = None) -> None:
        """
        Initialize an auth state message.

        Args:
            state: The authentication state.
            user_id: The user ID if authorized.
        """
        super().__init__(MessageType.AUTH_STATE, 0)
        self.state = state
        self.user_id = user_id
