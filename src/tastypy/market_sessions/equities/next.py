"""Next equities session endpoint."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from ..base import NextSession
from tastypy.session import Session


class EquitiesNextSession:
    """
    A class for fetching the next equities market session.

    This endpoint returns the next upcoming session for the equities market.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the equities next session fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._next_session: NextSession | None = None

    def sync(self, date: datetime.date | None = None) -> None:
        """
        Fetch next equities market session on or after the given date.

        Args:
            date: Optional date to find session on or after.
                  If not provided, finds the next session from today.

        Raises:
            translate_error_code: If the API request fails.
        """
        params = {}
        if date:
            params["date"] = date.strftime("%Y-%m-%d")

        response = self._session.client.get(
            "/market-time/equities/sessions/next", params=params
        )

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse session - API returns: {"data": {...}}
        data = self._request_json_data.get("data", {})
        if data:
            self._next_session = NextSession(data)

    @property
    def next_session(self) -> NextSession | None:
        """Next equities market session."""
        return self._next_session

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of the next session."""
        print(f"\n{'=' * 80}")
        print("NEXT EQUITIES SESSION")
        print(f"{'=' * 80}")

        if self._next_session:
            self._next_session.print_summary()
        else:
            print("No session data available")

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the next session."""
        console = Console()

        if self._next_session:
            self._next_session.pretty_print()
        else:
            console.print(
                Panel(
                    "[yellow]No session data available[/yellow]",
                    title="Next Equities Session",
                    border_style="yellow",
                )
            )
