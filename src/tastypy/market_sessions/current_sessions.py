"""Current market sessions endpoint."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.market_sessions.enums import InstrumentCollection
from .base import CurrentSession
from tastypy.session import Session


class CurrentSessions:
    """
    A class for fetching current session timings for multiple instrument collections.

    This endpoint returns current session data for one or more instrument collections.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the current sessions fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._sessions: list[CurrentSession] = []

    def sync(self, instrument_collections: list[InstrumentCollection]) -> None:
        """
        Fetch current market sessions for the given instrument collections.

        Args:
            instrument_collections: List of instrument collections to fetch.

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If instrument_collections list is empty.
        """
        if not instrument_collections:
            raise ValueError("At least one instrument collection is required.")

        # API expects: instrument-collections[]=value1&instrument-collections[]=value2
        params = {}
        for collection in instrument_collections:
            params.setdefault("instrument-collections[]", []).append(collection.value)

        response = self._session.client.get(
            "/market-time/sessions/current", params=params
        )

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse sessions - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._sessions = [CurrentSession(item) for item in items_data]

    @property
    def sessions(self) -> list[CurrentSession]:
        """List of current market sessions returned from the API."""
        return self._sessions

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all current sessions."""
        print(f"\n{'=' * 80}")
        print(f"CURRENT MARKET SESSIONS ({len(self._sessions)} collections)")
        print(f"{'=' * 80}")

        for session in self._sessions:
            session.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all current sessions."""
        console = Console()

        # Create summary table with local times
        summary_table = Table(
            title=f"Current Market Sessions ({len(self._sessions)} collections)",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Collection", style="cyan", no_wrap=True)
        summary_table.add_column("State", style="yellow")
        summary_table.add_column("Open (UTC)", style="green")
        summary_table.add_column("Close (UTC)", style="red")
        summary_table.add_column("Open (Local)", style="bright_green")
        summary_table.add_column("Close (Local)", style="bright_red")
        summary_table.add_column("Next Session", style="magenta")

        for session in self._sessions:
            open_str = session.open_at.strftime("%H:%M") if session.open_at else "N/A"
            close_str = (
                session.close_at.strftime("%H:%M") if session.close_at else "N/A"
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
            next_str = (
                session.next_session.session_date.strftime("%Y-%m-%d")
                if session.next_session and session.next_session.session_date
                else "N/A"
            )

            summary_table.add_row(
                session.instrument_collection,
                f"[bold]{session.state}[/bold]",
                open_str,
                close_str,
                open_local,
                close_local,
                next_str,
            )

        console.print(
            Panel(
                summary_table,
                title="[bold blue]Current Market Sessions[/bold blue]",
                border_style="blue",
            )
        )
