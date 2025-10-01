from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Strikes:
    _strikes_dict: dict

    def __init__(self, strikes_dict: dict):
        self._strikes_dict = strikes_dict

    @property
    def strike_price(self) -> float:
        value = self._strikes_dict.get("strike-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def call(self) -> str:
        return self._strikes_dict.get("call", "")

    @property
    def call_streamer_symbol(self) -> str:
        return self._strikes_dict.get("call-streamer-symbol", "")

    @property
    def put(self) -> str:
        return self._strikes_dict.get("put", "")

    @property
    def put_streamer_symbol(self) -> str:
        return self._strikes_dict.get("put-streamer-symbol", "")

    def __str__(self) -> str:
        return f"Strikes(strike_price={self.strike_price}, call={self.call}, put={self.put})"

    def print_summary(self) -> None:
        """Print a simple text summary of the strike information."""
        print(f"\n{'=' * 60}")
        print(f"STRIKE SUMMARY: ${self.strike_price:,.2f}")
        print(f"{'=' * 60}")
        print(f"Strike Price: ${self.strike_price:,.2f}")
        print(f"Call Option: {self.call}")
        print(f"Call Streamer Symbol: {self.call_streamer_symbol}")
        print(f"Put Option: {self.put}")
        print(f"Put Streamer Symbol: {self.put_streamer_symbol}")
        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all strike data in a nicely formatted table."""
        console = Console()

        # Create strike information table
        strike_table = Table(
            title=f"Strike: ${self.strike_price:,.2f}",
            show_header=True,
            header_style="bold blue",
        )
        strike_table.add_column("Property", style="cyan", no_wrap=True)
        strike_table.add_column("Value", style="green")

        # Strike information
        strike_table.add_row("Strike Price", f"${self.strike_price:,.2f}")
        strike_table.add_row("Call Option", str(self.call))
        strike_table.add_row("Call Streamer Symbol", str(self.call_streamer_symbol))
        strike_table.add_row("Put Option", str(self.put))
        strike_table.add_row("Put Streamer Symbol", str(self.put_streamer_symbol))

        # Options overview table
        options_table = Table(
            title="Options Overview",
            show_header=True,
            header_style="bold green",
        )
        options_table.add_column("Option Type", style="cyan")
        options_table.add_column("Symbol", style="green")
        options_table.add_column("Streamer Symbol", style="yellow")

        if self.call:
            options_table.add_row(
                "Call", str(self.call), str(self.call_streamer_symbol)
            )
        if self.put:
            options_table.add_row("Put", str(self.put), str(self.put_streamer_symbol))

        # Print all tables
        console.print(
            Panel(
                strike_table,
                title="[bold blue]Strike Information[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                options_table,
                title="[bold green]Available Options[/bold green]",
                border_style="green",
            )
        )
