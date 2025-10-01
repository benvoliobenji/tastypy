from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class TickSizes:
    _tick_sizes_dict: dict

    def __init__(self, tick_sizes_dict: dict):
        self._tick_sizes_dict = tick_sizes_dict

    @property
    def symbol(self) -> str:
        return self._tick_sizes_dict.get("symbol", "")

    @property
    def threshold(self) -> float:
        value = self._tick_sizes_dict.get("threshold", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def value(self) -> float:
        value = self._tick_sizes_dict.get("value", 0.0)
        return float(value) if value is not None else 0.0

    def __str__(self) -> str:
        return f"TickSizes(symbol={self.symbol}, threshold={self.threshold}, value={self.value})"

    def print_summary(self) -> None:
        """Print a simple text summary of the tick sizes."""
        print(f"\n{'=' * 60}")
        print(f"TICK SIZES SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Threshold: {self.threshold}")
        print(f"Tick Size Value: {self.value}")
        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print tick sizes data in a nicely formatted table."""
        console = Console()

        # Create tick sizes information table
        tick_table = Table(
            title=f"Tick Sizes: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        tick_table.add_column("Property", style="cyan", no_wrap=True)
        tick_table.add_column("Value", style="green")

        # Tick size information
        tick_table.add_row("Symbol", str(self.symbol))
        tick_table.add_row("Threshold", f"{self.threshold:,.4f}")
        tick_table.add_row("Tick Size Value", f"{self.value:,.4f}")

        # Description table for explanation
        description_table = Table(
            title="Tick Size Information",
            show_header=True,
            header_style="bold yellow",
        )
        description_table.add_column("Field", style="cyan")
        description_table.add_column("Description", style="white")

        description_table.add_row(
            "Symbol", "The trading symbol for which these tick sizes apply"
        )
        description_table.add_row(
            "Threshold", "The price threshold above which this tick size rule applies"
        )
        description_table.add_row(
            "Tick Size Value", "The minimum price increment (tick size) for trading"
        )

        # Print all tables
        console.print(
            Panel(
                tick_table,
                title="[bold blue]Tick Size Details[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                description_table,
                title="[bold yellow]Field Descriptions[/bold yellow]",
                border_style="yellow",
            )
        )
