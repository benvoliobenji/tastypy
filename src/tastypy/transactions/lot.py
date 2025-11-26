"""Lot data model for transaction lots."""

import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.utils.decode_json import parse_datetime, parse_float, parse_int, parse_date


class Lot:
    """Represents a lot within a transaction."""

    def __init__(self, lot_json: dict[str, Any]) -> None:
        """
        Initialize a lot object from JSON data.

        Args:
            lot_json: Dictionary containing lot data from API.
        """
        self._json = lot_json

    @property
    def id(self) -> str:
        """Unique identifier for the lot."""
        return self._json.get("id", "")

    @property
    def executed_at(self) -> datetime.datetime | None:
        """When the lot was executed."""
        return parse_datetime(self._json.get("executed-at"))

    @property
    def price(self) -> float:
        """Price of the lot."""
        return parse_float(self._json.get("price"))

    @property
    def quantity(self) -> float:
        """Quantity in the lot."""
        return parse_float(self._json.get("quantity"))

    @property
    def quantity_direction(self) -> str:
        """Direction of the quantity (Long/Short)."""
        return self._json.get("quantity-direction", "")

    @property
    def transaction_date(self) -> datetime.date | None:
        """Date of the transaction."""
        return parse_date(self._json.get("transaction-date"))

    @property
    def transaction_id(self) -> int:
        """ID of the parent transaction."""
        return parse_int(self._json.get("transaction-id"))

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data from the API."""
        return self._json

    def print_summary(self) -> None:
        """Print a plain text summary of the lot data."""
        print(f"  Lot ID: {self.id}")
        print(f"    Quantity: {self.quantity} ({self.quantity_direction})")
        print(f"    Price: ${self.price:.2f}")
        print(f"    Executed At: {self.executed_at}")
        print(f"    Transaction Date: {self.transaction_date}")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the lot data."""
        console = Console()

        table = Table(
            title=f"Lot {self.id}", show_header=True, header_style="bold blue"
        )
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row("Lot ID", self.id)
        table.add_row("Quantity", f"{self.quantity} ({self.quantity_direction})")
        table.add_row("Price", f"${self.price:.2f}")
        table.add_row(
            "Executed At", str(self.executed_at) if self.executed_at else "N/A"
        )
        table.add_row(
            "Transaction Date",
            str(self.transaction_date) if self.transaction_date else "N/A",
        )
        table.add_row("Transaction ID", str(self.transaction_id))

        console.print(table)
