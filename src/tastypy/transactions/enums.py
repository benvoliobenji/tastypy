"""Enums for transaction-related operations."""

import enum


class TransactionAction(str, enum.Enum):
    """Actions that can be taken in a transaction."""

    ALLOCATE = "Allocate"
    BUY = "Buy"
    BUY_TO_CLOSE = "Buy to Close"
    BUY_TO_OPEN = "Buy to Open"
    SELL = "Sell"
    SELL_TO_CLOSE = "Sell to Close"
    SELL_TO_OPEN = "Sell to Open"


class SortOrder(str, enum.Enum):
    """Sort order for transaction queries."""

    DESC = "Desc"
    ASC = "Asc"


class TransactionEffect(str, enum.Enum):
    """Effect of a transaction on account balance."""

    CREDIT = "Credit"
    DEBIT = "Debit"
    NONE = "None"


class InstrumentType(str, enum.Enum):
    """Types of instruments available in transactions."""

    BOND = "Bond"
    CRYPTOCURRENCY = "Cryptocurrency"
    CURRENCY_PAIR = "Currency Pair"
    EQUITY = "Equity"
    EQUITY_OFFERING = "Equity Offering"
    EQUITY_OPTION = "Equity Option"
    FIXED_INCOME_SECURITY = "Fixed Income Security"
    FUTURE = "Future"
    FUTURE_OPTION = "Future Option"
    INDEX = "Index"
    LIQUIDITY_POOL = "Liquidity Pool"
    UNKNOWN = "Unknown"
    WARRANT = "Warrant"
