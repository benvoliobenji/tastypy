import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.utils.decode_json import parse_date, parse_float


class EarningsInfo:
    """Dataclass containing historical earnings information for a symbol."""

    def __init__(self, data: dict[str, Any]) -> None:
        """
        Initialize earnings info from JSON data.

        Args:
            data: Dictionary containing earnings data from API.
        """
        self._data = data

    @property
    def occurred_date(self) -> datetime.date | None:
        """Date of earnings announcement."""
        value = self._data.get("occurred-date")
        return parse_date(value)

    @property
    def eps(self) -> float:
        """Earnings per share amount."""
        return parse_float(self._data.get("eps"), 0.0)

    def print_summary(self) -> None:
        """Print a plain text summary of the earnings report."""
        print(f"  Date: {self.occurred_date}, EPS: ${self.eps:.4f}")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the earnings report."""
        console = Console()

        table = Table(
            title="Earnings Details", show_header=True, header_style="bold cyan"
        )
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row(
            "Occurred Date", str(self.occurred_date) if self.occurred_date else "N/A"
        )
        table.add_row("EPS", f"${self.eps:.4f}")

        console.print(table)
