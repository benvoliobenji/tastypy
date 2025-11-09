"""Equities holidays endpoint."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from ..base import MarketCalendar
from tastypy.session import Session


class EquitiesHolidays:
    """
    A class for fetching equities market holidays and half-days.

    This endpoint returns a calendar of market holidays and early close days.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the equities holidays fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._calendars: list[MarketCalendar] = []

    def sync(self) -> None:
        """
        Fetch equities market holidays and half-days.

        Raises:
            translate_error_code: If the API request fails.
        """
        response = self._session.client.get("/market-time/equities/holidays")

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse calendar - API returns: {"data": {"market-holidays": [...], "market-half-days": [...]}}
        data = self._request_json_data.get("data", {})
        if data:
            # Create a single MarketCalendar from the data
            self._calendars = [MarketCalendar(data)]

    @property
    def calendars(self) -> list[MarketCalendar]:
        """List of market calendars returned from the API."""
        return self._calendars

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of the holidays."""
        print(f"\n{'=' * 80}")
        print(f"EQUITIES MARKET HOLIDAYS ({len(self._calendars)} calendars)")
        print(f"{'=' * 80}")

        for calendar in self._calendars:
            calendar.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the holidays."""
        console = Console()

        if self._calendars:
            for calendar in self._calendars:
                calendar.pretty_print()
        else:
            console.print(
                Panel(
                    "[yellow]No holiday data available[/yellow]",
                    title="Equities Holidays",
                    border_style="yellow",
                )
            )
