"""Watchlist data model."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.utils.decode_json import parse_int
from tastypy.watchlists.watchlist_entry import WatchlistEntry


class Watchlist:
    """Represents a user or public watchlist."""

    def __init__(self, watchlist_json: dict[str, Any]) -> None:
        """
        Initialize a watchlist from JSON data.

        Args:
            watchlist_json: Dictionary containing watchlist data from API.
        """
        self._json = watchlist_json
        self._entries: list[WatchlistEntry] = []

        # Parse watchlist entries
        entries_data = self._json.get("watchlist-entries", [])
        if isinstance(entries_data, list):
            self._entries = [WatchlistEntry(entry) for entry in entries_data]

    @property
    def name(self) -> str:
        """Name of the watchlist."""
        return self._json.get("name", "")

    @property
    def group_name(self) -> str:
        """Group name of the watchlist."""
        return self._json.get("group-name", "")

    @property
    def order_index(self) -> int:
        """Order index for sorting watchlists."""
        return parse_int(self._json.get("order-index"), default=9999)

    @property
    def cms_id(self) -> str:
        """CMS ID (for public watchlists)."""
        return self._json.get("cms-id", "")

    @property
    def watchlist_entries(self) -> list[WatchlistEntry]:
        """List of entries in this watchlist."""
        return self._entries

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data for this watchlist."""
        return self._json

    def to_dict(self) -> dict[str, Any]:
        """
        Convert watchlist to dictionary for API requests.

        Returns:
            Dictionary suitable for POST/PUT requests.
        """
        result: dict[str, Any] = {
            "name": self.name,
            "watchlist-entries": [entry.to_dict() for entry in self._entries],
        }

        if self.group_name:
            result["group-name"] = self.group_name

        if self.order_index != 9999:
            result["order-index"] = self.order_index

        return result

    def print_summary(self) -> None:
        """Print a plain text summary of the watchlist."""
        print(f"\nWatchlist: {self.name}")
        if self.group_name:
            print(f"  Group: {self.group_name}")
        print(f"  Order Index: {self.order_index}")
        if self.cms_id:
            print(f"  CMS ID: {self.cms_id}")
        print(f"  Entries ({len(self._entries)}):")
        for entry in self._entries:
            entry.print_summary()

    def pretty_print(self) -> None:
        """Print a rich formatted output of the watchlist."""
        console = Console()

        # Create header info
        header_lines = [f"[bold cyan]Name:[/bold cyan] {self.name}"]
        if self.group_name:
            header_lines.append(f"[bold cyan]Group:[/bold cyan] {self.group_name}")
        header_lines.append(f"[bold cyan]Order Index:[/bold cyan] {self.order_index}")
        if self.cms_id:
            header_lines.append(f"[bold cyan]CMS ID:[/bold cyan] {self.cms_id}")

        console.print(
            Panel("\n".join(header_lines), title="Watchlist", border_style="cyan")
        )

        # Create table for entries
        if self._entries:
            table = Table(
                title=f"Watchlist Entries ({len(self._entries)})", show_header=True
            )
            table.add_column("Symbol", style="magenta", no_wrap=True)
            table.add_column("Instrument Type", style="cyan")

            for entry in self._entries:
                table.add_row(
                    entry.symbol,
                    entry.instrument_type or "N/A",
                )

            console.print(table)
        else:
            console.print("[yellow]No entries in this watchlist[/yellow]")
