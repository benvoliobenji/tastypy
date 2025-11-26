"""Individual symbol data model."""

from typing import Any

from rich.console import Console
from rich.table import Table


class SymbolData:
    """Represents data for an individual symbol."""

    def __init__(self, symbol_json: dict[str, Any]) -> None:
        """
        Initialize a symbol data object from JSON data.

        Args:
            symbol_json: Dictionary containing symbol data from API.
        """
        self._json = symbol_json

    @property
    def symbol(self) -> str:
        """Symbol ticker."""
        return self._json.get("symbol", "")

    @property
    def description(self) -> str:
        """Company name or description."""
        return self._json.get("description", "")

    @property
    def listed_market(self) -> str:
        """Listed market where the symbol trades."""
        return self._json.get("listed-market", "")

    @property
    def price_increments(self) -> str:
        """Price increment information."""
        return self._json.get("price-increments", "")

    @property
    def trading_hours(self) -> str:
        """Trading hours information."""
        return self._json.get("trading-hours", "")

    @property
    def options(self) -> bool:
        """Whether the symbol has listed options."""
        return bool(self._json.get("options", False))

    @property
    def instrument_type(self) -> str:
        """Type of instrument."""
        return self._json.get("instrument-type", "")

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data from the API."""
        return self._json

    def print_summary(self) -> None:
        """Print a plain text summary of the symbol data."""
        print(f"\nSymbol: {self.symbol}")
        print(f"  Description: {self.description}")
        print(f"  Listed Market: {self.listed_market}")
        print(f"  Instrument Type: {self.instrument_type}")
        print(f"  Has Options: {self.options}")
        print(f"  Price Increments: {self.price_increments}")
        print(f"  Trading Hours: {self.trading_hours}")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the symbol data."""
        console = Console()

        # Create main table
        table = Table(
            title=f"{self.symbol} - {self.description}",
            show_header=True,
            header_style="bold blue",
        )
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Add rows
        table.add_row("Symbol", self.symbol)
        table.add_row("Description", self.description)
        table.add_row("Listed Market", self.listed_market)
        table.add_row("Instrument Type", self.instrument_type)
        table.add_row("Has Options", "Yes" if self.options else "No")
        table.add_row("Price Increments", self.price_increments)
        table.add_row("Trading Hours", self.trading_hours)

        console.print(table)
