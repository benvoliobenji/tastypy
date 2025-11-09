"""Current futures sessions (all exchanges) endpoint."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from ..base import CurrentSession
from tastypy.session import Session


class FuturesCurrentSessionsAll:
    """
    A class for fetching current futures sessions for all exchanges.

    This endpoint returns current session data for all futures exchanges.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the futures current sessions (all) fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._sessions: list[CurrentSession] = []

    def sync(self) -> None:
        """
        Fetch current futures sessions for all exchanges.

        Raises:
            translate_error_code: If the API request fails.
        """
        response = self._session.client.get("/market-time/futures/sessions/current")

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
        """List of current futures sessions for all exchanges."""
        return self._sessions

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all current futures sessions."""
        print(f"\n{'=' * 80}")
        print(f"CURRENT FUTURES SESSIONS (ALL) - {len(self._sessions)} exchanges")
        print(f"{'=' * 80}")

        for session in self._sessions:
            session.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all current futures sessions."""
        console = Console()

        if self._sessions:
            # Create summary table with local times
            summary_table = Table(
                title=f"Current Futures Sessions ({len(self._sessions)} exchanges)",
                show_header=True,
                header_style="bold blue",
            )
            summary_table.add_column("Exchange", style="cyan", no_wrap=True)
            summary_table.add_column("State", style="yellow")
            summary_table.add_column("Open (UTC)", style="green")
            summary_table.add_column("Close (UTC)", style="red")
            summary_table.add_column("Open (Local)", style="bright_green")
            summary_table.add_column("Close (Local)", style="bright_red")

            for session in self._sessions:
                open_str = (
                    session.open_at.strftime("%H:%M") if session.open_at else "N/A"
                )
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

                summary_table.add_row(
                    session.instrument_collection,
                    f"[bold]{session.state}[/bold]",
                    open_str,
                    close_str,
                    open_local,
                    close_local,
                )

            console.print(
                Panel(
                    summary_table,
                    title="[bold blue]Current Futures Sessions[/bold blue]",
                    border_style="blue",
                )
            )
        else:
            console.print(
                Panel(
                    "[yellow]No session data available[/yellow]",
                    title="Current Futures Sessions",
                    border_style="yellow",
                )
            )
