"""Feed service contract types."""

from enum import Enum


class FeedContract(str, Enum):
    """Feed service contract types."""

    TICKER = "TICKER"
    STREAM = "STREAM"
    HISTORY = "HISTORY"
    AUTO = "AUTO"
