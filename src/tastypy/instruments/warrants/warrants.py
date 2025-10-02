from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...errors import translate_error_code
from ...session import Session
from .warrant import Warrant


class Warrants:
    """Endpoint for fetching and managing warrant instruments."""

    _url_endpoint = "/instruments/warrants"
    _session: Session
    _tracked_warrants: dict[str, Warrant] = {}

    def __init__(self, active_session: Session):
        self._session = active_session

    def add(self, symbol: str):
        """Add a warrant to the tracked list by its symbol."""
        self._tracked_warrants.setdefault(symbol, Warrant({}))

    def remove(self, symbol: str):
        """Remove a warrant from the tracked list by its symbol."""
        self._tracked_warrants.pop(symbol, None)

    def sync(self):
        """Fetch the latest data for all tracked warrants."""
        if not self._tracked_warrants:
            print("No warrants are being tracked. Use the add() method to track some.")
            return

        # Parse this as symbol[]={value1}&symbol[]={value2}
        params = {"symbol[]": list(self._tracked_warrants.keys())}
        response = self._session._client.get(
            self._url_endpoint,
            params=params,
        )
        if response.status_code == 200:
            data = response.json()
            crypto_data = data.get("data", {}).get("items", [])
            for crypto_json in crypto_data:
                symbol = crypto_json.get("symbol", "")
                if symbol in self._tracked_warrants:
                    self._tracked_warrants[symbol] = Warrant(crypto_json)
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def tracked_warrants(self) -> list[Warrant]:
        """Get a list of all currently tracked warrants."""
        return list(self._tracked_warrants.values())

    def __str__(self):
        return f"Warrants: {len(self._tracked_warrants)} tracked warrants"

    def print_summary(self) -> None:
        """Print a simple text summary of all tracked warrants."""
        print(f"\n{'=' * 60}")
        print("WARRANTS SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Tracked Warrants: {len(self._tracked_warrants)}")

        if not self._tracked_warrants:
            print("No warrants are being tracked.")
            print("Use the add() method to track some warrants.")
            print(f"{'=' * 60}\n")
            return

        # Group by active status
        active_count = 0
        inactive_count = 0
        closing_only_count = 0

        for warrant in self._tracked_warrants.values():
            if warrant.active:
                active_count += 1
                if warrant.is_closing_only:
                    closing_only_count += 1
            else:
                inactive_count += 1

        print(f"Active Warrants: {active_count}")
        print(f"Inactive Warrants: {inactive_count}")
        print(f"Closing Only: {closing_only_count}")
        print()

        print("Warrant Details:")
        print("-" * 60)

        for i, (symbol, warrant) in enumerate(self._tracked_warrants.items(), 1):
            print(f"{i:2d}. {symbol}")
            print(f"    Description: {warrant.description}")
            print(f"    Instrument Type: {warrant.instrument_type}")
            print(f"    CUSIP: {warrant.cusip}")
            print(f"    Listed Market: {warrant.listed_market}")
            print(f"    Status: {'Active' if warrant.active else 'Inactive'}")
            if warrant.is_closing_only:
                print("    Mode: Closing Only")
            print()

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all tracked warrants data in nicely formatted tables."""
        console = Console()

        if not self._tracked_warrants:
            console.print(
                Panel(
                    "[yellow]No warrants are being tracked.\nUse the add() method to track some warrants.[/yellow]",
                    title="[bold blue]Warrants Summary[/bold blue]",
                    border_style="blue",
                )
            )
            return

        # Summary statistics
        summary_table = Table(
            title="Warrants Overview",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        # Calculate summary statistics
        active_count = 0
        inactive_count = 0
        closing_only_count = 0
        total_count = len(self._tracked_warrants)

        for warrant in self._tracked_warrants.values():
            if warrant.active:
                active_count += 1
                if warrant.is_closing_only:
                    closing_only_count += 1
            else:
                inactive_count += 1

        summary_table.add_row("Total Tracked", str(total_count))
        summary_table.add_row("Active", str(active_count))
        summary_table.add_row("Inactive", str(inactive_count))
        summary_table.add_row("Closing Only", str(closing_only_count))

        # Detailed warrants table
        warrants_table = Table(
            title="Tracked Warrants",
            show_header=True,
            header_style="bold yellow",
        )
        warrants_table.add_column("#", style="dim", width=3)
        warrants_table.add_column("Symbol", style="cyan", no_wrap=True)
        warrants_table.add_column("Description", style="blue")
        warrants_table.add_column("Instrument Type", style="magenta")
        warrants_table.add_column("CUSIP", style="yellow")
        warrants_table.add_column("Listed Market", style="green")
        warrants_table.add_column("Status", style="green")
        warrants_table.add_column("Closing Only", style="red")

        for i, (symbol, warrant) in enumerate(self._tracked_warrants.items(), 1):
            # Determine status
            status = "Active" if warrant.active else "Inactive"
            closing_only = "Yes" if warrant.is_closing_only else "No"

            warrants_table.add_row(
                str(i),
                symbol,
                warrant.description[:30] if warrant.description else "N/A",
                warrant.instrument_type if warrant.instrument_type else "N/A",
                warrant.cusip if warrant.cusip else "N/A",
                warrant.listed_market if warrant.listed_market else "N/A",
                status,
                closing_only,
            )

        # Print all tables
        console.print(
            Panel(
                summary_table,
                title="[bold blue]Warrants Overview[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                warrants_table,
                title="[bold yellow]All Tracked Warrants[/bold yellow]",
                border_style="yellow",
            )
        )
