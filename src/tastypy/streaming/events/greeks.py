"""Greeks event definition."""

from .base import MarketEvent
from ...utils.decode_json import parse_json_double
import datetime


class GreeksEvent(MarketEvent):
    """
    Greeks event is a snapshot of the option price, Black-Scholes volatility and greeks.

    It represents the most recent information that is available about the corresponding values on the market at any given moment of time.

    Contains delta, gamma, theta, vega, rho, and volatility.
    """

    @property
    def event_flags(self) -> str:
        """Event flags."""
        return str(self.get("eventFlags", ""))

    @property
    def index(self) -> int:
        """Index of the greeks event."""
        value = self.get("index", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time(self) -> datetime.datetime | None:
        """Time of the greeks event."""
        value = self.get("time")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def sequence(self) -> int:
        """Sequence number of the event."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def price(self) -> float:
        """Option price."""
        value = self.get("price", 0.0)
        return parse_json_double(value)

    @property
    def volatility(self) -> float:
        """Implied volatility."""
        value = self.get("volatility", 0.0)
        return parse_json_double(value)

    @property
    def delta(self) -> float:
        """Option delta."""
        value = self.get("delta", 0.0)
        return parse_json_double(value)

    @property
    def gamma(self) -> float:
        """Option gamma."""
        value = self.get("gamma", 0.0)
        return parse_json_double(value)

    @property
    def theta(self) -> float:
        """Option theta."""
        value = self.get("theta", 0.0)
        return parse_json_double(value)

    @property
    def rho(self) -> float:
        """Option rho."""
        value = self.get("rho", 0.0)
        return parse_json_double(value)

    @property
    def vega(self) -> float:
        """Option vega."""
        value = self.get("vega", 0.0)
        return parse_json_double(value)
