from .deliverable import Deliverable
from .expiration import NestedOptionChainExpiration
from ...common.tick_sizes import TickSizes
from ....session import Session
from ....errors import translate_error_code
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class NestedOptionChain:
    """
    A class to manage and represent nested equity option chains data.

    This provides a cleaner interface than fetching individual options,
    allowing you to access strikes and expirations in a structured format.
    """

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self, symbol: str):
        """
        Fetch the latest option chain data for the specified equity symbol.

        Args:
            symbol: The equity symbol to get the option chain for (e.g., 'AAPL', 'SPY')
        """
        # URL encode forward slashes for symbols like indexes
        symbol = symbol.replace("/", "%2F")
        self._endpoint_url = f"/option-chains/{symbol}/nested"

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            # The API returns a list of chains (can be multiple for different option types)
            chains_data = data.get("data", {}).get("items", [])
            if not chains_data:
                raise ValueError(f"No option chain data found for symbol: {symbol}")
            # Store the first chain (standard options, typically)
            self._chain_json = chains_data[0]
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
    def shares_per_contract(self) -> int:
        """Get the number of shares per contract."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        value = self._chain_json.get("shares-per-contract", 100)
        return int(value) if value is not None else 100

    @property
    def tick_sizes(self) -> list[TickSizes]:
        """Get the tick sizes for this option chain."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        tick_sizes_data = self._chain_json.get("tick-sizes", [])
        return [TickSizes(tick) for tick in tick_sizes_data]

    @property
    def deliverables(self) -> list[Deliverable]:
        """
        Get the deliverables for this option chain.

        Deliverables define what is received when an option is exercised.
        Standard equity options typically deliver 100 shares of the underlying,
        but adjusted options may have different deliverables (e.g., cash, multiple securities).
        """
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")

        deliverables_data = self._chain_json.get("deliverables")

        # Handle different API response formats
        if not deliverables_data:
            return []
        elif isinstance(deliverables_data, list):
            # If it's a list, process each deliverable
            return [Deliverable(deliv) for deliv in deliverables_data]
        elif isinstance(deliverables_data, dict):
            # If it's a single object, wrap it in a list
            return [Deliverable(deliverables_data)]
        else:
            return []

    @property
    def expirations(self) -> list[NestedOptionChainExpiration]:
        """Get the list of expirations with their strikes."""
        if not hasattr(self, "_chain_json"):
            raise ValueError("No option chain data loaded. Call sync() first.")
        expirations_data = self._chain_json.get("expirations", [])
        return [NestedOptionChainExpiration(exp) for exp in expirations_data]

    def __str__(self) -> str:
        if not hasattr(self, "_chain_json"):
            return "NestedOptionChain: No data loaded"
        return f"NestedOptionChain: {self.underlying_symbol} ({len(self.expirations)} expirations)"

    def print_summary(self) -> None:
        """Print a simple text summary of the option chain information."""
        if not hasattr(self, "_chain_json"):
            print("No option chain data loaded. Call sync() first.")
            return

        print(f"\n{'=' * 70}")
        print(f"NESTED OPTION CHAIN SUMMARY: {self.underlying_symbol}")
        print(f"{'=' * 70}")
        print(f"Underlying Symbol: {self.underlying_symbol}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Option Chain Type: {self.option_chain_type}")
        print(f"Shares per Contract: {self.shares_per_contract}")

        # Show deliverables information
        if self.deliverables:
            print(f"\nDeliverables ({len(self.deliverables)}):")
            for i, deliverable in enumerate(self.deliverables):
                print(f"  Deliverable {i + 1}:")
                deliverable.print_summary()

        # Show expiration information
        if self.expirations:
            print(f"\nExpiration Information ({len(self.expirations)} expirations):")

            total_strikes = 0
            for i, expiration in enumerate(self.expirations):
                print(f"  Expiration {i + 1}:")
                print(f"    Date: {expiration.expiration_date}")
                print(f"    Days to Expiration: {expiration.days_to_expiration}")
                print(f"    Type: {expiration.expiration_type}")
                print(f"    Settlement: {expiration.settlement_type}")

                if expiration.strikes:
                    strike_count = len(expiration.strikes)
                    total_strikes += strike_count
                    print(f"    Available Strikes: {strike_count}")

                    strike_prices = [
                        strike.strike_price for strike in expiration.strikes
                    ]
                    if strike_prices:
                        print(
                            f"    Strike Range: ${min(strike_prices):,.2f} - ${max(strike_prices):,.2f}"
                        )

                if i < len(self.expirations) - 1:
                    print()

            if total_strikes > 0:
                print(f"\n  Total Strikes Across All Expirations: {total_strikes}")

        print(f"{'=' * 70}\n")

    def pretty_print(self) -> None:
        """Pretty print all option chain data in nicely formatted tables."""
        if not hasattr(self, "_chain_json"):
            console = Console()
            console.print("[red]No option chain data loaded. Call sync() first.[/red]")
            return

        console = Console()

        # Create basic option chain information table
        basic_table = Table(
            title=f"Option Chain: {self.underlying_symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Underlying Symbol", str(self.underlying_symbol))
        basic_table.add_row("Root Symbol", str(self.root_symbol))
        basic_table.add_row("Option Chain Type", str(self.option_chain_type))
        basic_table.add_row("Shares per Contract", str(self.shares_per_contract))
        basic_table.add_row("Number of Expirations", str(len(self.expirations)))
        basic_table.add_row("Number of Deliverables", str(len(self.deliverables)))

        # Print basic information table
        console.print(
            Panel(
                basic_table,
                title="[bold blue]Option Chain Overview[/bold blue]",
                border_style="blue",
            )
        )

        # Show deliverables if available
        if self.deliverables:
            deliverables_table = Table(
                title=f"Deliverables ({len(self.deliverables)} total)",
                show_header=True,
                header_style="bold magenta",
            )
            deliverables_table.add_column("ID", style="cyan")
            deliverables_table.add_column("Symbol", style="green")
            deliverables_table.add_column("Type", style="yellow")
            deliverables_table.add_column("Amount", style="magenta")
            deliverables_table.add_column("Instrument Type", style="blue")

            for deliverable in self.deliverables:
                deliverables_table.add_row(
                    str(deliverable.id),
                    str(deliverable.symbol),
                    str(deliverable.deliverable_type),
                    str(deliverable.amount),
                    str(deliverable.instrument_type),
                )

            console.print(
                Panel(
                    deliverables_table,
                    title="[bold magenta]Deliverables[/bold magenta]",
                    border_style="magenta",
                )
            )

        # Show expiration summary if available
        if self.expirations:
            # Overview table for all expirations
            overview_table = Table(
                title=f"Expirations Overview ({len(self.expirations)} total)",
                show_header=True,
                header_style="bold green",
            )
            overview_table.add_column("Exp #", style="cyan")
            overview_table.add_column("Expiration Date", style="green")
            overview_table.add_column("Days to Exp", style="yellow")
            overview_table.add_column("Type", style="magenta")
            overview_table.add_column("Strikes", style="red")

            # Collect data across all expirations for summary
            all_strikes = []

            for i, expiration in enumerate(self.expirations):
                strike_count = len(expiration.strikes) if expiration.strikes else 0

                overview_table.add_row(
                    str(i + 1),
                    (
                        str(expiration.expiration_date)
                        if expiration.expiration_date
                        else "N/A"
                    ),
                    str(expiration.days_to_expiration),
                    str(expiration.expiration_type),
                    str(strike_count) if strike_count > 0 else "0",
                )

                # Collect strikes for summary statistics
                if expiration.strikes:
                    for strike in expiration.strikes:
                        all_strikes.append(strike.strike_price)

            console.print(
                Panel(
                    overview_table,
                    title="[bold green]Expirations Overview[/bold green]",
                    border_style="green",
                )
            )

            # Combined strike statistics across all expirations
            if all_strikes:
                strikes_summary_table = Table(
                    title=f"Combined Strike Statistics ({len(all_strikes)} total strikes)",
                    show_header=True,
                    header_style="bold yellow",
                )
                strikes_summary_table.add_column("Statistic", style="cyan")
                strikes_summary_table.add_column("Value", style="green")

                strikes_summary_table.add_row("Total Strikes", str(len(all_strikes)))
                strikes_summary_table.add_row("Min Strike", f"${min(all_strikes):,.2f}")
                strikes_summary_table.add_row("Max Strike", f"${max(all_strikes):,.2f}")
                if len(all_strikes) > 1:
                    avg_strike = sum(all_strikes) / len(all_strikes)
                    strikes_summary_table.add_row("Avg Strike", f"${avg_strike:,.2f}")

                console.print(
                    Panel(
                        strikes_summary_table,
                        title="[bold yellow]Combined Strike Statistics[/bold yellow]",
                        border_style="yellow",
                    )
                )
