import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Futures:
    _futures_json: dict

    def __init__(self, futures_json: dict):
        self._futures_json = futures_json

    @property
    def symbol(self) -> str:
        return self._futures_json.get("symbol", "")

    @property
    def root_symbol(self) -> str:
        return self._futures_json.get("root-symbol", "")

    @property
    def streamer_symbol(self) -> str:
        return self._futures_json.get("streamer-symbol", "")

    @property
    def maturity_date(self) -> datetime.date | None:
        date_str = self._futures_json.get("maturity-date", "")
        if date_str:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    @property
    def expiration_date(self) -> datetime.date | None:
        date_str = self._futures_json.get("expiration-date", "")
        if date_str:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    @property
    def days_to_expiration(self) -> int:
        return self._futures_json.get("days-to-expiration", 0)

    @property
    def active_month(self) -> bool:
        return self._futures_json.get("active-month", False)

    @property
    def next_active_month(self) -> bool:
        return self._futures_json.get("next-active-month", False)

    @property
    def stops_trading_at(self) -> datetime.datetime | None:
        datetime_str = self._futures_json.get("stops-trading-at", "")
        if datetime_str:
            try:
                # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
                return datetime.datetime.fromisoformat(
                    datetime_str.replace("Z", "+00:00")
                )
            except ValueError:
                return None
        return None

    @property
    def expires_at(self) -> datetime.datetime | None:
        datetime_str = self._futures_json.get("expires-at", "")
        if datetime_str:
            try:
                # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
                return datetime.datetime.fromisoformat(
                    datetime_str.replace("Z", "+00:00")
                )
            except ValueError:
                return None
        return None

    def print_summary(self) -> None:
        """Print a simple text summary of the futures contract information."""
        print(f"\n{'=' * 60}")
        print(f"FUTURES SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Streamer Symbol: {self.streamer_symbol}")

        print(f"Maturity Date: {self.maturity_date}")
        print(f"Expiration Date: {self.expiration_date}")
        print(f"Days to Expiration: {self.days_to_expiration}")

        print(f"Active Month: {'Yes' if self.active_month else 'No'}")
        print(f"Next Active Month: {'Yes' if self.next_active_month else 'No'}")

        if self.stops_trading_at:
            print(f"Stops Trading At: {self.stops_trading_at}")
        if self.expires_at:
            print(f"Expires At: {self.expires_at}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all futures contract data in nicely formatted tables."""
        console = Console()

        # Create basic futures information table
        basic_table = Table(
            title=f"Futures Contract: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Symbol", str(self.symbol))
        basic_table.add_row("Root Symbol", str(self.root_symbol))
        basic_table.add_row("Streamer Symbol", str(self.streamer_symbol))

        # Contract dates table
        dates_table = Table(
            title="Contract Dates",
            show_header=True,
            header_style="bold green",
        )
        dates_table.add_column("Property", style="cyan")
        dates_table.add_column("Value", style="green")

        dates_table.add_row(
            "Maturity Date",
            str(self.maturity_date) if self.maturity_date else "N/A",
        )
        dates_table.add_row(
            "Expiration Date",
            str(self.expiration_date) if self.expiration_date else "N/A",
        )
        dates_table.add_row("Days to Expiration", str(self.days_to_expiration))

        # Contract status table
        status_table = Table(
            title="Contract Status",
            show_header=True,
            header_style="bold yellow",
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Active Month", "Yes" if self.active_month else "No")
        status_table.add_row(
            "Next Active Month", "Yes" if self.next_active_month else "No"
        )

        # Trading times table (only if there are times)
        trading_table = Table(
            title="Trading Times",
            show_header=True,
            header_style="bold cyan",
        )
        trading_table.add_column("Property", style="cyan")
        trading_table.add_column("Value", style="green")

        if self.stops_trading_at:
            trading_table.add_row("Stops Trading At", str(self.stops_trading_at))
        if self.expires_at:
            trading_table.add_row("Expires At", str(self.expires_at))

        # Print all tables
        console.print(
            Panel(
                basic_table,
                title="[bold blue]Basic Information[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                dates_table,
                title="[bold green]Contract Dates[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                status_table,
                title="[bold yellow]Contract Status[/bold yellow]",
                border_style="yellow",
            )
        )

        # Only show trading times table if there are times
        if trading_table.row_count > 0:
            console.print(
                Panel(
                    trading_table,
                    title="[bold cyan]Trading Times[/bold cyan]",
                    border_style="cyan",
                )
            )

    def __str__(self) -> str:
        return f"Futures({self.symbol}): Maturity {self.maturity_date}, Expiration {self.expiration_date}, Expires {self.expires_at}"
