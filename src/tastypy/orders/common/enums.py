"""Enumerations for order types and related values."""

from enum import Enum


class OrderType(str, Enum):
    """The type of order in regards to the price."""

    LIMIT = "Limit"
    MARKET = "Market"
    MARKETABLE_LIMIT = "Marketable Limit"
    NOTIONAL_MARKET = "Notional Market"
    STOP = "Stop"
    STOP_LIMIT = "Stop Limit"


class TimeInForce(str, Enum):
    """The length in time before the order expires."""

    DAY = "Day"
    EXT = "Ext"
    EXT_OVERNIGHT = "Ext Overnight"
    GTC = "GTC"
    GTC_EXT = "GTC Ext"
    GTC_EXT_OVERNIGHT = "GTC Ext Overnight"
    GTD = "GTD"
    IOC = "IOC"


class PriceEffect(str, Enum):
    """If pay or receive payment for placing the order."""

    CREDIT = "Credit"
    DEBIT = "Debit"


class OrderAction(str, Enum):
    """The directional action of an order leg."""

    ALLOCATE = "Allocate"
    BUY = "Buy"
    BUY_TO_CLOSE = "Buy to Close"
    BUY_TO_OPEN = "Buy to Open"
    SELL = "Sell"
    SELL_TO_CLOSE = "Sell to Close"
    SELL_TO_OPEN = "Sell to Open"


class InstrumentType(str, Enum):
    """The type of instrument for order legs."""

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


class OrderStatus(str, Enum):
    """The status of an order."""

    RECEIVED = "Received"
    CANCELLED = "Cancelled"
    FILLED = "Filled"
    EXPIRED = "Expired"
    LIVE = "Live"
    REJECTED = "Rejected"
    CONTINGENT = "Contingent"
    ROUTED = "Routed"
    IN_FLIGHT = "In Flight"
    REPLACE_PENDING = "Replace Pending"
    CANCEL_PENDING = "Cancel Pending"
    REMOVED = "Removed"


class ConfirmationStatus(str, Enum):
    """The confirmation status of an order."""

    NOT_REQUIRED = "Not Required"
    REQUIRED = "Required"
    CONFIRMED = "Confirmed"


class ContingentStatus(str, Enum):
    """The contingent status of an order."""

    CONTINGENT = "Contingent"
    NOT_CONTINGENT = "Not Contingent"


class ComplexOrderType(str, Enum):
    """The type of strategy for a complex order."""

    BLAST = "BLAST"
    OCO = "OCO"
    OTO = "OTO"
    OTOCO = "OTOCO"
    PAIRS = "PAIRS"


class RuleComparator(str, Enum):
    """How to compare against a threshold in order rules."""

    GTE = "gte"  # Greater than or equal to
    LTE = "lte"  # Less than or equal to


class RuleAction(str, Enum):
    """The action in which a rule trigger is enacted."""

    CANCEL = "cancel"
    ROUTE = "route"


class RuleIndicator(str, Enum):
    """The indicator for a rule trigger."""

    LAST = "last"
    NAT = "nat"


class QuantityDirection(str, Enum):
    """The quantity direction for price components."""

    LONG = "Long"
    SHORT = "Short"


class SortOrder(str, Enum):
    """The order to sort results in."""

    DESC = "Desc"
    ASC = "Asc"
