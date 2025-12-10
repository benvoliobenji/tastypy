"""Summary event definition."""

from .base import MarketEvent
from ...utils.decode_json import parse_json_double


class SummaryEvent(MarketEvent):
    """
    Summary information snapshot about the trading session including session highs, lows, etc.

    It represents the most recent information that is available about the trading session in the market at any given moment of time.

    Contains open, high, low, close prices and other daily metrics.
    """

    @property
    def day_id(self) -> int:
        """Day identifier."""
        value = self.get("dayId", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def day_open_price(self) -> float:
        """Opening price for the day."""
        value = self.get("dayOpenPrice", 0.0)
        return parse_json_double(value)

    @property
    def day_high_price(self) -> float:
        """High price for the day."""
        value = self.get("dayHighPrice", 0.0)
        return parse_json_double(value)

    @property
    def day_low_price(self) -> float:
        """Low price for the day."""
        value = self.get("dayLowPrice", 0.0)
        return parse_json_double(value)

    @property
    def day_close_price(self) -> float:
        """Closing price for the day."""
        value = self.get("dayClosePrice", 0.0)
        return parse_json_double(value)

    @property
    def day_close_price_type(self) -> str:
        """Type of the closing price."""
        return str(self.get("dayClosePriceType", ""))

    @property
    def prev_day_id(self) -> int:
        """Previous day identifier."""
        value = self.get("prevDayId", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def prev_day_close_price(self) -> float:
        """Previous day's closing price."""
        value = self.get("prevDayClosePrice", 0.0)
        return parse_json_double(value)

    @property
    def prev_day_close_price_type(self) -> str:
        """Type of the previous day's closing price."""
        return str(self.get("prevDayClosePriceType", ""))

    @property
    def prev_day_volume(self) -> float:
        """Previous day's volume."""
        value = self.get("prevDayVolume", 0.0)
        return parse_json_double(value)

    @property
    def open_interest(self) -> float:
        """Open interest (for options/futures)."""
        value = self.get("openInterest", 0.0)
        return parse_json_double(value)
