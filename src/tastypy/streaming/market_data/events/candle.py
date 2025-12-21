"""Candle event definition."""

from .base import MarketEvent
from tastypy.utils import parse_json_double
import datetime


class CandleEvent(MarketEvent):
    """
    Candle event with open, high, low, close prices and other information for a specific period.

    Event symbol of the candle is represented with Candle symbol.
    Since the Candle is a time-series event, it is typically subscribed by TimeSeriesSubscription to specify a subscription time range.

    Represents aggregated price data over a specific time interval.
    """

    @property
    def event_flags(self) -> int:
        """Event flags."""
        value = self.get("eventFlags", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def index(self) -> int:
        """Candle index."""
        value = self.get("index", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time(self) -> datetime.datetime | None:
        """Time of the candle."""
        value = self.get("time")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def sequence(self) -> int:
        """Candle sequence number."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def count(self) -> int:
        """Number of trades in the candle period."""
        value = self.get("count", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def open(self) -> float:
        """Opening price."""
        value = self.get("open", 0.0)
        return parse_json_double(value)

    @property
    def high(self) -> float:
        """Highest price."""
        value = self.get("high", 0.0)
        return parse_json_double(value)

    @property
    def low(self) -> float:
        """Lowest price."""
        value = self.get("low", 0.0)
        return parse_json_double(value)

    @property
    def close(self) -> float:
        """Closing price."""
        value = self.get("close", 0.0)
        return parse_json_double(value)

    @property
    def volume(self) -> float:
        """Volume during the candle period."""
        value = self.get("volume", 0.0)
        return parse_json_double(value)

    @property
    def vwap(self) -> float:
        """Volume Weighted Average Price (VWAP) during the candle period."""
        value = self.get("vwap", 0.0)
        return parse_json_double(value)

    @property
    def bid_volume(self) -> float:
        """Total bid volume during the candle period."""
        value = self.get("bidVolume", 0.0)
        return parse_json_double(value)

    @property
    def ask_volume(self) -> float:
        """Total ask volume during the candle period."""
        value = self.get("askVolume", 0.0)
        return parse_json_double(value)

    @property
    def implied_volatility(self) -> float:
        """Implied volatility during the candle period."""
        value = self.get("impliedVolatility", 0.0)
        return parse_json_double(value)

    @property
    def open_interest(self) -> float:
        """Open interest during the candle period."""
        value = self.get("openInterest", 0.0)
        return parse_json_double(value)
