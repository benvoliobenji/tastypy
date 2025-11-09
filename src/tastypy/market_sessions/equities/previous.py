"""Previous equities session endpoint."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from ..base import PreviousSession
from tastypy.session import Session


class EquitiesPreviousSession:
    """
    A class for fetching the previous equities market session.

    This endpoint returns the previous session for the equities market.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the equities previous session fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._previous_session: PreviousSession | None = None

    def sync(self, date: datetime.date | None = None) -> None:
        """
        Fetch previous equities market session before the given date.

        Args:
            date: Optional date to find session before.
                  If not provided, finds the previous session from today.

        Raises:
            translate_error_code: If the API request fails.
        """
        params = {}
        if date:
            params["date"] = date.strftime("%Y-%m-%d")

        response = self._session.client.get(
            "/market-time/equities/sessions/previous", params=params
        )

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse session - API returns: {"data": {...}}
        data = self._request_json_data.get("data", {})
        if data:
            self._previous_session = PreviousSession(data)

    @property
    def previous_session(self) -> PreviousSession | None:
        """Previous equities market session."""
        return self._previous_session

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of the previous session."""
        print(f"\n{'=' * 80}")
        print("PREVIOUS EQUITIES SESSION")
        print(f"{'=' * 80}")

        if self._previous_session:
            self._previous_session.print_summary()
        else:
            print("No session data available")

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the previous session."""
        console = Console()

        if self._previous_session:
            self._previous_session.pretty_print()
        else:
            console.print(
                Panel(
                    "[yellow]No session data available[/yellow]",
                    title="Previous Equities Session",
                    border_style="yellow",
                )
            )
