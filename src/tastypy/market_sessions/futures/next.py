"""Next futures session for specific exchange endpoint."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel

from tastypy.errors import translate_error_code
from tastypy.market_sessions.enums import InstrumentCollection
from ..base import NextSession
from tastypy.session import Session


class FuturesNextSession:
    """
    A class for fetching the next futures session for a specific exchange.

    This endpoint returns the next upcoming session for a futures exchange.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the futures next session fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._next_session: NextSession | None = None

    def sync(
        self,
        instrument_collection: InstrumentCollection,
        date: datetime.date | None = None,
    ) -> None:
        """
        Fetch next futures session for the specified exchange on or after the given date.

        Args:
            instrument_collection: Futures exchange (CFE, CME, or Smalls).
            date: Optional date to find session on or after.
                  If not provided, finds the next session from today.

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
            f"/market-time/futures/sessions/next/{instrument_collection.value}",
            params=params,
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
        """Next futures session for the specified exchange."""
        return self._next_session

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of the next session."""
        print(f"\n{'=' * 80}")
        print("NEXT FUTURES SESSION")
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
                    title="Next Futures Session",
                    border_style="yellow",
                )
            )
