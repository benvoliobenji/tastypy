"""Format of data in FEED_DATA messages."""

from enum import Enum


class FeedDataFormat(str, Enum):
    """Format of data in FEED_DATA messages."""

    FULL = "FULL"
    COMPACT = "COMPACT"
