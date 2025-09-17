from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...errors import translate_error_code
from ...session import Session
from .equity import Equity, Lendability


class ActiveEquities:
    """Endpoint for fetching and managing active equity instruments."""

    _url_endpoint = "/instruments/equities/active"
    _session: Session
    _active_equities: list[Equity] = []

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(
        self,
        page_offset: int = 0,
        per_page: int = 1000,
        lendability: Lendability | None = None,
    ):
        """Fetch the latest data for all active equities with the given parameters."""
        params: dict = {
            "page-offset": page_offset,
            "per-page": per_page,
        }
        if lendability:
            params["lendability"] = lendability.value

        # For large datasets with a lot of per-page values, increase timeout and inform the user through a spinning symbol
        if per_page > 500:
            self._session._client.timeout = 60
            console = Console()
            with console.status(
                "[bold green]Fetching active equities data...[/bold green]",
                spinner="dots",
            ):
                response = self._session._client.get(self._url_endpoint, params=params)
        else:
            response = self._session._client.get(self._url_endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            equities_data = data.get("data", {}).get("items", [])
            self._active_equities = []
            for equity_json in equities_data:
                equity = Equity(equity_json)
                self._active_equities.append(equity)
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def active_equities(self) -> list[Equity]:
        """Get a list of all currently active equities."""
        if not hasattr(self, "_active_equities"):
            raise ValueError(
                "Active equities data has not been loaded. Call sync() first."
            )
        return self._active_equities

    def __str__(self):
        return f"ActiveEquities: {len(self._active_equities)} active equities"

    def print_summary(self) -> None:
        """Print a simple text summary of all active equities."""
        if not hasattr(self, "_active_equities"):
            print("No active equities data loaded. Call sync() first.")
            return

        print(f"\n{'=' * 60}")
        print("ACTIVE EQUITIES SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Active Equities: {len(self._active_equities)}")

        if not self._active_equities:
            print("No active equities found.")
            print(f"{'=' * 60}\n")
            return

        # Group by various criteria
        by_lendability = {}
        by_instrument_type = {}
        etf_count = 0
        index_count = 0
        illiquid_count = 0
        closing_only_count = 0
        options_closing_only_count = 0

        for equity in self._active_equities:
            # Lendability grouping
            lendability = equity.lendability.value if equity.lendability else "Unknown"
            if lendability not in by_lendability:
                by_lendability[lendability] = []
            by_lendability[lendability].append(equity)

            # Instrument type grouping
            instrument_type = equity.instrument_type or "Unknown"
            if instrument_type not in by_instrument_type:
                by_instrument_type[instrument_type] = []
            by_instrument_type[instrument_type].append(equity)

            # Classifications
            if equity.is_etf:
                etf_count += 1
            if equity.is_index:
                index_count += 1
            if equity.is_illiquid:
                illiquid_count += 1
            if equity.is_closing_only:
                closing_only_count += 1
            if equity.is_options_closing_only:
                options_closing_only_count += 1

        print(f"ETFs: {etf_count}")
        print(f"Indices: {index_count}")
        print(f"Illiquid Securities: {illiquid_count}")
        print(f"Closing Only: {closing_only_count}")
        print(f"Options Closing Only: {options_closing_only_count}")
        print()

        print("Equities by Lendability:")
        for lendability, equities_list in by_lendability.items():
            print(f"  {lendability}: {len(equities_list)} equities")

        print()
        print("Equities by Instrument Type:")
        for instrument_type, equities_list in by_instrument_type.items():
            print(f"  {instrument_type}: {len(equities_list)} equities")

        print()
        print("Sample Equity Details (first 10):")
        print("-" * 60)

        for i, equity in enumerate(self._active_equities[:10], 1):
            print(f"{i:2d}. {equity.symbol}")
            print(f"    Description: {equity.description}")
            print(
                f"    Lendability: {equity.lendability.value if equity.lendability else 'N/A'}"
            )
            print(f"    Borrow Rate: {equity.borrow_rate:.4f}%")
            if equity.is_etf:
                print("    Type: ETF")
            if equity.is_index:
                print("    Type: Index")
            if equity.is_illiquid:
                print("    Status: Illiquid")
            print()

        if len(self._active_equities) > 10:
            print(f"... and {len(self._active_equities) - 10} more equities")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all active equities data in nicely formatted tables."""
        if not hasattr(self, "_active_equities"):
            console = Console()
            console.print(
                "[red]No active equities data loaded. Call sync() first.[/red]"
            )
            return

        console = Console()

        if not self._active_equities:
            console.print(
                Panel(
                    "[yellow]No active equities found.[/yellow]",
                    title="[bold blue]Active Equities Summary[/bold blue]",
                    border_style="blue",
                )
            )
            return

        # Summary statistics
        summary_table = Table(
            title="Active Equities Overview",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        # Calculate summary statistics
        by_lendability = {}
        etf_count = 0
        index_count = 0
        illiquid_count = 0
        closing_only_count = 0
        options_closing_only_count = 0
        total_count = len(self._active_equities)

        for equity in self._active_equities:
            lendability = equity.lendability.value if equity.lendability else "Unknown"
            by_lendability[lendability] = by_lendability.get(lendability, 0) + 1

            if equity.is_etf:
                etf_count += 1
            if equity.is_index:
                index_count += 1
            if equity.is_illiquid:
                illiquid_count += 1
            if equity.is_closing_only:
                closing_only_count += 1
            if equity.is_options_closing_only:
                options_closing_only_count += 1

        summary_table.add_row("Total Active Equities", str(total_count))
        summary_table.add_row("ETFs", str(etf_count))
        summary_table.add_row("Indices", str(index_count))
        summary_table.add_row("Illiquid Securities", str(illiquid_count))
        summary_table.add_row("Closing Only", str(closing_only_count))
        summary_table.add_row("Options Closing Only", str(options_closing_only_count))

        # Lendability breakdown table
        lendability_table = Table(
            title="Equities by Lendability",
            show_header=True,
            header_style="bold green",
        )
        lendability_table.add_column("Lendability", style="cyan")
        lendability_table.add_column("Count", style="green")

        for lendability, count in sorted(by_lendability.items()):
            lendability_table.add_row(lendability, str(count))

        # Sample equities table (first 20)
        equities_table = Table(
            title=f"Sample Active Equities (showing first {min(20, len(self._active_equities))})",
            show_header=True,
            header_style="bold yellow",
        )
        equities_table.add_column("#", style="dim", width=3)
        equities_table.add_column("Symbol", style="cyan", no_wrap=True)
        equities_table.add_column("Description", style="blue")
        equities_table.add_column("Lendability", style="green")
        equities_table.add_column("Borrow Rate", style="yellow")
        equities_table.add_column("Type", style="magenta")

        for i, equity in enumerate(self._active_equities[:20], 1):
            # Determine type
            types = []
            if equity.is_etf:
                types.append("ETF")
            if equity.is_index:
                types.append("Index")
            if equity.is_illiquid:
                types.append("Illiquid")
            type_str = ", ".join(types) if types else "Regular"

            equities_table.add_row(
                str(i),
                equity.symbol,
                equity.description[:40] if equity.description else "N/A",
                equity.lendability.value[:15] if equity.lendability else "Unknown",
                f"{equity.borrow_rate:.4f}%",
                type_str[:20],
            )

        # Trading restrictions table for equities with restrictions
        restrictions_table = Table(
            title="Trading Restrictions",
            show_header=True,
            header_style="bold red",
        )
        restrictions_table.add_column("Symbol", style="cyan")
        restrictions_table.add_column("Restriction Type", style="yellow")
        restrictions_table.add_column("Status", style="red")

        for equity in self._active_equities[
            :50
        ]:  # Limit to first 50 to avoid too much output
            if equity.is_closing_only:
                restrictions_table.add_row(
                    equity.symbol, "Equity Trading", "Closing Only"
                )
            if equity.is_options_closing_only:
                restrictions_table.add_row(
                    equity.symbol, "Options Trading", "Closing Only"
                )
            if equity.halted_at:
                restrictions_table.add_row(
                    equity.symbol, "Trading Halt", f"Since {equity.halted_at}"
                )
            if equity.stops_trading_at:
                restrictions_table.add_row(
                    equity.symbol, "Trading Stop", f"At {equity.stops_trading_at}"
                )

        # Print all tables
        console.print(
            Panel(
                summary_table,
                title="[bold blue]Active Equities Overview[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                lendability_table,
                title="[bold green]Breakdown by Lendability[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                equities_table,
                title="[bold yellow]Sample Equities[/bold yellow]",
                border_style="yellow",
            )
        )

        # Only show restrictions table if there are restrictions
        if restrictions_table.row_count > 0:
            console.print(
                Panel(
                    restrictions_table,
                    title="[bold red]Trading Restrictions[/bold red]",
                    border_style="red",
                )
            )
