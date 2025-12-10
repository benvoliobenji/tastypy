"""
Compact Option Chain class for equity option chains.

The compact format minimizes content size by returning option symbols as
comma-separated strings instead of nested structures. This is useful when
you need a quick list of all available options without detailed strike/expiration data.
"""

from .deliverable import Deliverable
from ....session import Session
from ....errors import translate_error_code
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class CompactOptionChain:
    """
    A class to manage and represent compact equity option chains data.

    The compact format returns option symbols as comma-separated strings,
    making it more lightweight than the nested format. Use this when you
    need to quickly get all option symbols without detailed chain structure.
    """

    def __init__(self, active_session: Session):
        """
        Initialize a CompactOptionChain with a session.

        Args:
            active_session: The active TastyTrade session.
        """
        self._session = active_session

    def sync(self, symbol: str) -> None:
        """
        Fetch the latest compact option chain data for the specified equity symbol.

        Args:
            symbol: The equity symbol to get the option chain for (e.g., 'AAPL', 'SPY')
        """
        # URL encode forward slashes for symbols like indexes
        symbol = symbol.replace("/", "%2F")
        self._endpoint_url = f"/option-chains/{symbol}/compact"

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            # The API may return an items array like nested, or direct data
            chain_data = data.get("data", {})
            if "items" in chain_data and chain_data["items"]:
                # If items array exists, use the first item
                self._chain_json = chain_data["items"][0]
            else:
                # Otherwise use data directly
                self._chain_json = chain_data
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def underlying_symbol(self) -> str:
        """Get the underlying symbol for this option chain."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        return self._chain_json.get("underlying-symbol", "")

    @property
    def root_symbol(self) -> str:
        """Get the root symbol for this option chain."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        return self._chain_json.get("root-symbol", "")

    @property
    def option_chain_type(self) -> str:
        """Get the option chain type (e.g., 'Standard')."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        return self._chain_json.get("option-chain-type", "")

    @property
    def settlement_type(self) -> str:
        """Get the settlement type (e.g., 'PM', 'AM')."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        return self._chain_json.get("settlement-type", "")

    @property
    def shares_per_contract(self) -> int:
        """Get the number of shares per contract."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        value = self._chain_json.get("shares-per-contract", 100)
        return int(value) if value is not None else 100

    @property
    def expiration_type(self) -> str:
        """Get the expiration type."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        return self._chain_json.get("expiration-type", "")

    @property
    def deliverable(self) -> Deliverable | None:
        """
        Get the deliverable for this option chain.

        Deliverables define what is received when an option is exercised.
        Standard equity options typically deliver 100 shares of the underlying.
        Returns None if no deliverable data is present.
        """
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")

        deliverable_data = self._chain_json.get("deliverables")

        if deliverable_data and isinstance(deliverable_data, dict):
            return Deliverable(deliverable_data)
        return None

    @property
    def symbols(self) -> list[str]:
        """
        Get the list of option symbols as a list.

        The API may return this as either an array or a comma-separated string.
        """
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")

        symbols_data = self._chain_json.get("symbols", [])

        # Handle both list and string formats
        if isinstance(symbols_data, list):
            return symbols_data
        elif isinstance(symbols_data, str) and symbols_data:
            return [s.strip() for s in symbols_data.split(",")]
        return []

    @property
    def streamer_symbols(self) -> list[str]:
        """
        Get the list of streamer symbols as a list.

        The API may return this as either an array or a comma-separated string.
        Streamer symbols are used for real-time market data streaming.
        """
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")

        symbols_data = self._chain_json.get("streamer-symbols", [])

        # Handle both list and string formats
        if isinstance(symbols_data, list):
            return symbols_data
        elif isinstance(symbols_data, str) and symbols_data:
            return [s.strip() for s in symbols_data.split(",")]
        return []

    def __str__(self) -> str:
        if not hasattr(self, "_chain_json"):
            return "CompactOptionChain: No data loaded"
        return f"CompactOptionChain: {self.underlying_symbol} ({len(self.symbols)} options)"

    def print_summary(self) -> None:
        """Print a simple text summary of the compact option chain information."""
        if not hasattr(self, "_chain_json"):
            print("No option chain data loaded. Call sync() first.")
            return

        print(f"\n{'=' * 70}")
        print(f"COMPACT OPTION CHAIN SUMMARY: {self.underlying_symbol}")
        print(f"{'=' * 70}")
        print(f"Underlying Symbol: {self.underlying_symbol}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Option Chain Type: {self.option_chain_type}")
        print(f"Settlement Type: {self.settlement_type}")
        print(f"Shares per Contract: {self.shares_per_contract}")
        print(f"Expiration Type: {self.expiration_type}")
        print(f"Total Options: {len(self.symbols)}")
        print(f"Total Streamer Symbols: {len(self.streamer_symbols)}")

        # Show deliverable information if present
        if self.deliverable:
            print("\nDeliverable:")
            self.deliverable.print_summary()

        # Show sample symbols
        if self.symbols:
            print("\nSample Option Symbols (first 10):")
            for i, symbol in enumerate(self.symbols[:10]):
                print(f"  {i + 1}. {symbol}")
            if len(self.symbols) > 10:
                print(f"  ... and {len(self.symbols) - 10} more")

        print(f"{'=' * 70}\n")

    def pretty_print(self) -> None:
        """Pretty print the compact option chain data in nicely formatted tables."""
        if not hasattr(self, "_chain_json"):
            console = Console()
            console.print("[red]No option chain data loaded. Call sync() first.[/red]")
            return

        console = Console()

        # Create basic option chain information table
        basic_table = Table(
            title=f"Compact Option Chain: {self.underlying_symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Underlying Symbol", str(self.underlying_symbol))
        basic_table.add_row("Root Symbol", str(self.root_symbol))
        basic_table.add_row("Option Chain Type", str(self.option_chain_type))
        basic_table.add_row("Settlement Type", str(self.settlement_type))
        basic_table.add_row("Shares per Contract", str(self.shares_per_contract))
        basic_table.add_row("Expiration Type", str(self.expiration_type))
        basic_table.add_row("Total Options", str(len(self.symbols)))
        basic_table.add_row("Total Streamer Symbols", str(len(self.streamer_symbols)))

        # Print basic information table
        console.print(
            Panel(
                basic_table,
                title="[bold blue]Compact Chain Overview[/bold blue]",
                border_style="blue",
            )
        )

        # Show deliverable if available
        if self.deliverable:
            deliverable_table = Table(
                title="Deliverable",
                show_header=True,
                header_style="bold magenta",
            )
            deliverable_table.add_column("Property", style="cyan")
            deliverable_table.add_column("Value", style="green")

            deliverable_table.add_row("ID", str(self.deliverable.id))
            deliverable_table.add_row("Symbol", str(self.deliverable.symbol))
            deliverable_table.add_row("Type", str(self.deliverable.deliverable_type))
            deliverable_table.add_row("Amount", str(self.deliverable.amount))
            deliverable_table.add_row(
                "Instrument Type", str(self.deliverable.instrument_type)
            )
            if self.deliverable.description:
                deliverable_table.add_row(
                    "Description", str(self.deliverable.description)
                )

            console.print(
                Panel(
                    deliverable_table,
                    title="[bold magenta]Deliverable[/bold magenta]",
                    border_style="magenta",
                )
            )

        # Show sample symbols
        if self.symbols:
            symbols_table = Table(
                title=f"Option Symbols (showing first 20 of {len(self.symbols)})",
                show_header=True,
                header_style="bold green",
            )
            symbols_table.add_column("#", style="cyan", width=5)
            symbols_table.add_column("OCC Symbol", style="green")
            symbols_table.add_column("Streamer Symbol", style="yellow")

            for i, (occ_symbol, streamer_symbol) in enumerate(
                zip(self.symbols[:20], self.streamer_symbols[:20])
            ):
                symbols_table.add_row(
                    str(i + 1),
                    occ_symbol,
                    streamer_symbol,
                )

            if len(self.symbols) > 20:
                symbols_table.add_row(
                    "...",
                    f"({len(self.symbols) - 20} more)",
                    "...",
                )

            console.print(
                Panel(
                    symbols_table,
                    title="[bold green]Sample Option Symbols[/bold green]",
                    border_style="green",
                )
            )
