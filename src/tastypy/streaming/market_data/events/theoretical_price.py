"""Theoretical price event definition."""

from .base import MarketEvent
from tastypy.utils import parse_json_double
import datetime


class TheoreticalPriceEvent(MarketEvent):
    """
    Theo price is a snapshot of the theoretical option price computation that is periodically performed by dxPrice model-free computation.

    It represents the most recent information that is available about the corresponding values at any given moment of time.

    Represents the theoretical price of a financial instrument based on various factors.
    """

    @property
    def index(self) -> int:
        """Theoretical price index."""
        value = self.get("index", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time(self) -> datetime.datetime | None:
        """Time of the theoretical price."""
        value = self.get("time")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def sequence(self) -> int:
        """Theoretical price sequence number."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def price(self) -> float:
        """Asset price used in theoretical price calculation."""
        value = self.get("price", 0.0)
        return parse_json_double(value)

    @property
    def underlying_price(self) -> float:
        """Underlying asset price."""
        value = self.get("underlyingPrice", 0.0)
        return parse_json_double(value)

    @property
    def delta(self) -> float:
        """Delta value used in theoretical price calculation."""
        value = self.get("delta", 0.0)
        return parse_json_double(value)

    @property
    def gamma(self) -> float:
        """Gamma value used in theoretical price calculation."""
        value = self.get("gamma", 0.0)
        return parse_json_double(value)

    @property
    def dividend(self) -> float:
        """Dividend value used in theoretical price calculation."""
        value = self.get("dividend", 0.0)
        return parse_json_double(value)

    @property
    def interest(self) -> float:
        """Interest used in theoretical price calculation."""
        value = self.get("interest", 0.0)
        return parse_json_double(value)
