"""Market calendar model."""

from typing import Any

from rich.console import Console
from rich.table import Table


class MarketCalendar:
    """
    Represents market holidays and half-days calendar.

    Contains information about market closures and early close days.
    """

    def __init__(self, json_data: dict[str, Any]) -> None:
        """
        Initialize a market calendar from API JSON data.

        Args:
            json_data: Raw JSON data from the API.
        """
        self._json = json_data

    @property
    def market_holidays(self) -> list[str]:
        """List of market holiday dates."""
        holidays = self._json.get("market-holidays", [])
        # Handle both list and dict formats
        if isinstance(holidays, list):
            return holidays
        return []

    @property
    def market_half_days(self) -> list[str]:
        """List of market half-day (early close) dates."""
        half_days = self._json.get("market-half-days", [])
        # Handle both list and dict formats
        if isinstance(half_days, list):
            return half_days
        return []

    def print_summary(self) -> None:
        """Print a plain text summary of the market calendar."""
        print("\n  Market Calendar:")
        print(f"    Holidays: {len(self.market_holidays)} entries")
        print(f"    Half Days: {len(self.market_half_days)} entries")

        if self.market_holidays:
            print("\n    Upcoming Holidays:")
            for date in self.market_holidays[:5]:
                print(f"      {date}")

        if self.market_half_days:
            print("\n    Upcoming Half Days:")
            for date in self.market_half_days[:5]:
                print(f"      {date}")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the market calendar."""
        console = Console()

        # Holidays table
        if self.market_holidays:
            holiday_table = Table(title="Market Holidays")
            holiday_table.add_column("Date", style="cyan")

            for date in self.market_holidays[:20]:
                holiday_table.add_row(date)

            console.print(holiday_table)

        # Half days table
        if self.market_half_days:
            half_day_table = Table(title="Market Half Days (Early Close)")
            half_day_table.add_column("Date", style="cyan")

            for date in self.market_half_days[:20]:
                half_day_table.add_row(date)

            console.print(half_day_table)
