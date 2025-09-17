from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Cryptocurrency:
    """Represents a cryptocurrency instrument with various properties."""

    _crypto_json: dict

    def __init__(self, crypto_json: dict):
        self._crypto_json = crypto_json

    @property
    def id(self) -> int:
        return self._crypto_json.get("id", 0)

    @property
    def active(self) -> bool:
        return self._crypto_json.get("active", False)

    @property
    def description(self) -> str:
        return self._crypto_json.get("description", "")

    @property
    def instrument_type(self) -> str:
        return self._crypto_json.get("instrument-type", "")

    @property
    def is_closing_only(self) -> bool:
        return self._crypto_json.get("is-closing-only", False)

    @property
    def short_description(self) -> str:
        return self._crypto_json.get("short-description", "")

    @property
    def streamer_symbol(self) -> str:
        return self._crypto_json.get("streamer-symbol", "")

    @property
    def symbol(self) -> str:
        return self._crypto_json.get("symbol", "")

    @property
    def tick_size(self) -> float:
        value = self._crypto_json.get("tick-size", 0.0)
        return float(value) if value is not None else 0.0

    def __str__(self) -> str:
        return f"Cryptocurrency({self.symbol}): {self.description}"

    def print_summary(self) -> None:
        """Print a simple text summary of the cryptocurrency."""
        print(f"\n{'=' * 60}")
        print(f"CRYPTOCURRENCY SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Description: {self.description}")
        print(f"Short Description: {self.short_description}")
        print(f"Instrument Type: {self.instrument_type}")
        print(f"ID: {self.id}")
        print(f"Active: {self.active}")
        print(f"Is Closing Only: {self.is_closing_only}")
        print(f"Streamer Symbol: {self.streamer_symbol}")
        print(f"Tick Size: {self.tick_size}")
        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all cryptocurrency data in a nicely formatted table."""
        console = Console()

        # Create cryptocurrency information table
        crypto_table = Table(
            title=f"Cryptocurrency: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        crypto_table.add_column("Property", style="cyan", no_wrap=True)
        crypto_table.add_column("Value", style="green")

        # Basic information
        crypto_table.add_row("Symbol", str(self.symbol))
        crypto_table.add_row("Description", str(self.description))
        crypto_table.add_row("Short Description", str(self.short_description))
        crypto_table.add_row("Instrument Type", str(self.instrument_type))
        crypto_table.add_row("ID", str(self.id))
        crypto_table.add_row("Active", "Yes" if self.active else "No")
        crypto_table.add_row("Is Closing Only", "Yes" if self.is_closing_only else "No")
        crypto_table.add_row("Streamer Symbol", str(self.streamer_symbol))
        crypto_table.add_row("Tick Size", f"{self.tick_size:g}")

        # Status information table
        status_table = Table(
            title="Status & Trading Information",
            show_header=True,
            header_style="bold green",
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Trading Status", "Active" if self.active else "Inactive")
        status_table.add_row(
            "Trading Mode", "Closing Only" if self.is_closing_only else "Full Trading"
        )
        status_table.add_row("Minimum Price Increment", f"{self.tick_size:g}")

        # Print all tables
        console.print(
            Panel(
                crypto_table,
                title="[bold blue]Cryptocurrency Details[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                status_table,
                title="[bold green]Trading Status[/bold green]",
                border_style="green",
            )
        )
