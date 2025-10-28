import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.utils.decode_json import parse_date, parse_float


class DividendInfo:
    """Dataclass containing historical dividend information for a symbol."""

    def __init__(self, data: dict[str, Any]) -> None:
        """
        Initialize dividend info from JSON data.

        Args:
            data: Dictionary containing dividend data from API.
        """
        self._data = data

    @property
    def occurred_date(self) -> datetime.date | None:
        """Date of dividend."""
        value = self._data.get("occurred-date")
        return parse_date(value)

    @property
    def amount(self) -> float:
        """Per share dividend amount."""
        return parse_float(self._data.get("amount"), 0.0)

    def print_summary(self) -> None:
        """Print a plain text summary of the dividend."""
        print(f"  Date: {self.occurred_date}, Amount: ${self.amount:.4f}")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the dividend."""
        console = Console()

        table = Table(
            title="Dividend Details", show_header=True, header_style="bold cyan"
        )
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row(
            "Occurred Date", str(self.occurred_date) if self.occurred_date else "N/A"
        )
        table.add_row("Amount", f"${self.amount:.4f}")

        console.print(table)
