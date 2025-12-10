"""Order event definition."""

from .base import MarketEvent
from ...utils.decode_json import parse_json_double
import datetime


class OrderEvent(MarketEvent):
    """
    Order event is a snapshot for a full available market depth for a symbol.

    The collection of order events of a symbol represents the most recent information
    that is available about orders on the market at any given moment of time.
    """

    @property
    def market_maker(self) -> str:
        """Market maker identifier."""
        return str(self.get("marketMaker", ""))

    @property
    def event_flags(self) -> int:
        """Event flags."""
        value = self.get("eventFlags", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def index(self) -> int:
        """Order event index."""
        value = self.get("index", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def time(self) -> datetime.datetime | None:
        """Time of the order event."""
        value = self.get("time")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def time_nano_part(self) -> int:
        """Nanosecond part of the order event time."""
        value = self.get("timeNanoPart", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def sequence(self) -> int:
        """Order event sequence number."""
        value = self.get("sequence", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def source(self) -> str:
        """Source of the order event."""
        return str(self.get("source", ""))

    @property
    def action(self) -> str:
        """Action of the order event."""
        return str(self.get("action", ""))

    @property
    def action_time(self) -> datetime.datetime | None:
        """Time of the action in the order event."""
        value = self.get("actionTime")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def order_id(self) -> int:
        """Order identifier."""
        value = self.get("orderId", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def aux_order_id(self) -> int:
        """Auxiliary order identifier."""
        value = self.get("auxOrderId", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def price(self) -> float:
        """Order price."""
        value = self.get("price", 0.0)
        return parse_json_double(value)

    @property
    def size(self) -> float:
        """Order size."""
        value = self.get("size", 0.0)
        return parse_json_double(value)

    @property
    def executed_size(self) -> float:
        """Executed size of the order."""
        value = self.get("executedSize", 0.0)
        return parse_json_double(value)

    @property
    def count(self) -> int:
        """Number of orders at this price level."""
        value = self.get("count", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def exchange_code(self) -> str:
        """Exchange code for the order."""
        return str(self.get("exchangeCode", ""))

    @property
    def order_side(self) -> str:
        """Side of the order."""
        return str(self.get("orderSide", ""))

    @property
    def scope(self) -> str:
        """Scope of the order."""
        return str(self.get("scope", ""))

    @property
    def trade_id(self) -> int:
        """Trade identifier associated with the order."""
        value = self.get("tradeId", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def trade_price(self) -> float:
        """Trade price associated with the order."""
        value = self.get("tradePrice", 0.0)
        return parse_json_double(value)

    @property
    def trade_size(self) -> float:
        """Trade size associated with the order."""
        value = self.get("tradeSize", 0.0)
        return parse_json_double(value)
