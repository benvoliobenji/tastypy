"""Futures holidays for specific exchange endpoint."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from tastypy.market_sessions.enums import InstrumentCollection
from ..base import MarketCalendar
from tastypy.session import Session


class FuturesHolidays:
    """
    A class for fetching futures market holidays and half-days for a specific exchange.

    This endpoint returns a calendar of market holidays and early close days.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the futures holidays fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._calendars: list[MarketCalendar] = []

    def sync(self, instrument_collection: InstrumentCollection) -> None:
        """
        Fetch futures market holidays and half-days for the specified exchange.

        Args:
            instrument_collection: Futures exchange (CFE, CME, or Smalls).

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If invalid instrument collection provided.
        """
        # Validate it's a futures exchange
        valid_collections = [
            InstrumentCollection.CFE,
            InstrumentCollection.CME,
            InstrumentCollection.SMALLS,
        ]
        if instrument_collection not in valid_collections:
            raise ValueError(
                f"Invalid instrument collection. Must be one of: {', '.join([c.value for c in valid_collections])}"
            )

        response = self._session.client.get(
            f"/market-time/futures/holidays/{instrument_collection.value}"
        )

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
        print(f"FUTURES MARKET HOLIDAYS ({len(self._calendars)} calendars)")
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
                    title="Futures Holidays",
                    border_style="yellow",
                )
            )
