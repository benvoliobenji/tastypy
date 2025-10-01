from ..common.future_option import FutureOption
from ....session import Session
from ....errors import translate_error_code
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FuturesOptionChainsSymbol:
    _endpoint_url = ""
    _session: Session
    _future_options: list[FutureOption]

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self, symbol: str):
        """Fetch the latest data for the specified futures option symbol."""
        self._endpoint_url = f"/futures-option-chains/{symbol}"

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            futures_options_list = data.get("data", {}).get("items", [])
            if not futures_options_list:
                raise ValueError(f"No data found for symbol: {symbol}")
            self._future_options = [FutureOption(item) for item in futures_options_list]
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def future_options(self) -> list[FutureOption]:
        """Get the currently loaded futures options."""
        if not hasattr(self, "_future_options"):
            raise ValueError("No futures options data loaded. Call sync() first.")
        return self._future_options

    def __str__(self):
        if not hasattr(self, "_future_options") or not self._future_options:
            return "FuturesOptionChain: No data loaded"
        return f"FuturesOptionChain: {len(self._future_options)} options for {self._future_options[0].underlying_symbol}"

    def print_summary(self):
        """Print a simple text summary of all futures options in the chain."""
        if not hasattr(self, "_future_options"):
            print("No futures options data loaded. Call sync() first.")
            return

        if not self._future_options:
            print("No futures options found.")
            return

        print(f"\n{'=' * 70}")
        print("FUTURES OPTION CHAIN SUMMARY")
        print(f"{'=' * 70}")
        print(f"Underlying Symbol: {self._future_options[0].underlying_symbol}")
        print(f"Total Options: {len(self._future_options)}")

        # Group by option type and expiration
        calls = [opt for opt in self._future_options if opt.option_type == "C"]
        puts = [opt for opt in self._future_options if opt.option_type == "P"]

        print(f"Calls: {len(calls)}")
        print(f"Puts: {len(puts)}")

        # Group by expiration dates
        expirations = {}
        for option in self._future_options:
            exp_date = option.expiration_date
            if exp_date not in expirations:
                expirations[exp_date] = []
            expirations[exp_date].append(option)

        print(f"Expiration Dates: {len(expirations)}")

        # Show expiration breakdown
        print("\nOptions by Expiration:")
        for exp_date, options in sorted(expirations.items()):
            exp_calls = [opt for opt in options if opt.option_type == "C"]
            exp_puts = [opt for opt in options if opt.option_type == "P"]
            print(
                f"  {exp_date}: {len(options)} total ({len(exp_calls)} calls, {len(exp_puts)} puts)"
            )

        # Show strike price range
        strikes = [
            opt.strike_price for opt in self._future_options if opt.strike_price > 0
        ]
        if strikes:
            print(f"\nStrike Price Range: {min(strikes):,.2f} - {max(strikes):,.2f}")

        # Show sample options (first 10)
        print(f"\nSample Options (first {min(10, len(self._future_options))}):")
        print("-" * 70)
        for i, option in enumerate(self._future_options[:10], 1):
            print(f"{i:2d}. {option.symbol}")
            print(f"    Type: {option.option_type}, Strike: {option.strike_price:,.2f}")
            print(
                f"    Expires: {option.expiration_date}, DTE: {option.days_to_expiration}"
            )
            print(
                f"    Active: {option.active}, Closing Only: {option.is_closing_only}"
            )

        if len(self._future_options) > 10:
            print(f"... and {len(self._future_options) - 10} more options")

        print(f"{'=' * 70}\n")

    def pretty_print(self):
        """Pretty print futures options chain data in nicely formatted tables."""
        if not hasattr(self, "_future_options"):
            console = Console()
            console.print(
                "[red]No futures options data loaded. Call sync() first.[/red]"
            )
            return

        console = Console()

        if not self._future_options:
            console.print(
                Panel(
                    "[yellow]No futures options found.[/yellow]",
                    title="[bold blue]Futures Option Chain[/bold blue]",
                    border_style="blue",
                )
            )
            return

        # Summary statistics
        summary_table = Table(
            title=f"Futures Option Chain: {self._future_options[0].underlying_symbol}",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        # Calculate summary statistics
        calls = [opt for opt in self._future_options if opt.option_type == "C"]
        puts = [opt for opt in self._future_options if opt.option_type == "P"]
        active_options = [opt for opt in self._future_options if opt.active]
        closing_only = [opt for opt in self._future_options if opt.is_closing_only]

        # Expiration dates
        expirations = set(
            opt.expiration_date for opt in self._future_options if opt.expiration_date
        )

        # Strike prices
        strikes = [
            opt.strike_price for opt in self._future_options if opt.strike_price > 0
        ]

        summary_table.add_row("Total Options", str(len(self._future_options)))
        summary_table.add_row("Call Options", str(len(calls)))
        summary_table.add_row("Put Options", str(len(puts)))
        summary_table.add_row("Active Options", str(len(active_options)))
        summary_table.add_row("Closing Only", str(len(closing_only)))
        summary_table.add_row("Expiration Dates", str(len(expirations)))
        if strikes:
            summary_table.add_row(
                "Strike Range", f"{min(strikes):,.2f} - {max(strikes):,.2f}"
            )

        # Expiration breakdown table
        expiration_table = Table(
            title="Options by Expiration Date",
            show_header=True,
            header_style="bold green",
        )
        expiration_table.add_column("Expiration Date", style="cyan")
        expiration_table.add_column("Total", style="green")
        expiration_table.add_column("Calls", style="blue")
        expiration_table.add_column("Puts", style="red")
        expiration_table.add_column("Days to Exp", style="yellow")

        # Group by expiration for table
        exp_groups = {}
        for option in self._future_options:
            exp_date = option.expiration_date
            if exp_date not in exp_groups:
                exp_groups[exp_date] = []
            exp_groups[exp_date].append(option)

        for exp_date, options in sorted(exp_groups.items()):
            exp_calls = [opt for opt in options if opt.option_type == "C"]
            exp_puts = [opt for opt in options if opt.option_type == "P"]
            # Get days to expiration from first option in group
            dte = options[0].days_to_expiration if options else 0

            expiration_table.add_row(
                str(exp_date) if exp_date else "N/A",
                str(len(options)),
                str(len(exp_calls)),
                str(len(exp_puts)),
                str(dte),
            )

        # Sample options table (showing first 20)
        sample_table = Table(
            title=f"Sample Options (showing first {min(20, len(self._future_options))})",
            show_header=True,
            header_style="bold yellow",
        )
        sample_table.add_column("#", style="dim", width=3)
        sample_table.add_column("Symbol", style="cyan", no_wrap=True)
        sample_table.add_column("Type", style="magenta", width=4)
        sample_table.add_column("Strike", style="green")
        sample_table.add_column("Expiration", style="blue")
        sample_table.add_column("DTE", style="yellow", width=4)
        sample_table.add_column("Active", style="green", width=6)
        sample_table.add_column("Status", style="red")

        for i, option in enumerate(self._future_options[:20], 1):
            status = "Closing Only" if option.is_closing_only else "Normal"

            sample_table.add_row(
                str(i),
                option.symbol[:25] if option.symbol else "N/A",  # Truncate long symbols
                option.option_type,
                f"{option.strike_price:,.0f}" if option.strike_price else "N/A",
                str(option.expiration_date) if option.expiration_date else "N/A",
                str(option.days_to_expiration),
                "Yes" if option.active else "No",
                status,
            )

        # Print all tables
        console.print(
            Panel(
                summary_table,
                title="[bold blue]Chain Overview[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                expiration_table,
                title="[bold green]Expiration Breakdown[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                sample_table,
                title="[bold yellow]Sample Options[/bold yellow]",
                border_style="yellow",
            )
        )

        # Show additional info if there are many options
        if len(self._future_options) > 20:
            console.print(
                f"\n[dim]... and {len(self._future_options) - 20} more options in the chain[/dim]"
            )
