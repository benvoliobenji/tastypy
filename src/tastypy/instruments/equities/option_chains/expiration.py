import datetime
from ...common.strikes import Strikes
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class NestedOptionChainExpiration:
    """Represents an expiration in a nested equity options chain."""

    def __init__(self, expiration_json: dict):
        self._expiration_json = expiration_json

    @property
    def expiration_type(self) -> str:
        return self._expiration_json.get("expiration-type", "")

    @property
    def expiration_date(self) -> datetime.date | None:
        date_str = self._expiration_json.get("expiration-date")
        if date_str:
            return datetime.date.fromisoformat(date_str)
        return None

    @property
    def days_to_expiration(self) -> int:
        value = self._expiration_json.get("days-to-expiration", 0)
        return int(value) if value is not None else 0

    @property
    def settlement_type(self) -> str:
        return self._expiration_json.get("settlement-type", "")

    @property
    def strikes(self) -> list[Strikes]:
        strikes_data = self._expiration_json.get("strikes", [])
        return [Strikes(strike) for strike in strikes_data]

    def __str__(self) -> str:
        return f"NestedOptionChainExpiration(expiration_date={self.expiration_date}, days_to_expiration={self.days_to_expiration}, strikes={len(self.strikes)})"

    def print_summary(self) -> None:
        """Print a simple text summary of the expiration information."""
        print(f"\n{'=' * 60}")
        print(f"EXPIRATION SUMMARY: {self.expiration_date}")
        print(f"{'=' * 60}")
        print(f"Expiration Date: {self.expiration_date}")
        print(f"Days to Expiration: {self.days_to_expiration}")
        print(f"Expiration Type: {self.expiration_type}")
        print(f"Settlement Type: {self.settlement_type}")

        if self.strikes:
            strike_count = len(self.strikes)
            print(f"Available Strikes: {strike_count}")

            strike_prices = [strike.strike_price for strike in self.strikes]
            if strike_prices:
                print(
                    f"Strike Range: ${min(strike_prices):,.2f} - ${max(strike_prices):,.2f}"
                )

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all expiration data in a nicely formatted table."""
        console = Console()

        # Create expiration info table
        info_table = Table(
            title=f"Expiration: {self.expiration_date}",
            show_header=True,
            header_style="bold blue",
        )
        info_table.add_column("Property", style="cyan", no_wrap=True)
        info_table.add_column("Value", style="green")

        info_table.add_row("Expiration Date", str(self.expiration_date))
        info_table.add_row("Days to Expiration", str(self.days_to_expiration))
        info_table.add_row("Expiration Type", self.expiration_type)
        info_table.add_row("Settlement Type", self.settlement_type)
        info_table.add_row("Number of Strikes", str(len(self.strikes)))

        console.print(
            Panel(
                info_table,
                title="[bold blue]Expiration Details[/bold blue]",
                border_style="blue",
            )
        )

        # Display strikes if available
        if self.strikes:
            strikes_table = Table(
                title=f"Strikes ({len(self.strikes)} total)",
                show_header=True,
                header_style="bold green",
            )
            strikes_table.add_column("Strike Price", style="yellow")
            strikes_table.add_column("Call Symbol", style="green")
            strikes_table.add_column("Put Symbol", style="red")

            # Show first 20 strikes
            for strike in self.strikes[:20]:
                strikes_table.add_row(
                    f"${strike.strike_price:,.2f}", strike.call, strike.put
                )

            if len(self.strikes) > 20:
                strikes_table.add_row("...", f"({len(self.strikes) - 20} more)", "...")

            console.print(
                Panel(
                    strikes_table,
                    title="[bold green]Available Strikes[/bold green]",
                    border_style="green",
                )
            )
