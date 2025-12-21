"""Types of market events available in DXLink."""

from enum import Enum


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
