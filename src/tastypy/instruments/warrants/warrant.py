from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Warrant:
    _warrant_json: dict = {}

    def __init__(self, warrant_json: dict):
        self._warrant_json = warrant_json

    @property
    def active(self) -> bool:
        return self._warrant_json.get("active", False)

    @property
    def cusip(self) -> str:
        return self._warrant_json.get("cusip", "")

    @property
    def description(self) -> str:
        return self._warrant_json.get("description", "")

    @property
    def instrument_type(self) -> str:
        return self._warrant_json.get("instrument-type", "")

    @property
    def is_closing_only(self) -> bool:
        return self._warrant_json.get("is-closing-only", False)

    @property
    def listed_market(self) -> str:
        return self._warrant_json.get("listed-market", "")

    @property
    def symbol(self) -> str:
        return self._warrant_json.get("symbol", "")

    def print_summary(self) -> None:
        """Print a simple text summary of the warrant."""
        print(f"\n{'=' * 60}")
        print(f"WARRANT SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Description: {self.description}")
        print(f"Instrument Type: {self.instrument_type}")
        print(f"CUSIP: {self.cusip}")
        print(f"Listed Market: {self.listed_market}")
        print(f"Active: {self.active}")
        print(f"Is Closing Only: {self.is_closing_only}")
        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all warrant data in a nicely formatted table."""
        console = Console()

        # Create warrant information table
        warrant_table = Table(
            title=f"Warrant: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        warrant_table.add_column("Property", style="cyan", no_wrap=True)
        warrant_table.add_column("Value", style="green")

        # Warrant information
        warrant_table.add_row("Symbol", str(self.symbol))
        warrant_table.add_row("Description", str(self.description))
        warrant_table.add_row("Instrument Type", str(self.instrument_type))
        warrant_table.add_row("CUSIP", str(self.cusip))
        warrant_table.add_row("Listed Market", str(self.listed_market))
        warrant_table.add_row("Active", "Yes" if self.active else "No")
        warrant_table.add_row(
            "Is Closing Only", "Yes" if self.is_closing_only else "No"
        )

        # Print table
        console.print(
            Panel(
                warrant_table,
                title="[bold blue]Warrant Information[/bold blue]",
                border_style="blue",
            )
        )

    def __str__(self) -> str:
        return f"Warrant({self.symbol}): {self.description}"
