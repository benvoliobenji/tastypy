"""Enumerations for DXLink WebSocket streaming protocol."""

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


class ErrorType(str, Enum):
    """Types of errors in DXLink protocol."""

    UNSUPPORTED_PROTOCOL = "UNSUPPORTED_PROTOCOL"
    TIMEOUT = "TIMEOUT"
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_MESSAGE = "INVALID_MESSAGE"
    BAD_ACTION = "BAD_ACTION"
    UNKNOWN = "UNKNOWN"


class AuthState(str, Enum):
    """Authentication states in the DXLink protocol."""

    AUTHORIZED = "AUTHORIZED"
    UNAUTHORIZED = "UNAUTHORIZED"


class ServiceType(str, Enum):
    """Types of services available in DXLink."""

    FEED = "FEED"
    DOM = "DOM"


class FeedContract(str, Enum):
    """Feed service contract types."""

    TICKER = "TICKER"
    STREAM = "STREAM"
    HISTORY = "HISTORY"
    AUTO = "AUTO"


class FeedDataFormat(str, Enum):
    """Format of data in FEED_DATA messages."""

    FULL = "FULL"
    COMPACT = "COMPACT"


class FeedQuoteField(str, Enum):
    """Fields available in quote events."""

    BID_PRICE = "bid_price"
    ASK_PRICE = "ask_price"
    LAST_PRICE = "last_price"
    VOLUME = "volume"
    OPEN_PRICE = "open_price"
    HIGH_PRICE = "high_price"
    LOW_PRICE = "low_price"


class DomDataFormat(str, Enum):
    """Format of data in DOM_SNAPSHOT messages."""

    FULL = "FULL"
    COMPACT = "COMPACT"


class EventType(str, Enum):
    """Types of market events available in DXLink."""

    # Quote and trade events
    QUOTE = "Quote"
    TRADE = "Trade"
    TRADE_ETH = "TradeETH"

    # Profile and summary events
    PROFILE = "Profile"
    SUMMARY = "Summary"

    # Options-related events
    GREEKS = "Greeks"
    THEO_PRICE = "TheoPrice"
    UNDERLYING = "Underlying"
    SERIES = "Series"

    # Time series events
    CANDLE = "Candle"
    TIME_AND_SALE = "TimeAndSale"
    OPTION_SALE = "OptionSale"

    # Order book events
    ORDER = "Order"
    SPREAD_ORDER = "SpreadOrder"
    ANALYTIC_ORDER = "AnalyticOrder"

    # System events
    CONFIGURATION = "Configuration"
    MESSAGE = "Message"
