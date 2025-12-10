"""Message parser for DXLink protocol."""

from typing import Any

from ..enums import (
    AuthState,
    DomDataFormat,
    FeedDataFormat,
    MessageType,
    ServiceType,
)
from .base import Message
from .common import (
    AuthMessage,
    AuthStateMessage,
    ChannelClosedMessage,
    ChannelOpenedMessage,
    ErrorMessage,
    KeepaliveMessage,
    SetupMessage,
)
from .dom import DomConfigMessage, DomSnapshotMessage
from .feed import FeedConfigMessage, FeedDataMessage


def parse_message(data: dict[str, Any]) -> Message:
    """
    Parse a JSON message into the appropriate Message subclass.

    Args:
        data: The JSON message data.

    Returns:
        An instance of the appropriate Message subclass.
    """
    msg_type = MessageType(data["type"])
    channel = data.get("channel", 0)

    if msg_type == MessageType.SETUP:
        return SetupMessage(
            channel=channel,
            keepalive_timeout=data.get("keepaliveTimeout", 60),
            accept_keepalive_timeout=data.get("acceptKeepaliveTimeout", 60),
            version=data.get("version", ""),
        )

    elif msg_type == MessageType.KEEPALIVE:
        return KeepaliveMessage(channel)

    elif msg_type == MessageType.AUTH:
        return AuthMessage(data["token"], channel)

    elif msg_type == MessageType.AUTH_STATE:
        return AuthStateMessage(AuthState(data["state"]), data.get("userId"))

    elif msg_type == MessageType.CHANNEL_OPENED:
        return ChannelOpenedMessage(
            channel, ServiceType(data["service"]), data.get("parameters", {})
        )

    elif msg_type == MessageType.CHANNEL_CLOSED:
        return ChannelClosedMessage(channel)

    elif msg_type == MessageType.FEED_CONFIG:
        return FeedConfigMessage(
            channel,
            FeedDataFormat(data["dataFormat"]),
            data.get("aggregationPeriod"),
            data.get("eventFields"),
        )

    elif msg_type == MessageType.FEED_DATA:
        return FeedDataMessage(channel, data.get("data", []))

    elif msg_type == MessageType.DOM_CONFIG:
        return DomConfigMessage(
            channel,
            DomDataFormat(data["dataFormat"]),
            data.get("aggregationPeriod"),
            data.get("depthLimit"),
            data.get("orderFields"),
        )

    elif msg_type == MessageType.DOM_SNAPSHOT:
        return DomSnapshotMessage(
            channel,
            data.get("time", 0),
            data.get("bids", []),
            data.get("asks", []),
        )

    elif msg_type == MessageType.ERROR:
        return ErrorMessage(channel, data["error"], data.get("message"))

    else:
        # Return generic message for unhandled types
        return Message(msg_type, channel)
