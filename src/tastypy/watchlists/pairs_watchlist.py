"""Pairs watchlist data model."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.utils.decode_json import parse_int


class PairsWatchlist:
    """Represents a pairs trading watchlist."""

    def __init__(self, pairs_watchlist_json: dict[str, Any]) -> None:
        """
        Initialize a pairs watchlist from JSON data.

        Args:
            pairs_watchlist_json: Dictionary containing pairs watchlist data from API.
        """
        self._json = pairs_watchlist_json

    @property
    def name(self) -> str:
        """Name of the pairs watchlist."""
        return self._json.get("name", "")

    @property
    def order_index(self) -> int:
        """Order index for sorting watchlists."""
        return parse_int(self._json.get("order-index"), default=9999)

    @property
    def pairs_equations(self) -> list[dict[str, Any]]:
        """Pairs equations data as a list of equation dictionaries."""
        equations = self._json.get("pairs-equations", [])
        if isinstance(equations, list):
            return equations
        return []

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data for this pairs watchlist."""
        return self._json

    def print_summary(self) -> None:
        """Print a plain text summary of the pairs watchlist."""
        print(f"\nPairs Watchlist: {self.name}")
        print(f"  Order Index: {self.order_index}")
        print(f"  Pairs Equations ({len(self.pairs_equations)}):")
        for i, eq in enumerate(self.pairs_equations, 1):
            left_action = eq.get("left-action", "")
            left_symbol = eq.get("left-symbol", "")
            left_qty = eq.get("left-quantity", 0)
            right_action = eq.get("right-action", "")
            right_symbol = eq.get("right-symbol", "")
            right_qty = eq.get("right-quantity", 0)
            print(
                f"    {i}. {left_action} {left_qty}x {left_symbol} vs {right_action} {right_qty}x {right_symbol}"
            )

    def pretty_print(self) -> None:
        """Print a rich formatted output of the pairs watchlist."""
        console = Console()

        # Create header info
        header_lines = [
            f"[bold cyan]Name:[/bold cyan] {self.name}",
            f"[bold cyan]Order Index:[/bold cyan] {self.order_index}",
            f"[bold cyan]Pairs Count:[/bold cyan] {len(self.pairs_equations)}",
        ]

        console.print(
            Panel("\n".join(header_lines), title="Pairs Watchlist", border_style="cyan")
        )

        # Create table for pairs equations
        if self.pairs_equations:
            table = Table(
                title=f"Pairs Equations ({len(self.pairs_equations)})", show_header=True
            )
            table.add_column("#", style="yellow", justify="right")
            table.add_column("Left Side", style="green")
            table.add_column("Right Side", style="red")

            for i, eq in enumerate(self.pairs_equations, 1):
                left_action = eq.get("left-action", "")
                left_symbol = eq.get("left-symbol", "")
                left_qty = eq.get("left-quantity", 0)
                right_action = eq.get("right-action", "")
                right_symbol = eq.get("right-symbol", "")
                right_qty = eq.get("right-quantity", 0)

                left_side = f"{left_action} {left_qty}x {left_symbol}"
                right_side = f"{right_action} {right_qty}x {right_symbol}"

                table.add_row(str(i), left_side, right_side)

            console.print(table)
        else:
            console.print("[yellow]No pairs equations in this watchlist[/yellow]")
