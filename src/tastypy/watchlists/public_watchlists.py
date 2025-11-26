"""Public watchlists manager for TastyTrade API."""

from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session
from tastypy.watchlists.watchlist import Watchlist


class PublicWatchlists:
    """
    Manager for TastyWorks public watchlists.

    Public watchlists are curated by TastyTrade and available to all users.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the public watchlists manager.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._url_endpoint = "/public-watchlists"
        self._request_json_data: dict[str, Any] = {}
        self._watchlists: list[Watchlist] = []

    def sync(self, counts_only: bool = False) -> None:
        """
        Fetch all public watchlists.

        Args:
            counts_only: If True, only fetch counts without full data (default: False).

        Raises:
            translate_error_code: If the API request fails.
        """
        params: dict[str, Any] = {}
        if counts_only:
            params["counts-only"] = "true"

        response = self._session.client.get(self._url_endpoint, params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse watchlists - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._watchlists = [Watchlist(item) for item in items_data]

    def get_by_name(self, watchlist_name: str) -> Watchlist:
        """
        Fetch a specific public watchlist by name.

        Args:
            watchlist_name: The name of the watchlist to retrieve.

        Returns:
            Watchlist: The requested watchlist.

        Raises:
            translate_error_code: If the API request fails.
        """
        url = f"{self._url_endpoint}/{watchlist_name}"
        response = self._session.client.get(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Parse watchlist - API returns: {"data": {...}}
        data = response.json().get("data", {})
        return Watchlist(data)

    @property
    def watchlists(self) -> list[Watchlist]:
        """List of public watchlists."""
        return self._watchlists

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data from the last API call."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all public watchlists."""
        print(f"\n{'=' * 80}")
        print(f"PUBLIC WATCHLISTS ({len(self._watchlists)} total)")
        print(f"{'=' * 80}")

        for watchlist in self._watchlists:
            watchlist.print_summary()

    def pretty_print(self) -> None:
        """Print a rich formatted output of all public watchlists."""
        console = Console()

        # Create summary table
        table = Table(
            title=f"Public Watchlists ({len(self._watchlists)} total)", show_header=True
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Group", style="magenta")
        table.add_column("Order", style="yellow", justify="right")
        table.add_column("CMS ID", style="green")
        table.add_column("Entries", style="blue", justify="right")

        for watchlist in self._watchlists:
            table.add_row(
                watchlist.name,
                watchlist.group_name or "N/A",
                str(watchlist.order_index),
                watchlist.cms_id or "N/A",
                str(len(watchlist.watchlist_entries)),
            )

        console.print(table)
