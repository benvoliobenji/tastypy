"""
Streaming data module for TastyTrade.

This module provides real-time streaming for both market data and account updates.

Market Data Streaming (via DXLink WebSocket protocol):
    Supports multiple event types (Quote, Trade, Greeks, Candles, etc.) for real-time
    market data. Runs in a background thread to avoid blocking your application.

Account Data Streaming:
    Provides real-time notifications for orders, balances, positions, quote alerts,
    and watchlist updates. Also runs in a background thread for non-blocking operation.

Example - Market Data:
    >>> from tastypy import Session
    >>> from tastypy.streaming import MarketDataStreamer, EventType
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

Example - Account Data:
    >>> from tastypy.streaming import AccountStreamer, AccountEventType
    >>>
    >>> session = Session(client_secret="...", refresh_token="...")
    >>> streamer = AccountStreamer(session)
    >>>
    >>> def on_order(event):
    ...     print(f"Order {event.order_id}: {event.status}")
    >>>
    >>> streamer.subscribe(AccountEventType.ORDER, on_order)
    >>> streamer.start()
    >>> streamer.subscribe_accounts(["5WT00000"])
    >>> streamer.wait()  # Keep running

For async applications:
    >>> from tastypy.streaming import AsyncMarketDataStreamer, AsyncAccountStreamer
    >>>
    >>> async def main():
    ...     session = Session(client_secret="...", refresh_token="...")
    ...     async with AsyncAccountStreamer(session) as streamer:
    ...         streamer.subscribe_orders(on_order)
    ...         await streamer.subscribe_accounts(["5WT00000"])
    ...         await asyncio.sleep(60)  # Stream for 60 seconds
"""

from .account import (
    AccountConnection,
    AccountEvent,
    AccountEventType,
    AccountStreamer,
    AsyncAccountStreamer,
    BalanceEvent,
    ComplexOrderEvent,
    OrderEvent,
    PositionEvent,
    PublicWatchlistsEvent,
    QuoteAlertEvent,
    parse_account_event,
    parse_account_events,
)
from .market_data import (
    AsyncMarketDataStreamer,
    AuthState,
    CandleEvent,
    DomChannel,
    DomConfigMessage,
    DomDataFormat,
    DomSetupMessage,
    DomSnapshotMessage,
    DXLinkConnection,
    EventType,
    FeedChannel,
    FeedContract,
    FeedDataFormat,
    GreeksEvent,
    MarketDataStreamer,
    MarketEvent,
    MessageType,
    ProfileEvent,
    QuoteEvent,
    ServiceType,
    Subscription,
    SummaryEvent,
    TimeAndSaleEvent,
    TradeETHEvent,
    TradeEvent,
)

__all__ = [
    # Main streamer classes
    "MarketDataStreamer",
    "AsyncMarketDataStreamer",
    "AccountStreamer",
    "AsyncAccountStreamer",
    # Account event types
    "AccountEvent",
    "OrderEvent",
    "BalanceEvent",
    "PositionEvent",
    "QuoteAlertEvent",
    "ComplexOrderEvent",
    "PublicWatchlistsEvent",
    # Enums
    "AccountEventType",
    "EventType",
    "MessageType",
    "AuthState",
    "ServiceType",
    "FeedContract",
    "FeedDataFormat",
    "DomDataFormat",
    # Market event types
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
    "AccountConnection",
    # DOM message classes
    "DomSetupMessage",
    "DomConfigMessage",
    "DomSnapshotMessage",
    # Account parsing functions
    "parse_account_event",
    "parse_account_events",
]
