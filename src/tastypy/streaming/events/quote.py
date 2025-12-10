"""Quote event definition."""

from .base import MarketEvent
from ...utils.decode_json import parse_json_double
import datetime


class QuoteEvent(MarketEvent):
    """
    Quote event with best bid and ask prices.

    Represents the most recent bid/ask quotes on the market.
    """

    @property
    def sequence_number(self) -> int:
        """Quote sequence number."""
        value = self.get("sequenceNumber", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time_nano_part(self) -> int:
        """Nanosecond part of the quote time."""
        value = self.get("timeNanoPart", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def bid_time(self) -> datetime.datetime | None:
        """Time of the bid quote."""
        value = self.get("bidTime")
        if value and value != "NaN":
            # Convert milliseconds to datetime
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def bid_exchange_code(self) -> str:
        """Exchange code for the bid quote."""
        return str(self.get("bidExchangeCode", ""))

    @property
    def bid_price(self) -> float:
        """Best bid price."""
        value = self.get("bidPrice", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def bid_size(self) -> float:
        """Best bid size."""
        value = self.get("bidSize", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def ask_time(self) -> datetime.datetime | None:
        """Time of the ask quote."""
        value = self.get("askTime")
        if value and value != "NaN":
            # Convert milliseconds to datetime
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def ask_exchange_code(self) -> str:
        """Exchange code for the ask quote."""
        return str(self.get("askExchangeCode", ""))

    @property
    def ask_price(self) -> float:
        """Best ask price."""
        value = self.get("askPrice", 0.0)
        return float(value) if value not in ("NaN", None) else 0.0

    @property
    def ask_size(self) -> float:
        """Best ask size."""
        value = self.get("askSize", 0.0)
        return parse_json_double(value, 0.0)
