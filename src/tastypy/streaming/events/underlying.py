"""Underlying event definition."""

from .base import MarketEvent
from ...utils.decode_json import parse_json_double
import datetime


class UnderlyingEvent(MarketEvent):
    """
    Underlying event is a snapshot of computed values that are available for an option underlying symbol based on the option prices on the market.

    It represents the most recent information that is available about the corresponding values on the market at any given moment of time.
    """

    @property
    def index(self) -> int:
        """Underlying asset index."""
        value = self.get("index", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time(self) -> datetime.datetime | None:
        """Time of the underlying asset price."""
        value = self.get("time")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def sequence(self) -> int:
        """Underlying asset sequence number."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def volatility(self) -> float:
        """Volatility of the underlying asset."""
        value = self.get("volatility", 0.0)
        return parse_json_double(value)

    @property
    def front_volatility(self) -> float:
        """Front month volatility of the underlying asset."""
        value = self.get("frontVolatility", 0.0)
        return parse_json_double(value)

    @property
    def back_volatility(self) -> float:
        """Back month volatility of the underlying asset."""
        value = self.get("backVolatility", 0.0)
        return parse_json_double(value)

    @property
    def call_volume(self) -> float:
        """Call option volume for the underlying asset."""
        value = self.get("callVolume", 0.0)
        return parse_json_double(value)

    @property
    def put_volume(self) -> float:
        """Put option volume for the underlying asset."""
        value = self.get("putVolume", 0.0)
        return parse_json_double(value)

    @property
    def put_call_ratio(self) -> float:
        """Put/Call ratio for the underlying asset."""
        value = self.get("putCallRatio", 0.0)
        return parse_json_double(value)
