from ..session import Session
from ..errors import translate_error_code
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class QuantityDecimalPrecisions:
    """Endpoint for fetching quantity decimal precision data."""

    _url_endpoint = "/instruments/quantity-decimal-precisions"
    _session: Session
    _data: dict

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self):
        """Fetch the latest quantity decimal precision data."""
        # This reports basically nothing, no idea until I understand how TastyTrade ACTUALLY uses this because their docs don't report anything useful
        response = self._session._client.get(f"{self._url_endpoint}")
        if response.status_code == 200:
            data = response.json()
            self._data = data.get("data", {})
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def instrument_type(self) -> str:
        return self._data.get("instrument-type", "")

    @property
    def minimum_increment_precision(self) -> int:
        return self._data.get("minimum-increment-precision", 0)

    @property
    def symbol(self) -> str:
        return self._data.get("symbol", "")

    @property
    def value(self) -> int:
        return self._data.get("value", 0)

    def print_summary(self) -> None:
        """Print a simple text summary of the quantity decimal precisions."""
        print(f"\n{'=' * 60}")
        print(f"QUANTITY DECIMAL PRECISIONS: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Instrument Type: {self.instrument_type}")
        print(f"Value: {self.value}")
        print(f"Minimum Increment Precision: {self.minimum_increment_precision}")
        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all quantity decimal precision data in a nicely formatted table."""
        console = Console()

        # Create precision information table
        precision_table = Table(
            title=f"Quantity Decimal Precisions: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        precision_table.add_column("Property", style="cyan", no_wrap=True)
        precision_table.add_column("Value", style="green")

        # Precision information
        precision_table.add_row("Symbol", str(self.symbol))
        precision_table.add_row("Instrument Type", str(self.instrument_type))
        precision_table.add_row("Value", str(self.value))
        precision_table.add_row(
            "Minimum Increment Precision", str(self.minimum_increment_precision)
        )

        # Print table
        console.print(
            Panel(
                precision_table,
                title="[bold blue]Quantity Decimal Precision Information[/bold blue]",
                border_style="blue",
            )
        )

    def __str__(self) -> str:
        return f"QuantityDecimalPrecisions({self.symbol}): {self.instrument_type} with precision {self.value}"
