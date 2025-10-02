from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FutureETFEquivalent:
    _future_etf_equivalent_json: dict = {}

    def __init__(self, future_etf_equivalent_json: dict):
        self._future_etf_equivalent_json = future_etf_equivalent_json

    @property
    def share_quantity(self) -> int:
        return self._future_etf_equivalent_json.get("share-quantity", 0)

    @property
    def symbol(self) -> str:
        return self._future_etf_equivalent_json.get("symbol", "")

    def print_summary(self) -> None:
        """Print a simple text summary of the future ETF equivalent."""
        print(f"\n{'=' * 60}")
        print(f"FUTURE ETF EQUIVALENT SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Share Quantity: {self.share_quantity:,}")
        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all future ETF equivalent data in a nicely formatted table."""
        console = Console()

        # Create ETF equivalent information table
        etf_table = Table(
            title=f"Future ETF Equivalent: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        etf_table.add_column("Property", style="cyan", no_wrap=True)
        etf_table.add_column("Value", style="green")

        # ETF equivalent information
        etf_table.add_row("Symbol", str(self.symbol))
        etf_table.add_row("Share Quantity", f"{self.share_quantity:,}")

        # Print table
        console.print(
            Panel(
                etf_table,
                title="[bold blue]ETF Equivalent Information[/bold blue]",
                border_style="blue",
            )
        )

    def __str__(self) -> str:
        return f"FutureETFEquivalent({self.symbol}): {self.share_quantity} shares"
