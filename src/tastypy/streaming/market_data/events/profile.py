"""Profile event definition."""

from .base import MarketEvent
from tastypy.utils import parse_json_double
import datetime


class ProfileEvent(MarketEvent):
    """
    Profile event with instrument information.

    Contains description, trading status, and other instrument details.
    """

    @property
    def description(self) -> str:
        """Instrument description."""
        return str(self.get("description", ""))

    @property
    def short_sale_restriction(self) -> str:
        """Short sale restriction status."""
        return str(self.get("shortSaleRestriction", ""))

    @property
    def trading_status(self) -> str:
        """Current trading status."""
        return str(self.get("tradingStatus", ""))

    @property
    def status_reason(self) -> str:
        """Reason for current status."""
        return str(self.get("statusReason", ""))

    @property
    def halt_start_time(self) -> datetime.datetime | None:
        """Time when trading halt started."""
        value = self.get("haltStartTime")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def halt_end_time(self) -> datetime.datetime | None:
        """Time when trading halt is expected to end."""
        value = self.get("haltEndTime")
        if value and value != "NaN":
            return datetime.datetime.fromtimestamp(
                int(value) / 1000, tz=datetime.timezone.utc
            )
        return None

    @property
    def high_limit_price(self) -> float:
        """High limit price."""
        value = self.get("highLimitPrice", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def low_limit_price(self) -> float:
        """Low limit price."""
        value = self.get("lowLimitPrice", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def high_52_week_price(self) -> float:
        """52-week high price."""
        value = self.get("high52WeekPrice", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def low_52_week_price(self) -> float:
        """52-week low price."""
        value = self.get("low52WeekPrice", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def beta(self) -> float:
        """Beta value of the instrument."""
        value = self.get("beta", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def earnings_per_share(self) -> float:
        """Earnings per share."""
        value = self.get("earningsPerShare", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def dividend_frequency(self) -> float:
        """Dividend frequency."""
        value = self.get("dividendFrequency", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def ex_dividend_amount(self) -> float:
        """Ex-dividend amount."""
        value = self.get("exDividendAmount", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def ex_dividend_day_id(self) -> int:
        """Ex-dividend day ID."""
        value = self.get("exDividendDayId", 0)
        return int(value) if value not in ("NaN", None) else 0

    @property
    def shares(self) -> float:
        """Number of shares."""
        value = self.get("shares", 0.0)
        return parse_json_double(value, 0.0)

    @property
    def free_float(self) -> float:
        """Free float percentage."""
        value = self.get("freeFloat", 0.0)
        return parse_json_double(value, 0.0)
