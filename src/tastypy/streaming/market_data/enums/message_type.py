"""Types of messages in the DXLink WebSocket protocol."""

from enum import Enum


class MessageType(str, Enum):
    """Types of messages in the DXLink WebSocket protocol."""

    # Connection messages
    SETUP = "SETUP"
    KEEPALIVE = "KEEPALIVE"

    # Authentication messages
    AUTH = "AUTH"
    AUTH_STATE = "AUTH_STATE"

    # Channel management messages
    CHANNEL_REQUEST = "CHANNEL_REQUEST"
    CHANNEL_OPENED = "CHANNEL_OPENED"
    CHANNEL_CLOSED = "CHANNEL_CLOSED"
    CHANNEL_CANCEL = "CHANNEL_CANCEL"

    # Feed service messages
    FEED_SETUP = "FEED_SETUP"
    FEED_CONFIG = "FEED_CONFIG"
    FEED_SUBSCRIPTION = "FEED_SUBSCRIPTION"
    FEED_DATA = "FEED_DATA"

    # DOM service messages
    DOM_SETUP = "DOM_SETUP"
    DOM_CONFIG = "DOM_CONFIG"
    DOM_SNAPSHOT = "DOM_SNAPSHOT"

    # Error messages
    ERROR = "ERROR"
