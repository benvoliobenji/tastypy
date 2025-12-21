"""
Market data module for TastyTrade REST API.

This module provides access to market data quotes and instrument information via the
TastyTrade REST API (not real-time streaming - see tastypy.streaming for that).

Classes:
    MarketDataByType: Fetch market data grouped by instrument type
    MarketDataItem: Individual market data quote/snapshot
    Instrument: Instrument details and metadata
    InstrumentKey: Unique identifier for instruments

Enums:
    InstrumentType: Type of instrument (Equity, EquityOption, Future, etc.)
    ExchangeType: Exchange identifier
    ClosePriceType: Type of closing price

Example - Fetch Market Data:
    >>> from tastypy import Session
    >>> from tastypy.market_data import MarketDataByType, InstrumentType
    >>>
    >>> session = Session(client_secret="...", refresh_token="...")
    >>> market_data = MarketDataByType(session)
    >>> market_data.sync(symbols=["AAPL", "MSFT"])
    >>>
    >>> for symbol in market_data.equity_symbols:
    ...     item = market_data.get_equity_item(symbol)
    ...     print(f"{symbol}: ${item.last_price}")

Example - Get Instrument Details:
    >>> from tastypy.market_data import Instrument
    >>>
    >>> instrument = Instrument(session, "AAPL")
    >>> instrument.sync()
    >>> print(f"Symbol: {instrument.symbol}")
    >>> print(f"Type: {instrument.instrument_type}")
    >>> print(f"Shortable: {instrument.is_shortable}")

Note: For real-time streaming market data, use the tastypy.streaming module instead.
"""

from tastypy.market_data.enums import ClosePriceType, ExchangeType, InstrumentType
from tastypy.market_data.instrument import Instrument
from tastypy.market_data.instrument_key import InstrumentKey
from tastypy.market_data.market_data_by_type import MarketDataByType
from tastypy.market_data.market_data_item import MarketDataItem

__all__ = [
    # Main classes
    "MarketDataByType",
    "MarketDataItem",
    "Instrument",
    "InstrumentKey",
    # Enums
    "InstrumentType",
    "ExchangeType",
    "ClosePriceType",
]
