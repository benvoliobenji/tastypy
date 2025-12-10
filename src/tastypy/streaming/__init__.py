"""
Streaming market data module for TastyTrade.

This module provides real-time market data streaming via DXLink WebSocket protocol.
It supports multiple event types (Quote, Trade, Greeks, Candles, etc.) and runs
in a background thread to avoid blocking your application.

Example:
    >>> from tastypy import Session
    >>> from tastypy.streaming.streamers import MarketDataStreamer, EventType
    >>>
    >>> session = Session(client_secret="...", refresh_token="...")
    >>> streamer = MarketDataStreamer(session)
    >>>
    >>> def on_quote(event):
    ...     print(f"{event.event_symbol}: Bid={event.bid_price}, Ask={event.ask_price}")
    >>>
    >>> streamer.subscribe("AAPL", EventType.QUOTE, on_quote)
    >>> streamer.start()
    >>> streamer.wait()  # Keep running

For async applications:
    >>> from tastypy.streaming.streamers import AsyncMarketDataStreamer, EventType
    >>>
    >>> async def main():
    ...     session = Session(client_secret="...", refresh_token="...")
    ...     async with AsyncMarketDataStreamer(session) as streamer:
    ...         await streamer.subscribe("AAPL", EventType.QUOTE, on_quote)
    ...         await asyncio.sleep(60)  # Stream for 60 seconds
"""

from .channels import DomChannel, FeedChannel, Subscription
from .connection import DXLinkConnection
from .enums import (
    AuthState,
    DomDataFormat,
    EventType,
    FeedContract,
    FeedDataFormat,
    MessageType,
    ServiceType,
)
from .events import (
    CandleEvent,
    GreeksEvent,
    MarketEvent,
    ProfileEvent,
    QuoteEvent,
    SummaryEvent,
    TimeAndSaleEvent,
    TradeETHEvent,
    TradeEvent,
)
from .messages import (
    DomConfigMessage,
    DomSetupMessage,
    DomSnapshotMessage,
)
from .streamers import AsyncMarketDataStreamer, MarketDataStreamer

__all__ = [
    # Main streamer classes
    "MarketDataStreamer",
    "AsyncMarketDataStreamer",
    # Enums
    "EventType",
    "MessageType",
    "AuthState",
    "ServiceType",
    "FeedContract",
    "FeedDataFormat",
    "DomDataFormat",
    # Event types
    "MarketEvent",
    "QuoteEvent",
    "TradeEvent",
    "TradeETHEvent",
    "ProfileEvent",
    "SummaryEvent",
    "GreeksEvent",
    "CandleEvent",
    "TimeAndSaleEvent",
    # Lower-level classes (for advanced users)
    "DXLinkConnection",
    "FeedChannel",
    "DomChannel",
    "Subscription",
    # DOM message classes
    "DomSetupMessage",
    "DomConfigMessage",
    "DomSnapshotMessage",
]
