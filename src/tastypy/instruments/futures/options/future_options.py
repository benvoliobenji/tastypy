from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ....errors import translate_error_code
from ....session import Session
from ..common.future_option import FutureOption


class FutureOptions:
    _session: Session
    _future_option: FutureOption
    _endpoint_url: str = ""

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self, symbol: str):
        """Fetch the latest data for the specified future option symbol. NOTE: Uses TW symbology (./ESZ9 EW4U9 190927P2975)"""
        # Small linting
        # The symbol provided must start with a "./"
        if not symbol.startswith("./"):
            raise ValueError("Symbol must start with './' for futures options.")

        # The API expects the symbol to be UTF-8 encoded
        # For example:
        # ./ESU3 E1DQ3 230803P3860 should be .%2FESU3%20E1DQ3%20230803P3860 in the API call
        utf_symbol = symbol.replace(" ", "%20").replace("/", "%2F")

        self._endpoint_url = f"/instruments/future-options/{utf_symbol}"

        response = self._session.client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            data_dict = data.get("data", {})
            self._future_option = FutureOption(data_dict)
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def future_option(self) -> FutureOption:
        """Get the currently loaded future option."""
        if not hasattr(self, "_future_option"):
            raise ValueError("No future option data loaded. Call sync() first.")
        return self._future_option

    def print_summary(self) -> None:
        """Print a simple text summary of the future options data."""
        print(f"\n{'=' * 60}")
        print("FUTURE OPTIONS SUMMARY")
        print(f"{'=' * 60}")

        if hasattr(self, "_future_option"):
            print("Future Option Loaded: Yes")
            print(f"Symbol: {self.future_option.symbol}")
            print(f"Underlying Symbol: {self.future_option.underlying_symbol}")
            print(f"Option Type: {self.future_option.option_type}")
            print(f"Strike Price: {self.future_option.strike_price}")
            print(f"Expiration Date: {self.future_option.expiration_date}")
            print(f"Days to Expiration: {self.future_option.days_to_expiration}")
            print(f"Exchange: {self.future_option.exchange}")
            print(f"Active: {'Yes' if self.future_option.active else 'No'}")
        else:
            print("Future Option Loaded: No - Call sync() first")
            print("No future option data available")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print the future options data in nicely formatted tables."""
        console = Console()

        # Check if data is loaded
        if not hasattr(self, "_future_option"):
            error_table = Table(
                title="Future Options",
                show_header=True,
                header_style="bold red",
            )
            error_table.add_column("Status", style="red", justify="center")
            error_table.add_row("No data loaded - Please call sync() first")

            console.print(
                Panel(
                    error_table,
                    title="[bold red]Error[/bold red]",
                    border_style="red",
                )
            )
            return

        # Create overview table
        overview_table = Table(
            title="Future Options Overview",
            show_header=True,
            header_style="bold blue",
        )
        overview_table.add_column("Property", style="cyan", no_wrap=True)
        overview_table.add_column("Value", style="green")

        overview_table.add_row("Data Status", "✓ Loaded Successfully")
        overview_table.add_row("Symbol", str(self.future_option.symbol))
        overview_table.add_row(
            "Underlying Symbol", str(self.future_option.underlying_symbol)
        )
        overview_table.add_row("Option Type", str(self.future_option.option_type))
        overview_table.add_row(
            "Strike Price", f"{self.future_option.strike_price:,.2f}"
        )
        overview_table.add_row(
            "Expiration Date",
            (
                str(self.future_option.expiration_date)
                if self.future_option.expiration_date
                else "N/A"
            ),
        )
        overview_table.add_row(
            "Days to Expiration", str(self.future_option.days_to_expiration)
        )
        overview_table.add_row("Exchange", str(self.future_option.exchange))
        overview_table.add_row("Active", "Yes" if self.future_option.active else "No")

        console.print(
            Panel(
                overview_table,
                title="[bold blue]Overview[/bold blue]",
                border_style="blue",
            )
        )

        # Show detailed future option information using the future_option's pretty_print method
        console.print(
            "\n[bold white]📊 Detailed Future Option Information:[/bold white]\n"
        )
        self.future_option.pretty_print()
