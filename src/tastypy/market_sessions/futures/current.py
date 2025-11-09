"""Current futures session for specific exchange endpoint."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from tastypy.market_sessions.enums import InstrumentCollection
from ..base import CurrentSession
from tastypy.session import Session


class FuturesCurrentSession:
    """
    A class for fetching the current futures session for a specific exchange.

    This endpoint returns current session data for a single futures exchange.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the futures current session fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._current_session: CurrentSession | None = None

    def sync(self, instrument_collection: InstrumentCollection) -> None:
        """
        Fetch current futures session for the specified exchange.

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
            f"/market-time/futures/sessions/current/{instrument_collection.value}"
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
        """Current futures session for the specified exchange."""
        return self._current_session

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of the current session."""
        print(f"\n{'=' * 80}")
        print("CURRENT FUTURES SESSION")
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
                    title="Current Futures Session",
                    border_style="yellow",
                )
            )
