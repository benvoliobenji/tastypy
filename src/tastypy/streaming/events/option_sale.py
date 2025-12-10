"""Option sale event definition."""

from .base import MarketEvent
from ...utils.decode_json import parse_json_double
import datetime


class OptionSaleEvent(MarketEvent):
    """
    Option Sale event represents a trade or another market event with the price
    (for example, market open/close price, etc.) for each option symbol listed under the specified Underlying.

    Option Sales are intended to provide information about option trades in a
    continuous time slice with the additional metrics, like Option Volatility, Option Delta, and Underlying Price.
    """

    @property
    def index(self) -> int:
        """Option sale index."""
        value = self.get("index", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time(self) -> datetime.datetime | None:
        """Time of the option sale."""
        value = self.get("time")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def time_nano_part(self) -> int:
        """Nanosecond part of the option sale time."""
        value = self.get("timeNanoPart", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def sequence(self) -> int:
        """Option sale sequence number."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def exchange_code(self) -> str:
        """Exchange code for the option sale."""
        return str(self.get("exchangeCode", ""))

    @property
    def price(self) -> float:
        """Option sale price."""
        value = self.get("price", 0.0)
        return parse_json_double(value)

    @property
    def size(self) -> float:
        """Option sale size."""
        value = self.get("size", 0.0)
        return parse_json_double(value)

    @property
    def bid_price(self) -> float:
        """Option sale bid price."""
        value = self.get("bidPrice", 0.0)
        return parse_json_double(value)

    @property
    def ask_price(self) -> float:
        """Option sale ask price."""
        value = self.get("askPrice", 0.0)
        return parse_json_double(value)

    @property
    def exchange_sale_conditions(self) -> str:
        """Exchange sale conditions for the option sale."""
        return str(self.get("exchangeSaleConditions", ""))

    @property
    def trade_through_exempt(self) -> bool:
        """Indicates if the trade is through exempt."""
        value = self.get("tradeThroughExempt", False)
        return bool(value)

    @property
    def agressor_side(self) -> str:
        """Aggressor side of the trade (e.g., "BUY", "SELL", "UNKNOWN")."""
        return str(self.get("aggressorSide", ""))

    @property
    def spread_leg(self) -> bool:
        """Indicates if the option sale is part of a spread leg."""
        value = self.get("spreadLeg", False)
        return bool(value)

    @property
    def extended_trading_hours(self) -> bool:
        """Indicates if the option sale occurred during extended trading hours."""
        value = self.get("extendedTradingHours", False)
        return bool(value)

    @property
    def valid_tick(self) -> bool:
        """Indicates if the option sale has a valid tick."""
        value = self.get("validTick", False)
        return bool(value)

    @property
    def type(self) -> str:
        """Type of the option sale."""
        return str(self.get("type", ""))

    @property
    def underlying_price(self) -> float:
        """Price of the underlying asset at the time of the option sale."""
        value = self.get("underlyingPrice", 0.0)
        return parse_json_double(value)

    @property
    def volatility(self) -> float:
        """Volatility of the option at the time of the sale."""
        value = self.get("volatility", 0.0)
        return parse_json_double(value)

    @property
    def delta(self) -> float:
        """Delta of the option at the time of the sale."""
        value = self.get("delta", 0.0)
        return parse_json_double(value)

    @property
    def option_symbol(self) -> str:
        """The option symbol for this event."""
        return str(self.get("optionSymbol", ""))
