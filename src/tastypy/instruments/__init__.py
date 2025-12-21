"""
Instruments module for TastyTrade API.

This module provides access to instrument data and metadata across multiple asset
classes including equities, options, futures, cryptocurrencies, and warrants.

Classes:
    Common:
        Strikes: Option strike price data
        TickSizes: Minimum price increment information

    Cryptocurrency:
        Cryptocurrencies: Query and retrieve cryptocurrency instruments

    Equities:
        ActiveEquities: Currently active equity symbols
        EquitySymbol: Individual equity symbol information
        CompactOptionChain: Streamlined option chain data
        NestedOptionChain: Hierarchical option chain structure
        get_option_chain: Helper function to fetch option chains

    Futures:
        Future: Futures contract details
        FutureProduct: Futures product specifications
        FutureETFEquivalent: ETF equivalents for futures products
        FutureOptions: Options on futures contracts
        FutureOptionProducts: Futures option product specifications
        FuturesOptionChainsNested: Nested futures option chain data
        FuturesOptionChainsSymbol: Futures option chain by symbol

    Warrants:
        Warrants: Query and retrieve warrant instruments

    Utility:
        QuantityDecimalPrecisions: Decimal precision rules for order quantities

Example - Fetch Active Equities:
    >>> from tastypy import Session
    >>> from tastypy.instruments import ActiveEquities
    >>>
    >>> session = Session(client_secret="...", refresh_token="...")
    >>> equities = ActiveEquities(session)
    >>> equities.sync()
    >>> for symbol in equities.equity_symbols[:5]:
    ...     print(f"Symbol: {symbol}")

Example - Get Option Chain:
    >>> from tastypy.instruments import get_option_chain
    >>>
    >>> chain = get_option_chain(session, "AAPL")
    >>> chain.sync()
    >>> print(f"Strikes available: {len(chain.strikes)}")

Example - Fetch Futures Products:
    >>> from tastypy.instruments import FutureProduct
    >>>
    >>> product = FutureProduct(session, "ES")
    >>> product.sync()
    >>> print(f"Product: {product.code}")
    >>> print(f"Description: {product.description}")

Note: For real-time market data, use the tastypy.streaming or tastypy.market_data modules.
"""

# Common
from .common import Strikes, TickSizes

# Cryptocurrency
from .cryptocurrency import Cryptocurrencies

# Equities
from .equities import (
    ActiveEquities,
    CompactOptionChain,
    EquitySymbol,
    NestedOptionChain,
    get_option_chain,
)

# Futures
from .futures import (
    Future,
    FutureETFEquivalent,
    FutureOptionProducts,
    FutureOptions,
    FutureProduct,
    FuturesOptionChainsNested,
    FuturesOptionChainsSymbol,
)

# Warrants
from .warrants import Warrants

# Quantity Decimal Precisions
from .quantity_decimal_precisions import QuantityDecimalPrecisions

__all__ = [
    # Common
    "Strikes",
    "TickSizes",
    # Cryptocurrency
    "Cryptocurrencies",
    # Equities
    "ActiveEquities",
    "CompactOptionChain",
    "EquitySymbol",
    "NestedOptionChain",
    "get_option_chain",
    # Futures
    "Future",
    "FutureETFEquivalent",
    "FutureOptionProducts",
    "FutureOptions",
    "FutureProduct",
    "FuturesOptionChainsNested",
    "FuturesOptionChainsSymbol",
    # Warrants
    "Warrants",
    # Quantity Decimal Precisions
    "QuantityDecimalPrecisions",
]
