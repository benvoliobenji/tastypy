"""Previous futures session for specific exchange endpoint."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from tastypy.market_sessions.enums import InstrumentCollection
from ..base import PreviousSession
from tastypy.session import Session


class FuturesPreviousSession:
    """
    A class for fetching the previous futures session for a specific exchange.

    This endpoint returns the previous session for a futures exchange.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the futures previous session fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._previous_session: PreviousSession | None = None

    def sync(
        self,
        instrument_collection: InstrumentCollection,
        date: datetime.date | None = None,
    ) -> None:
        """
        Fetch previous futures session for the specified exchange before the given date.

        Args:
            instrument_collection: Futures exchange (CFE, CME, or Smalls).
            date: Optional date to find session before.
                  If not provided, finds the previous session from today.

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

        params = {}
        if date:
            params["date"] = date.strftime("%Y-%m-%d")

        response = self._session.client.get(
            f"/market-time/futures/sessions/previous/{instrument_collection.value}",
            params=params,
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
        """Previous futures session for the specified exchange."""
        return self._previous_session

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of the previous session."""
        print(f"\n{'=' * 80}")
        print("PREVIOUS FUTURES SESSION")
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
                    title="Previous Futures Session",
                    border_style="yellow",
                )
            )
