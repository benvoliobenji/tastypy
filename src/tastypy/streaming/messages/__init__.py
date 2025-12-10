"""
DXLink protocol messages.

This module contains message classes organized by service type:
- base: Base Message class
- common: Setup, Auth, Channel management messages
- feed: FEED service messages
- dom: DOM service messages
- parser: Message parsing utilities
"""

from .base import Message
from .common import (
    AuthMessage,
    AuthStateMessage,
    ChannelCancelMessage,
    ChannelClosedMessage,
    ChannelOpenedMessage,
    ChannelRequestMessage,
    ErrorMessage,
    KeepaliveMessage,
    SetupMessage,
)
from .dom import DomConfigMessage, DomSetupMessage, DomSnapshotMessage
from .feed import (
    FeedConfigMessage,
    FeedDataMessage,
    FeedSetupMessage,
    FeedSubscriptionMessage,
)
from .parser import parse_message

__all__ = [
    # Base
    "Message",
    # Common messages
    "SetupMessage",
    "KeepaliveMessage",
    "AuthMessage",
    "AuthStateMessage",
    "ChannelRequestMessage",
    "ChannelOpenedMessage",
    "ChannelClosedMessage",
    "ChannelCancelMessage",
    "ErrorMessage",
    # FEED messages
    "FeedSetupMessage",
    "FeedConfigMessage",
    "FeedSubscriptionMessage",
    "FeedDataMessage",
    # DOM messages
    "DomSetupMessage",
    "DomConfigMessage",
    "DomSnapshotMessage",
    # Parser
    "parse_message",
]
