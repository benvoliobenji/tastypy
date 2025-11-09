"""Current equities session endpoint."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from ..base import CurrentSession
from tastypy.session import Session


class EquitiesCurrentSession:
    """
    A class for fetching the current equities market session.

    This endpoint returns current session data for the equities market.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the equities current session fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._current_session: CurrentSession | None = None

    def sync(self, current_time: datetime.datetime | None = None) -> None:
        """
        Fetch current equities market session.

        Args:
            current_time: Optional datetime to base the current session on.
                         If not provided, uses current server time.

        Raises:
            translate_error_code: If the API request fails.
        """
        params = {}
        if current_time:
            # Format as ISO 8601 datetime
            params["current-time"] = current_time.isoformat()

        response = self._session.client.get(
            "/market-time/equities/sessions/current", params=params
        )

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse session - API returns: {"data": {...}}
        data = self._request_json_data.get("data", {})
        if data:
            self._current_session = CurrentSession(data)

    @property
    def current_session(self) -> CurrentSession | None:
        """Current equities market session."""
        return self._current_session

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of the current session."""
        print(f"\n{'=' * 80}")
        print("CURRENT EQUITIES SESSION")
        print(f"{'=' * 80}")

        if self._current_session:
            self._current_session.print_summary()
        else:
            print("No session data available")

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the current session."""
        console = Console()

        if self._current_session:
            self._current_session.pretty_print()
        else:
            console.print(
                Panel(
                    "[yellow]No session data available[/yellow]",
                    title="Current Equities Session",
                    border_style="yellow",
                )
            )
