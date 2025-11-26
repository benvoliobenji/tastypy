"""User watchlists manager for TastyTrade API."""

from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session
from tastypy.watchlists.watchlist import Watchlist


class UserWatchlists:
    """
    Manager for user-created watchlists.

    This class provides methods to create, retrieve, update, and delete
    watchlists for the authenticated user's account.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the user watchlists manager.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._url_endpoint = "/watchlists"
        self._request_json_data: dict[str, Any] = {}
        self._watchlists: list[Watchlist] = []

    def sync(self) -> None:
        """
        Fetch all watchlists for the authenticated user.

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

        self._watchlists = [Watchlist(item) for item in items_data]

    def get_by_name(self, watchlist_name: str) -> Watchlist:
        """
        Fetch a specific user watchlist by name.

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

    def create(
        self,
        name: str,
        watchlist_entries: list[dict[str, str]],
        group_name: str | None = None,
        order_index: int = 9999,
    ) -> Watchlist:
        """
        Create a new watchlist.

        Args:
            name: The watchlist name (required).
            watchlist_entries: List of instruments to watch. Each entry should be a dict
                with 'symbol' (required) and optionally 'instrument-type'.
            group_name: The group to which this watchlist belongs (optional).
            order_index: The order index of the watchlist (default: 9999).

        Returns:
            Watchlist: The newly created watchlist.

        Raises:
            translate_error_code: If the API request fails.

        Example:
            >>> entries = [
            ...     {"symbol": "AAPL"},
            ...     {"symbol": "MSFT", "instrument-type": "Equity"}
            ... ]
            >>> watchlist = user_watchlists.create("Tech Stocks", entries)
        """
        payload: dict[str, Any] = {
            "name": name,
            "watchlist-entries": watchlist_entries,
            "order-index": order_index,
        }

        if group_name:
            payload["group-name"] = group_name

        response = self._session.client.post(self._url_endpoint, json=payload)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        # Parse created watchlist - API returns: {"data": {...}}
        data = response.json().get("data", {})
        return Watchlist(data)

    def update(
        self,
        watchlist_name: str,
        name: str,
        watchlist_entries: list[dict[str, str]],
        group_name: str | None = None,
        order_index: int = 9999,
    ) -> Watchlist:
        """
        Replace all properties of a watchlist.

        Args:
            watchlist_name: The current name of the watchlist to update.
            name: The new watchlist name (required).
            watchlist_entries: List of instruments to watch. Each entry should be a dict
                with 'symbol' (required) and optionally 'instrument-type'.
            group_name: The group to which this watchlist belongs (optional).
            order_index: The order index of the watchlist (default: 9999).

        Returns:
            Watchlist: The updated watchlist.

        Raises:
            translate_error_code: If the API request fails.
        """
        url = f"{self._url_endpoint}/{watchlist_name}"
        payload: dict[str, Any] = {
            "name": name,
            "watchlist-entries": watchlist_entries,
            "order-index": order_index,
        }

        if group_name:
            payload["group-name"] = group_name

        response = self._session.client.put(url, json=payload)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Parse updated watchlist - API returns: {"data": {...}}
        data = response.json().get("data", {})
        return Watchlist(data)

    def delete(self, watchlist_name: str) -> Watchlist:
        """
        Delete a watchlist.

        Args:
            watchlist_name: The name of the watchlist to delete.

        Returns:
            Watchlist: The deleted watchlist data.

        Raises:
            translate_error_code: If the API request fails.
        """
        url = f"{self._url_endpoint}/{watchlist_name}"
        response = self._session.client.delete(url)

        # DELETE can return 200 (with body) or 204 (no content)
        if response.status_code not in [200, 204]:
            raise translate_error_code(response.status_code, response.text)

        # Parse deleted watchlist - API returns: {"data": {...}}
        # If 204, there's no body to parse
        if response.status_code == 204:
            return Watchlist({"name": watchlist_name, "watchlist-entries": []})

        data = response.json().get("data", {})
        return Watchlist(data)

    @property
    def watchlists(self) -> list[Watchlist]:
        """List of user watchlists."""
        return self._watchlists

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data from the last API call."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all user watchlists."""
        print(f"\n{'=' * 80}")
        print(f"USER WATCHLISTS ({len(self._watchlists)} total)")
        print(f"{'=' * 80}")

        for watchlist in self._watchlists:
            watchlist.print_summary()

    def pretty_print(self) -> None:
        """Print a rich formatted output of all user watchlists."""
        console = Console()

        # Create summary table
        table = Table(
            title=f"User Watchlists ({len(self._watchlists)} total)", show_header=True
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Group", style="magenta")
        table.add_column("Order", style="yellow", justify="right")
        table.add_column("Entries", style="blue", justify="right")

        for watchlist in self._watchlists:
            table.add_row(
                watchlist.name,
                watchlist.group_name or "N/A",
                str(watchlist.order_index),
                str(len(watchlist.watchlist_entries)),
            )

        console.print(table)
