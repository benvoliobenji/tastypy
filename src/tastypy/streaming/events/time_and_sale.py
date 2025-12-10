"""Time and sale event definition."""

from .base import MarketEvent
from ...utils.decode_json import parse_json_double
import datetime


class TimeAndSaleEvent(MarketEvent):
    """
    Time and Sale represents a trade or other market event with price, like market open/close price, etc.

    Time and Sales are intended to provide information about trades in a continuous time slice
    (unlike Trade events which are supposed to provide snapshot about the current last trade).
    """

    @property
    def index(self) -> int:
        """Time and sale index."""
        value = self.get("index", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time(self) -> datetime.datetime | None:
        """Time of the trade."""
        value = self.get("time")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def time_nano_part(self) -> int:
        """Nanosecond part of the trade time."""
        value = self.get("timeNanoPart", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def sequence(self) -> int:
        """Time and sale sequence number."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def exchange_code(self) -> str:
        """Exchange code for the trade."""
        return str(self.get("exchangeCode", ""))

    @property
    def price(self) -> float:
        """Trade price."""
        value = self.get("price", 0.0)
        return parse_json_double(value)

    @property
    def size(self) -> float:
        """Trade size."""
        value = self.get("size", 0.0)
        return parse_json_double(value)

    @property
    def bid_price(self) -> float:
        """Bid price at time of trade."""
        value = self.get("bidPrice", 0.0)
        return parse_json_double(value)

    @property
    def ask_price(self) -> float:
        """Ask price at time of trade."""
        value = self.get("askPrice", 0.0)
        return parse_json_double(value)

    @property
    def exchange_sale_conditions(self) -> str:
        """Exchange sale conditions."""
        return str(self.get("exchangeSaleConditions", ""))

    @property
    def trade_through_exempt(self) -> bool:
        """Indicates if the trade is through exempt."""
        value = self.get("tradeThroughExempt", False)
        return bool(value)

    @property
    def agressor_side(self) -> str:
        """Aggressor side of the trade (e.g., "BUY", "SELL", "UNKNOWN")."""
        return str(self.get("aggressorSide", "UNKNOWN"))

    @property
    def spread_leg(self) -> bool:
        """Indicates if the trade is part of a spread leg."""
        value = self.get("spreadLeg", False)
        return bool(value)

    @property
    def extended_trading_hours(self) -> bool:
        """Indicates if the trade occurred during extended trading hours."""
        value = self.get("extendedTradingHours", False)
        return bool(value)

    @property
    def valid_tick(self) -> bool:
        """Indicates if the trade has a valid tick."""
        value = self.get("validTick", False)
        return bool(value)

    @property
    def type(self) -> str:
        """Type of the time and sale event."""
        return str(self.get("type", ""))

    @property
    def buyer(self) -> str:
        """Buyer identifier."""
        return str(self.get("buyer", ""))

    @property
    def seller(self) -> str:
        """Seller identifier."""
        return str(self.get("seller", ""))
