"""Enums for watchlists module."""

from enum import Enum


class InstrumentType(str, Enum):
    """Types of instruments that can be added to watchlists."""

    EQUITY = "Equity"
    EQUITY_OPTION = "Equity Option"
    FUTURE = "Future"
    FUTURE_OPTION = "Future Option"
    CRYPTOCURRENCY = "Cryptocurrency"
    WARRANT = "Warrant"
