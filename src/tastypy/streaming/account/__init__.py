"""
Account streaming submodule for TastyTrade WebSocket protocol.

This submodule provides real-time streaming of account-related events including orders,
balances, positions, quote alerts, and watchlist updates. Most users should use the
high-level AccountStreamer or AsyncAccountStreamer classes.

Components:
    Connection: AccountConnection for WebSocket communication
    Events: Account event types (Order, Balance, Position, QuoteAlert, etc.)
    Streamers: AccountStreamer and AsyncAccountStreamer

Example - Using High-Level Streamer (Recommended):
    >>> from tastypy.streaming.account import AccountStreamer, AccountEventType
    >>> from tastypy import Session
    >>>
    >>> session = Session(client_secret="...", refresh_token="...")
    >>> streamer = AccountStreamer(session)
    >>>
    >>> # Define event handlers
    >>> def on_order(event):
    ...     print(f"Order {event.order_id}: {event.status}")
    >>>
    >>> def on_balance(event):
    ...     print(f"Balance: ${event.net_liquidating_value:.2f}")
    >>>
    >>> # Subscribe to event types
    >>> streamer.subscribe(AccountEventType.ORDER, on_order)
    >>> streamer.subscribe(AccountEventType.BALANCE, on_balance)
    >>>
    >>> # Start streaming
    >>> streamer.start()
    >>> streamer.subscribe_accounts(["5WT00000"])
    >>>
    >>> # ... do other work while streaming in background ...
    >>>
    >>> # Stop streaming
    >>> streamer.stop()

Example - Using Async Streamer:
    >>> import asyncio
    >>> from tastypy.streaming.account import AsyncAccountStreamer, AccountEventType
    >>>
    >>> async def main():
    ...     session = Session(client_secret="...", refresh_token="...")
    ...     streamer = AsyncAccountStreamer(session)
    ...
    ...     async def on_order(event):
    ...         print(f"Order update: {event.order_id}")
    ...
    ...     streamer.subscribe(AccountEventType.ORDER, on_order)
    ...     await streamer.start()
    ...     await streamer.subscribe_accounts(["5WT00000"])
    ...
    ...     # Keep streaming
    ...     await asyncio.sleep(60)
    ...     await streamer.stop()
    >>>
    >>> asyncio.run(main())

Note: This module handles account-level data. For market data streaming (quotes, trades,
      greeks), use the tastypy.streaming.market_data module instead.
"""

# Connection
from .connection import AccountConnection

# Events
from .events import (
    AccountEvent,
    AccountEventType,
    BalanceEvent,
    ComplexOrderEvent,
    OrderEvent,
    PositionEvent,
    PublicWatchlistsEvent,
    QuoteAlertEvent,
    parse_account_event,
    parse_account_events,
)

# Streamers
from .streamers import AccountStreamer, AsyncAccountStreamer

__all__ = [
    # Main streamer classes
    "AccountStreamer",
    "AsyncAccountStreamer",
    # Connection
    "AccountConnection",
    # Enums
    "AccountEventType",
    # Event types
    "AccountEvent",
    "OrderEvent",
    "BalanceEvent",
    "PositionEvent",
    "QuoteAlertEvent",
    "PublicWatchlistsEvent",
    "ComplexOrderEvent",
    # Parsing functions
    "parse_account_event",
    "parse_account_events",
]
