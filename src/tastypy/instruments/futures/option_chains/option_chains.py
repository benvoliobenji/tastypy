from .expirations import Expirations
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class OptionChains:
    _option_chains_json: dict

    def __init__(self, option_chains_json: dict):
        self._option_chains_json = option_chains_json

    @property
    def underlying_symbol(self) -> str:
        return self._option_chains_json.get("underlying-symbol", "")

    @property
    def root_symbol(self) -> str:
        return self._option_chains_json.get("root-symbol", "")

    @property
    def exercise_style(self) -> str:
        return self._option_chains_json.get("exercise-style", "")

    @property
    def expirations(self) -> list[Expirations]:
        expirations_data = self._option_chains_json.get("expirations", [])
        return [Expirations(exp) for exp in expirations_data]

    def print_summary(self) -> None:
        """Print a simple text summary of the option chains information."""
        print(f"\n{'=' * 60}")
        print(f"OPTION CHAINS SUMMARY: {self.underlying_symbol}")
        print(f"{'=' * 60}")
        print(f"Underlying Symbol: {self.underlying_symbol}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Exercise Style: {self.exercise_style}")

        # Show expiration information
        if self.expirations:
            print(f"\nExpiration Information ({len(self.expirations)} expirations):")

            # Show information for each expiration
            for i, expiration in enumerate(self.expirations):
                print(f"  Expiration {i + 1}:")
                print(f"    Expiration Date: {expiration.expiration_date}")
                print(f"    Days to Expiration: {expiration.days_to_expiration}")
                print(f"    Expiration Type: {expiration.expiration_type}")
                print(f"    Settlement Type: {expiration.settlement_type}")

                if expiration.strikes:
                    strike_count = len(expiration.strikes)
                    print(f"    Available Strikes: {strike_count}")

                    strike_prices = [
                        strike.strike_price for strike in expiration.strikes
                    ]
                    if strike_prices:
                        print(
                            f"    Strike Range: ${min(strike_prices):,.2f} - ${max(strike_prices):,.2f}"
                        )

                if expiration.tick_sizes:
                    print(f"    Tick Sizes Available: {len(expiration.tick_sizes)}")

                # Add separator between expirations except for the last one
                if i < len(self.expirations) - 1:
                    print()

            # Summary statistics across all expirations
            total_strikes = sum(
                len(exp.strikes) if exp.strikes else 0 for exp in self.expirations
            )
            if total_strikes > 0:
                print(f"\n  Total Strikes Across All Expirations: {total_strikes}")

                # Get all strike prices across all expirations
                all_strike_prices = []
                for exp in self.expirations:
                    if exp.strikes:
                        all_strike_prices.extend(
                            [strike.strike_price for strike in exp.strikes]
                        )

                if all_strike_prices:
                    print(
                        f"  Overall Strike Range: ${min(all_strike_prices):,.2f} - ${max(all_strike_prices):,.2f}"
                    )

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all option chains data in nicely formatted tables."""
        console = Console()

        # Create basic option chains information table
        basic_table = Table(
            title=f"Option Chains: {self.underlying_symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Underlying Symbol", str(self.underlying_symbol))
        basic_table.add_row("Root Symbol", str(self.root_symbol))
        basic_table.add_row("Exercise Style", str(self.exercise_style))

        # Print basic information table
        console.print(
            Panel(
                basic_table,
                title="[bold blue]Option Chains Overview[/bold blue]",
                border_style="blue",
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
            total_calls = 0
            total_puts = 0

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
                        if strike.call:
                            total_calls += 1
                        if strike.put:
                            total_puts += 1

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

                strikes_summary_table.add_row("Total Calls", str(total_calls))
                strikes_summary_table.add_row("Total Puts", str(total_puts))

                console.print(
                    Panel(
                        strikes_summary_table,
                        title="[bold yellow]Combined Strike Statistics[/bold yellow]",
                        border_style="yellow",
                    )
                )

                # Sample strikes table from first expiration with strikes
                first_exp_with_strikes = next(
                    (exp for exp in self.expirations if exp.strikes), None
                )
                if first_exp_with_strikes and first_exp_with_strikes.strikes:
                    sample_table = Table(
                        title="Sample Strikes (First 5 from first expiration)",
                        show_header=True,
                        header_style="bold magenta",
                    )
                    sample_table.add_column("Strike Price", style="cyan")
                    sample_table.add_column("Call Available", style="green")
                    sample_table.add_column("Put Available", style="yellow")

                    sample_strikes = first_exp_with_strikes.strikes[:5]
                    for strike in sample_strikes:
                        sample_table.add_row(
                            f"${strike.strike_price:,.2f}",
                            "Yes" if strike.call else "No",
                            "Yes" if strike.put else "No",
                        )

                    if len(first_exp_with_strikes.strikes) > 5:
                        sample_table.add_row("...", "...", "...")

                    console.print(
                        Panel(
                            sample_table,
                            title="[bold magenta]Sample Strikes[/bold magenta]",
                            border_style="magenta",
                        )
                    )

            # Tick sizes summary from first expiration with tick sizes
            first_exp_with_ticks = next(
                (exp for exp in self.expirations if exp.tick_sizes), None
            )
            if first_exp_with_ticks and first_exp_with_ticks.tick_sizes:
                tick_summary_table = Table(
                    title=f"Tick Sizes Sample ({len(first_exp_with_ticks.tick_sizes)} entries from first expiration)",
                    show_header=True,
                    header_style="bold cyan",
                )
                tick_summary_table.add_column("Index", style="cyan")
                tick_summary_table.add_column("Threshold", style="green")
                tick_summary_table.add_column("Value", style="yellow")

                for i, tick_size in enumerate(
                    first_exp_with_ticks.tick_sizes[:3]
                ):  # Show first 3
                    tick_summary_table.add_row(
                        str(i + 1),
                        (
                            f"${tick_size.threshold:,.2f}"
                            if tick_size.threshold
                            else "N/A"
                        ),
                        f"${tick_size.value:,.4f}" if tick_size.value else "N/A",
                    )

                if len(first_exp_with_ticks.tick_sizes) > 3:
                    tick_summary_table.add_row("...", "...", "...")

                console.print(
                    Panel(
                        tick_summary_table,
                        title="[bold cyan]Tick Sizes Sample[/bold cyan]",
                        border_style="cyan",
                    )
                )

    def __str__(self) -> str:
        return f"OptionChains(underlying_symbol={self.underlying_symbol}, root_symbol={self.root_symbol}, exercise_style={self.exercise_style})"
