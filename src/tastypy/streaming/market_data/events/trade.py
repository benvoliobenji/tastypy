"""Trade (and extended hours trade) event definition."""

from .base import MarketEvent
from tastypy.utils import parse_json_double
import datetime


class TradeEvent(MarketEvent):
    """
    Trade event with last trade information.

    Represents the last trade that occurred for a symbol.
    """

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
        """Trade sequence number."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def exchange_code(self) -> str:
        """Exchange code for the trade."""
        return str(self.get("exchangeCode", ""))

    @property
    def price(self) -> float:
        """Last trade price."""
        value = self.get("price", 0.0)
        return parse_json_double(value)

    @property
    def change(self) -> float:
        """Last trade change."""
        value = self.get("change", 0.0)
        return parse_json_double(value)

    @property
    def size(self) -> float:
        """Last trade size."""
        value = self.get("size", 0.0)
        return parse_json_double(value)

    @property
    def day_id(self) -> int:
        """Day identifier for the trade."""
        value = self.get("dayId", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def day_volume(self) -> float:
        """Total volume for the day."""
        value = self.get("dayVolume", 0.0)
        return parse_json_double(value)

    @property
    def day_turnover(self) -> float:
        """Total turnover for the day."""
        value = self.get("dayTurnover", 0.0)
        return parse_json_double(value)

    @property
    def tick_direction(self) -> str:
        """Tick direction of the trade (e.g., "UP", "DOWN", "NO_CHANGE")."""
        return str(self.get("tickDirection", "NO_CHANGE"))

    @property
    def extended_trading(self) -> bool:
        """Indicates if the trade occurred during extended trading hours."""
        value = self.get("extendedTrading", False)
        return bool(value)


class TradeETHEvent(TradeEvent):
    """
    Extended trading hours trade event.

    Similar to TradeEvent but for trades during extended hours.
    """

    pass
