"""
Market data streaming submodule for TastyTrade DXLink WebSocket protocol.

This submodule provides the lower-level components for real-time market data streaming.
Most users should use the high-level MarketDataStreamer or AsyncMarketDataStreamer
from tastypy.streaming instead.

Components:
    Connection: DXLinkConnection for WebSocket communication
    Channels: FeedChannel and DomChannel for data subscriptions
    Events: Market event types (Quote, Trade, Greeks, Candles, etc.)
    Enums: Event types, message types, and other constants
    Streamers: MarketDataStreamer and AsyncMarketDataStreamer

Example - Using High-Level Streamer (Recommended):
    >>> from tastypy.streaming import MarketDataStreamer, EventType
    >>> streamer = MarketDataStreamer(session)
    >>> streamer.subscribe("AAPL", EventType.QUOTE, callback)
    >>> streamer.start()

Example - Using Lower-Level Components (Advanced):
    >>> from tastypy.streaming.market_data import DXLinkConnection, FeedChannel
    >>> connection = DXLinkConnection(auth_token)
    >>> channel = FeedChannel(connection, "FEED")
    >>> # ... configure and use connection/channel directly
"""

# Channels
from .channels import DomChannel, FeedChannel, Subscription

# Connection
from .connection import DXLinkConnection

# Enums
from .enums import (
    AuthState,
    DomDataFormat,
    ErrorType,
    EventType,
    FeedContract,
    FeedDataFormat,
    FeedQuoteField,
    MessageType,
    ServiceType,
)

# Events
from .events import (
    AnalyticOrderEvent,
    CandleEvent,
    ConfigurationEvent,
    GreeksEvent,
    MarketEvent,
    OptionSaleEvent,
    OrderEvent,
    ProfileEvent,
    QuoteEvent,
    SeriesEvent,
    SpreadOrderEvent,
    SummaryEvent,
    TheoreticalPriceEvent,
    TimeAndSaleEvent,
    TradeETHEvent,
    TradeEvent,
    UnderlyingEvent,
)

# Messages
from .messages import (
    AuthMessage,
    ChannelRequestMessage,
    DomConfigMessage,
    DomSetupMessage,
    DomSnapshotMessage,
    ErrorMessage,
    FeedConfigMessage,
    FeedDataMessage,
    FeedSetupMessage,
    FeedSubscriptionMessage,
    SetupMessage,
)

# Streamers
from .streamers import AsyncMarketDataStreamer, MarketDataStreamer

__all__ = [
    # Main streamer classes
    "MarketDataStreamer",
    "AsyncMarketDataStreamer",
    # Connection
    "DXLinkConnection",
    # Channels
    "FeedChannel",
    "DomChannel",
    "Subscription",
    # Enums
    "EventType",
    "MessageType",
    "AuthState",
    "ServiceType",
    "FeedContract",
    "FeedDataFormat",
    "FeedQuoteField",
    "DomDataFormat",
    "ErrorType",
    # Events
    "MarketEvent",
    "QuoteEvent",
    "TradeEvent",
    "TradeETHEvent",
    "ProfileEvent",
    "SummaryEvent",
    "GreeksEvent",
    "CandleEvent",
    "TimeAndSaleEvent",
    "UnderlyingEvent",
    "SeriesEvent",
    "TheoreticalPriceEvent",
    "AnalyticOrderEvent",
    "OrderEvent",
    "SpreadOrderEvent",
    "OptionSaleEvent",
    "ConfigurationEvent",
    # Messages
    "AuthMessage",
    "ChannelRequestMessage",
    "SetupMessage",
    "ErrorMessage",
    "FeedSetupMessage",
    "FeedConfigMessage",
    "FeedDataMessage",
    "FeedSubscriptionMessage",
    "DomSetupMessage",
    "DomConfigMessage",
    "DomSnapshotMessage",
]
