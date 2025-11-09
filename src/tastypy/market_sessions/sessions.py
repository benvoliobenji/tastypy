"""Market sessions list endpoint."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.market_sessions.enums import InstrumentCollection
from .base import SimpleSession
from tastypy.session import Session


class Sessions:
    """
    A class for fetching a list of market session timings for a date range.

    This endpoint returns session timing information for a specified instrument
    collection over a date range (maximum 9 months).
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the sessions fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._sessions: list[SimpleSession] = []

    def sync(
        self,
        to_date: datetime.date,
        from_date: datetime.date | None = None,
        instrument_collection: InstrumentCollection = InstrumentCollection.EQUITY,
    ) -> None:
        """
        Fetch market sessions for a date range.

        Args:
            to_date: End date (required).
            from_date: Start date (optional, defaults to today).
            instrument_collection: Instrument collection (default: Equity).

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If date range exceeds 9 months.
        """
        params: dict[str, str] = {
            "to-date": to_date.strftime("%Y-%m-%d"),
            "instrument-collection": instrument_collection.value,
        }

        if from_date:
            params["from-date"] = from_date.strftime("%Y-%m-%d")

            # Validate date range (9 months max)
            delta = to_date - from_date
            if delta.days > 270:  # Approximately 9 months
                raise ValueError(
                    "Date range cannot exceed 9 months (from-date to to-date)."
                )

        response = self._session.client.get("/market-time/sessions", params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse sessions - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._sessions = [SimpleSession(item) for item in items_data]

    @property
    def sessions(self) -> list[SimpleSession]:
        """List of market sessions returned from the API."""
        return self._sessions

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all sessions."""
        print(f"\n{'=' * 80}")
        print(f"MARKET SESSIONS ({len(self._sessions)} sessions)")
        print(f"{'=' * 80}")

        for session in self._sessions:
            session.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all sessions."""
        console = Console()

        # Create summary table with local time
        summary_table = Table(
            title=f"Market Sessions ({len(self._sessions)} sessions)",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Date", style="cyan", no_wrap=True)
        summary_table.add_column("Collection", style="yellow")
        summary_table.add_column("Start (UTC)", style="green")
        summary_table.add_column("Open (UTC)", style="green")
        summary_table.add_column("Close (UTC)", style="red")
        summary_table.add_column("Start (Local)", style="bright_green")
        summary_table.add_column("Open (Local)", style="bright_green")
        summary_table.add_column("Close (Local)", style="bright_red")

        for session in self._sessions:
            date_str = (
                session.session_date.strftime("%Y-%m-%d")
                if session.session_date
                else ""
            )
            start_str = (
                session.start_at.strftime("%H:%M") if session.start_at else "N/A"
            )
            open_str = session.open_at.strftime("%H:%M") if session.open_at else "N/A"
            close_str = (
                session.close_at.strftime("%H:%M") if session.close_at else "N/A"
            )

            # Local times
            start_local = (
                session.start_at.astimezone().strftime("%H:%M")
                if session.start_at
                else "N/A"
            )
            open_local = (
                session.open_at.astimezone().strftime("%H:%M")
                if session.open_at
                else "N/A"
            )
            close_local = (
                session.close_at.astimezone().strftime("%H:%M")
                if session.close_at
                else "N/A"
            )

            summary_table.add_row(
                date_str,
                session.instrument_collection,
                start_str,
                open_str,
                close_str,
                start_local,
                open_local,
                close_local,
            )

        console.print(
            Panel(
                summary_table,
                title="[bold blue]Market Sessions[/bold blue]",
                border_style="blue",
            )
        )
