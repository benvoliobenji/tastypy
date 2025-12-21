"""Fields available in quote events."""

from enum import Enum


class FeedQuoteField(str, Enum):
    """Fields available in quote events."""

    BID_PRICE = "bid_price"
    ASK_PRICE = "ask_price"
    LAST_PRICE = "last_price"
    VOLUME = "volume"
    OPEN_PRICE = "open_price"
    HIGH_PRICE = "high_price"
    LOW_PRICE = "low_price"
