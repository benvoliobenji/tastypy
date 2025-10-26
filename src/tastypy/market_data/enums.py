"""Enum types for market data module."""

from enum import Enum


class ClosePriceType(str, Enum):
    """Contains possible statuses for close prices."""

    FINAL = "Final"
    INDICATIVE = "Indicative"
    PRELIMINARY = "Preliminary"
    REGULAR = "Regular"
    UNKNOWN = "Unknown"


class ExchangeType(str, Enum):
    """Contains the valid exchanges to fetch data for."""

    EQUITY = "Equity"
    SMALLS = "Smalls"
    CME = "CME"
    CFE = "CFE"
    CBOED = "CBOED"
    BOND = "Bond"
    CRYPTOCURRENCY = "Cryptocurrency"
    EQUITY_OFFERING = "Equity Offering"
    UNKNOWN = "Unknown"


class InstrumentType(str, Enum):
    """Types of instruments available in the API."""

    BOND = "Bond"
    CRYPTOCURRENCY = "Cryptocurrency"
    EQUITY = "Equity"
    EQUITY_OFFERING = "Equity Offering"
    EQUITY_OPTION = "Equity Option"
    FIXED_INCOME_SECURITY = "Fixed Income Security"
    FUTURE = "Future"
    FUTURE_OPTION = "Future Option"
    INDEX = "Index"
    LIQUIDITY_POOL = "Liquidity Pool"
    MUTUAL_FUND = "Mutual Fund"
    UNKNOWN = "Unknown"
