"""Enums for market sessions module."""

from enum import Enum


class InstrumentCollection(str, Enum):
    """Instrument collections for market sessions."""

    EQUITY = "Equity"
    CME = "CME"
    CFE = "CFE"
    ZERO_HASH_CLOB = "Zero Hash CLOB"
    SMALLS = "Smalls"


class SessionState(str, Enum):
    """Market session states."""

    OPEN = "Open"
    CLOSED = "Closed"
    PRE_MARKET = "Pre-Market"
    POST_MARKET = "Post-Market"
