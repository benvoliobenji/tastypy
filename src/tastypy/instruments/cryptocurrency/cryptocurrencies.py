from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...errors import translate_error_code
from ...session import Session
from .cryptocurrency import Cryptocurrency


class Cryptocurrencies:
    """Endpoint for fetching and managing cryptocurrency instruments."""

    _url_endpoint = "/instruments/cryptocurrencies"
    _session: Session
    _tracked_cryptos: dict[str, Cryptocurrency] = {}

    def __init__(self, active_session: Session):
        self._session = active_session

    def add(self, symbol: str):
        """Add a cryptocurrency to the tracked list by its symbol."""
        self._tracked_cryptos.setdefault(symbol, Cryptocurrency({}))

    def remove(self, symbol: str):
        """Remove a cryptocurrency from the tracked list by its symbol."""
        self._tracked_cryptos.pop(symbol, None)

    def sync(self):
        """Fetch the latest data for all tracked cryptocurrencies."""
        if not self._tracked_cryptos:
            print(
                "No cryptocurrencies are being tracked. Use the add() method to track some."
            )
            return

        # Parse this as symbol[]={value1}&symbol[]={value2}
        params = {"symbol[]": list(self._tracked_cryptos.keys())}
        response = self._session._client.get(
            self._url_endpoint,
            params=params,
        )
        if response.status_code == 200:
            data = response.json()
            crypto_data = data.get("data", {}).get("items", [])
            for crypto_json in crypto_data:
                symbol = crypto_json.get("symbol", "")
                if symbol in self._tracked_cryptos:
                    self._tracked_cryptos[symbol] = Cryptocurrency(crypto_json)
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def tracked_cryptos(self) -> list[Cryptocurrency]:
        """Get a list of all currently tracked cryptocurrencies."""
        return list(self._tracked_cryptos.values())

    def __str__(self):
        return (
            f"Cryptocurrencies: {len(self._tracked_cryptos)} tracked cryptocurrencies"
        )

    def print_summary(self) -> None:
        """Print a simple text summary of all tracked cryptocurrencies."""
        print(f"\n{'=' * 60}")
        print("CRYPTOCURRENCIES SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Tracked Cryptocurrencies: {len(self._tracked_cryptos)}")

        if not self._tracked_cryptos:
            print("No cryptocurrencies are being tracked.")
            print("Use the add() method to track some cryptocurrencies.")
            print(f"{'=' * 60}\n")
            return

        # Group by active status
        active_count = 0
        inactive_count = 0
        closing_only_count = 0

        for crypto in self._tracked_cryptos.values():
            if crypto.active:
                active_count += 1
                if crypto.is_closing_only:
                    closing_only_count += 1
            else:
                inactive_count += 1

        print(f"Active Cryptocurrencies: {active_count}")
        print(f"Inactive Cryptocurrencies: {inactive_count}")
        print(f"Closing Only: {closing_only_count}")
        print()

        print("Cryptocurrency Details:")
        print("-" * 60)

        for i, (symbol, crypto) in enumerate(self._tracked_cryptos.items(), 1):
            print(f"{i:2d}. {symbol}")
            print(f"    Description: {crypto.description}")
            print(f"    Status: {'Active' if crypto.active else 'Inactive'}")
            if crypto.active and crypto.is_closing_only:
                print("    Mode: Closing Only")
            elif crypto.active:
                print("    Mode: Full Trading")
            print(f"    Tick Size: {crypto.tick_size:g}")
            if crypto.streamer_symbol:
                print(f"    Streamer Symbol: {crypto.streamer_symbol}")
            print()

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all tracked cryptocurrencies data in nicely formatted tables."""
        console = Console()

        if not self._tracked_cryptos:
            console.print(
                Panel(
                    "[yellow]No cryptocurrencies are being tracked.\nUse the add() method to track some cryptocurrencies.[/yellow]",
                    title="[bold blue]Cryptocurrencies Summary[/bold blue]",
                    border_style="blue",
                )
            )
            return

        # Summary statistics
        summary_table = Table(
            title="Cryptocurrencies Overview",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        # Calculate summary statistics
        active_count = 0
        inactive_count = 0
        closing_only_count = 0
        total_count = len(self._tracked_cryptos)

        for crypto in self._tracked_cryptos.values():
            if crypto.active:
                active_count += 1
                if crypto.is_closing_only:
                    closing_only_count += 1
            else:
                inactive_count += 1

        summary_table.add_row("Total Tracked", str(total_count))
        summary_table.add_row("Active", str(active_count))
        summary_table.add_row("Inactive", str(inactive_count))
        summary_table.add_row("Closing Only", str(closing_only_count))
        summary_table.add_row("Full Trading", str(active_count - closing_only_count))

        # Detailed cryptocurrencies table
        cryptos_table = Table(
            title="Tracked Cryptocurrencies",
            show_header=True,
            header_style="bold yellow",
        )
        cryptos_table.add_column("#", style="dim", width=3)
        cryptos_table.add_column("Symbol", style="cyan", no_wrap=True)
        cryptos_table.add_column("Description", style="blue")
        cryptos_table.add_column("Status", style="green")
        cryptos_table.add_column("Trading Mode", style="magenta")
        cryptos_table.add_column("Tick Size", style="yellow")
        cryptos_table.add_column("Streamer Symbol", style="dim")

        for i, (symbol, crypto) in enumerate(self._tracked_cryptos.items(), 1):
            # Determine status and trading mode
            status = "Active" if crypto.active else "Inactive"
            trading_mode = "N/A"
            if crypto.active:
                trading_mode = (
                    "Closing Only" if crypto.is_closing_only else "Full Trading"
                )

            cryptos_table.add_row(
                str(i),
                symbol,
                crypto.description[:30] if crypto.description else "N/A",
                status,
                trading_mode,
                f"{crypto.tick_size:g}" if crypto.tick_size else "N/A",
                crypto.streamer_symbol if crypto.streamer_symbol else "N/A",
            )

        # Additional details table for cryptocurrencies with interesting data
        details_table = Table(
            title="Additional Details",
            show_header=True,
            header_style="bold magenta",
        )
        details_table.add_column("Symbol", style="cyan")
        details_table.add_column("Property", style="yellow")
        details_table.add_column("Value", style="green")

        for symbol, crypto in self._tracked_cryptos.items():
            if crypto.id:
                details_table.add_row(symbol, "ID", str(crypto.id))

            if crypto.instrument_type:
                details_table.add_row(symbol, "Instrument Type", crypto.instrument_type)

            if (
                crypto.short_description
                and crypto.short_description != crypto.description
            ):
                details_table.add_row(
                    symbol, "Short Description", crypto.short_description
                )

        # Print all tables
        console.print(
            Panel(
                summary_table,
                title="[bold blue]Cryptocurrencies Overview[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                cryptos_table,
                title="[bold yellow]All Tracked Cryptocurrencies[/bold yellow]",
                border_style="yellow",
            )
        )

        # Only show details table if there are interesting details
        if details_table.row_count > 0:
            console.print(
                Panel(
                    details_table,
                    title="[bold magenta]Additional Details[/bold magenta]",
                    border_style="magenta",
                )
            )
