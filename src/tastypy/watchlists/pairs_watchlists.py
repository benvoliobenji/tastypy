"""Pairs watchlists manager for TastyTrade API."""

from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session
from tastypy.watchlists.pairs_watchlist import PairsWatchlist


class PairsWatchlists:
    """
    Manager for TastyWorks pairs trading watchlists.

    Pairs watchlists track pairs of securities for pairs trading strategies.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the pairs watchlists manager.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._url_endpoint = "/pairs-watchlists"
        self._request_json_data: dict[str, Any] = {}
        self._watchlists: list[PairsWatchlist] = []

    def sync(self) -> None:
        """
        Fetch all pairs watchlists.

        Raises:
            translate_error_code: If the API request fails.
        """
        response = self._session.client.get(self._url_endpoint)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse watchlists - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._watchlists = [PairsWatchlist(item) for item in items_data]

    def get_by_name(self, pairs_watchlist_name: str) -> PairsWatchlist:
        """
        Fetch a specific pairs watchlist by name.

        Args:
            pairs_watchlist_name: The name of the pairs watchlist to retrieve.

        Returns:
            PairsWatchlist: The requested pairs watchlist.

        Raises:
            translate_error_code: If the API request fails.
        """
        url = f"{self._url_endpoint}/{pairs_watchlist_name}"
        response = self._session.client.get(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Parse watchlist - API returns: {"data": {...}}
        data = response.json().get("data", {})
        return PairsWatchlist(data)

    @property
    def watchlists(self) -> list[PairsWatchlist]:
        """List of pairs watchlists."""
        return self._watchlists

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data from the last API call."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all pairs watchlists."""
        print(f"\n{'=' * 80}")
        print(f"PAIRS WATCHLISTS ({len(self._watchlists)} total)")
        print(f"{'=' * 80}")

        for watchlist in self._watchlists:
            watchlist.print_summary()

    def pretty_print(self) -> None:
        """Print a rich formatted output of all pairs watchlists."""
        console = Console()

        # Create summary table
        table = Table(
            title=f"Pairs Watchlists ({len(self._watchlists)} total)", show_header=True
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Order", style="yellow", justify="right")

        for watchlist in self._watchlists:
            table.add_row(
                watchlist.name,
                str(watchlist.order_index),
            )

        console.print(table)
