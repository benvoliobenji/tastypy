from .futures import Futures
from .option_chains import OptionChains
from ....session import Session
from ....errors import translate_error_code
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FuturesOptionChainsNested:
    """A class to manage and represent nested futures option chains data. Returns futures product code in a nested form to minimize redundant processing (unlike symbol)"""

    _endpoint_url = ""
    _session: Session
    _nested_data: dict
    _futures_list: list[Futures] = []
    _option_chains_list: list[OptionChains] = []

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self, symbol: str):
        """Fetch the latest data for the specified futures option symbol."""
        self._endpoint_url = f"/futures-option-chains/{symbol}/nested"

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            self._nested_data = data.get("data", {})
            self._futures_list = [
                Futures(fut) for fut in self._nested_data.get("futures", [])
            ]
            self._option_chains_list = [
                OptionChains(opt) for opt in self._nested_data.get("option-chains", [])
            ]
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def futures(self) -> list[Futures]:
        """Get the list of futures data from the nested structure."""
        if len(self._futures_list) == 0:
            raise ValueError("No futures data available. Please call sync() first.")
        return self._futures_list

    @property
    def option_chains(self) -> list[OptionChains]:
        """Get the list of option chains data from the nested structure."""
        if len(self._option_chains_list) == 0:
            raise ValueError(
                "No option chains data available. Please call sync() first."
            )
        return self._option_chains_list

    def print_summary(self) -> None:
        """Print a simple text summary of the nested futures option chains data."""
        print(f"\n{'=' * 60}")
        print("FUTURES OPTION CHAINS NESTED SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Futures Contracts: {len(self._futures_list)}")
        print(f"Total Option Chains: {len(self._option_chains_list)}")

        # Futures summary
        if self._futures_list:
            print("\nFutures Contracts:")
            active_count = sum(1 for f in self._futures_list if f.active_month)
            next_active_count = sum(
                1 for f in self._futures_list if f.next_active_month
            )
            print(f"  Active Month Contracts: {active_count}")
            print(f"  Next Active Month Contracts: {next_active_count}")

            # Show sample futures symbols
            sample_futures = self._futures_list[:3]
            print(f"  Sample Symbols: {', '.join([f.symbol for f in sample_futures])}")
            if len(self._futures_list) > 3:
                print(f"  ... and {len(self._futures_list) - 3} more")

        # Option chains summary
        if self._option_chains_list:
            print("\nOption Chains:")
            underlying_symbols = list(
                set([oc.underlying_symbol for oc in self._option_chains_list])
            )
            print(f"  Underlying Symbols: {', '.join(underlying_symbols)}")

            # Count total strikes across all chains
            total_strikes = 0
            for chain in self._option_chains_list:
                for expiration in chain.expirations:
                    if expiration.strikes:
                        total_strikes += len(expiration.strikes)

            if total_strikes > 0:
                print(f"  Total Available Strikes: {total_strikes}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all nested futures option chains data in nicely formatted tables."""
        console = Console()

        # Create overview table
        overview_table = Table(
            title="Futures Option Chains Nested Overview",
            show_header=True,
            header_style="bold blue",
        )
        overview_table.add_column("Category", style="cyan", no_wrap=True)
        overview_table.add_column("Count", style="green")
        overview_table.add_column("Details", style="yellow")

        overview_table.add_row(
            "Futures Contracts",
            str(len(self._futures_list)),
            (
                f"{sum(1 for f in self._futures_list if f.active_month)} active, "
                f"{sum(1 for f in self._futures_list if f.next_active_month)} next active"
                if self._futures_list
                else "N/A"
            ),
        )

        overview_table.add_row(
            "Option Chains",
            str(len(self._option_chains_list)),
            (
                f"{len(set([oc.underlying_symbol for oc in self._option_chains_list]))} unique symbols"
                if self._option_chains_list
                else "N/A"
            ),
        )

        console.print(
            Panel(
                overview_table,
                title="[bold blue]Collection Overview[/bold blue]",
                border_style="blue",
            )
        )

        # Futures contracts summary
        if self._futures_list:
            futures_table = Table(
                title=f"Futures Contracts ({len(self._futures_list)} total)",
                show_header=True,
                header_style="bold green",
            )
            futures_table.add_column("Symbol", style="cyan")
            futures_table.add_column("Maturity Date", style="green")
            futures_table.add_column("Days to Exp", style="yellow")
            futures_table.add_column("Active", style="magenta")
            futures_table.add_column("Next Active", style="red")

            # Show first 10 futures for overview
            display_futures = self._futures_list[:10]
            for future in display_futures:
                futures_table.add_row(
                    str(future.symbol),
                    str(future.maturity_date) if future.maturity_date else "N/A",
                    str(future.days_to_expiration),
                    "Yes" if future.active_month else "No",
                    "Yes" if future.next_active_month else "No",
                )

            if len(self._futures_list) > 10:
                futures_table.add_row("...", "...", "...", "...", "...")

            console.print(
                Panel(
                    futures_table,
                    title="[bold green]Futures Contracts[/bold green]",
                    border_style="green",
                )
            )

        # Option chains summary
        if self._option_chains_list:
            chains_table = Table(
                title=f"Option Chains ({len(self._option_chains_list)} total)",
                show_header=True,
                header_style="bold yellow",
            )
            chains_table.add_column("Underlying", style="cyan")
            chains_table.add_column("Root Symbol", style="green")
            chains_table.add_column("Exercise Style", style="yellow")
            chains_table.add_column("Exp Date", style="magenta")
            chains_table.add_column("Strikes", style="red")

            # Show all option chains (usually not too many)
            for chain in self._option_chains_list:
                # Calculate total strikes across all expirations for this chain
                total_chain_strikes = 0
                for expiration in chain.expirations:
                    if expiration.strikes:
                        total_chain_strikes += len(expiration.strikes)

                # Get first expiration date for display (if any)
                first_exp_date = "N/A"
                if chain.expirations:
                    for expiration in chain.expirations:
                        if expiration.expiration_date:
                            first_exp_date = str(expiration.expiration_date)
                            break

                chains_table.add_row(
                    str(chain.underlying_symbol),
                    str(chain.root_symbol),
                    str(chain.exercise_style),
                    first_exp_date,
                    str(total_chain_strikes) if total_chain_strikes > 0 else "0",
                )

            console.print(
                Panel(
                    chains_table,
                    title="[bold yellow]Option Chains[/bold yellow]",
                    border_style="yellow",
                )
            )

            # Strike statistics across all chains
            all_strikes = []
            total_calls = 0
            total_puts = 0

            for chain in self._option_chains_list:
                for expiration in chain.expirations:
                    if expiration.strikes:
                        for strike in expiration.strikes:
                            all_strikes.append(strike.strike_price)
                            if strike.call:
                                total_calls += 1
                            if strike.put:
                                total_puts += 1

            if all_strikes:
                stats_table = Table(
                    title="Combined Strike Statistics",
                    show_header=True,
                    header_style="bold magenta",
                )
                stats_table.add_column("Statistic", style="cyan")
                stats_table.add_column("Value", style="green")

                stats_table.add_row("Total Strikes", str(len(all_strikes)))
                stats_table.add_row("Min Strike", f"${min(all_strikes):,.2f}")
                stats_table.add_row("Max Strike", f"${max(all_strikes):,.2f}")
                if len(all_strikes) > 1:
                    avg_strike = sum(all_strikes) / len(all_strikes)
                    stats_table.add_row("Avg Strike", f"${avg_strike:,.2f}")

                stats_table.add_row("Total Calls", str(total_calls))
                stats_table.add_row("Total Puts", str(total_puts))

                console.print(
                    Panel(
                        stats_table,
                        title="[bold magenta]Strike Statistics[/bold magenta]",
                        border_style="magenta",
                    )
                )

    def __str__(self):
        return f"FuturesOptionChainsNested: {len(self._futures_list)} futures, {len(self._option_chains_list)} option chains"
