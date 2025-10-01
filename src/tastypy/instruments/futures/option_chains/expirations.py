import datetime

from ...common.tick_sizes import TickSizes
from ...common.strikes import Strikes
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Expirations:
    _expirations_dict: dict

    def __init__(self, expirations_dict: dict):
        self._expirations_dict = expirations_dict

    @property
    def underlying_symbol(self) -> str:
        return self._expirations_dict.get("underlying-symbol", "")

    @property
    def root_symbol(self) -> str:
        return self._expirations_dict.get("root-symbol", "")

    @property
    def option_root_symbol(self) -> str:
        return self._expirations_dict.get("option-root-symbol", "")

    @property
    def option_contract_sybmol(self) -> str:
        return self._expirations_dict.get("option-contract-symbol", "")

    @property
    def asset(self) -> str:
        return self._expirations_dict.get("asset", "")

    @property
    def expiration_date(self) -> datetime.date | None:
        date_str = self._expirations_dict.get("expiration-date", "")
        if date_str:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return None

    @property
    def days_to_expiration(self) -> int:
        return self._expirations_dict.get("days-to-expiration", 0)

    @property
    def expiration_type(self) -> str:
        return self._expirations_dict.get("expiration-type", "")

    @property
    def settlement_type(self) -> str:
        return self._expirations_dict.get("settlement-type", "")

    @property
    def notional_value(self) -> float:
        value = self._expirations_dict.get("notional-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def display_factor(self) -> float:
        value = self._expirations_dict.get("display-factor", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def strike_factor(self) -> float:
        value = self._expirations_dict.get("strike-factor", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def stops_trading_at(self) -> datetime.datetime | None:
        stops_trading_at = self._expirations_dict.get("stops-trading-at", "")
        if stops_trading_at:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(
                stops_trading_at.replace("Z", "+00:00")
            )
        return None

    @property
    def expires_at(self) -> datetime.datetime | None:
        expires_at = self._expirations_dict.get("expires-at", "")
        if expires_at:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        return None

    @property
    def tick_sizes(self) -> list[TickSizes] | None:
        tick_sizes_data = self._expirations_dict.get("tick-sizes", None)
        if tick_sizes_data:
            if isinstance(tick_sizes_data, list):
                return [TickSizes(item) for item in tick_sizes_data]
            else:
                return [TickSizes(tick_sizes_data)]
        return None

    @property
    def strikes(self) -> list[Strikes] | None:
        strikes_data = self._expirations_dict.get("strikes", None)
        if strikes_data:
            if isinstance(strikes_data, list):
                return [Strikes(item) for item in strikes_data]
            else:
                return [Strikes(strikes_data)]
        return None

    def print_summary(self) -> None:
        """Print a simple text summary of the expiration information."""
        print(f"\n{'=' * 60}")
        print(f"EXPIRATION SUMMARY: {self.underlying_symbol}")
        print(f"{'=' * 60}")
        print(f"Underlying Symbol: {self.underlying_symbol}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Option Root Symbol: {self.option_root_symbol}")
        print(f"Option Contract Symbol: {self.option_contract_sybmol}")
        print(f"Asset: {self.asset}")

        print(f"Expiration Date: {self.expiration_date}")
        print(f"Days to Expiration: {self.days_to_expiration}")
        print(f"Expiration Type: {self.expiration_type}")
        print(f"Settlement Type: {self.settlement_type}")

        print(f"Notional Value: ${self.notional_value:,.2f}")
        print(f"Display Factor: {self.display_factor}")
        print(f"Strike Factor: {self.strike_factor}")

        if self.stops_trading_at:
            print(f"Stops Trading At: {self.stops_trading_at}")
        if self.expires_at:
            print(f"Expires At: {self.expires_at}")

        # Tick sizes information
        if self.tick_sizes:
            print(f"Number of Tick Sizes: {len(self.tick_sizes)}")

        # Strikes information
        if self.strikes:
            print(f"Number of Strikes: {len(self.strikes)}")
            strike_prices = [strike.strike_price for strike in self.strikes]
            if strike_prices:
                print(
                    f"Strike Price Range: ${min(strike_prices):,.2f} - ${max(strike_prices):,.2f}"
                )

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all expiration data in nicely formatted tables."""
        console = Console()

        # Create basic expiration information table
        basic_table = Table(
            title=f"Expiration: {self.underlying_symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Underlying Symbol", str(self.underlying_symbol))
        basic_table.add_row("Root Symbol", str(self.root_symbol))
        basic_table.add_row("Option Root Symbol", str(self.option_root_symbol))
        basic_table.add_row("Option Contract Symbol", str(self.option_contract_sybmol))
        basic_table.add_row("Asset", str(self.asset))

        # Expiration details table
        expiration_table = Table(
            title="Expiration Details",
            show_header=True,
            header_style="bold green",
        )
        expiration_table.add_column("Property", style="cyan")
        expiration_table.add_column("Value", style="green")

        expiration_table.add_row(
            "Expiration Date",
            str(self.expiration_date) if self.expiration_date else "N/A",
        )
        expiration_table.add_row("Days to Expiration", str(self.days_to_expiration))
        expiration_table.add_row("Expiration Type", str(self.expiration_type))
        expiration_table.add_row("Settlement Type", str(self.settlement_type))

        # Contract specifications table
        contract_table = Table(
            title="Contract Specifications",
            show_header=True,
            header_style="bold yellow",
        )
        contract_table.add_column("Property", style="cyan")
        contract_table.add_column("Value", style="green")

        contract_table.add_row("Notional Value", f"${self.notional_value:,.2f}")
        contract_table.add_row("Display Factor", f"{self.display_factor:g}")
        contract_table.add_row("Strike Factor", f"{self.strike_factor:g}")

        # Important dates table (only if there are dates)
        dates_table = Table(
            title="Important Dates & Times",
            show_header=True,
            header_style="bold cyan",
        )
        dates_table.add_column("Property", style="cyan")
        dates_table.add_column("Value", style="green")

        if self.stops_trading_at:
            dates_table.add_row("Stops Trading At", str(self.stops_trading_at))
        if self.expires_at:
            dates_table.add_row("Expires At", str(self.expires_at))

        # Print all basic tables
        console.print(
            Panel(
                basic_table,
                title="[bold blue]Basic Information[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                expiration_table,
                title="[bold green]Expiration Details[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                contract_table,
                title="[bold yellow]Contract Specifications[/bold yellow]",
                border_style="yellow",
            )
        )

        # Only show dates table if there are dates
        if dates_table.row_count > 0:
            console.print(
                Panel(
                    dates_table,
                    title="[bold cyan]Important Dates & Times[/bold cyan]",
                    border_style="cyan",
                )
            )

        # Tick sizes overview
        if self.tick_sizes:
            tick_table = Table(
                title=f"Tick Sizes ({len(self.tick_sizes)} entries)",
                show_header=True,
                header_style="bold magenta",
            )
            tick_table.add_column("Index", style="cyan")
            tick_table.add_column("Threshold", style="green")
            tick_table.add_column("Value", style="yellow")

            for i, tick_size in enumerate(self.tick_sizes):
                tick_table.add_row(
                    str(i + 1),
                    f"${tick_size.threshold:,.2f}" if tick_size.threshold else "N/A",
                    f"${tick_size.value:,.4f}" if tick_size.value else "N/A",
                )

            console.print(
                Panel(
                    tick_table,
                    title="[bold magenta]Tick Sizes[/bold magenta]",
                    border_style="magenta",
                )
            )

        # Strikes overview
        if self.strikes:
            strikes_table = Table(
                title=f"Strikes Overview ({len(self.strikes)} strikes)",
                show_header=True,
                header_style="bold red",
            )
            strikes_table.add_column("Strike Price", style="cyan")
            strikes_table.add_column("Call", style="green")
            strikes_table.add_column("Put", style="yellow")

            # Show first 10 strikes for overview
            display_strikes = self.strikes[:10]
            for strike in display_strikes:
                strikes_table.add_row(
                    f"${strike.strike_price:,.2f}",
                    "Yes" if strike.call else "No",
                    "Yes" if strike.put else "No",
                )

            if len(self.strikes) > 10:
                strikes_table.add_row("...", "...", "...")

            console.print(
                Panel(
                    strikes_table,
                    title="[bold red]Available Strikes[/bold red]",
                    border_style="red",
                )
            )

            # Strike statistics
            strike_prices = [strike.strike_price for strike in self.strikes]
            if strike_prices:
                stats_table = Table(
                    title="Strike Statistics",
                    show_header=True,
                    header_style="bold white",
                )
                stats_table.add_column("Statistic", style="cyan")
                stats_table.add_column("Value", style="green")

                stats_table.add_row("Total Strikes", str(len(strike_prices)))
                stats_table.add_row("Min Strike", f"${min(strike_prices):,.2f}")
                stats_table.add_row("Max Strike", f"${max(strike_prices):,.2f}")
                if len(strike_prices) > 1:
                    avg_strike = sum(strike_prices) / len(strike_prices)
                    stats_table.add_row("Avg Strike", f"${avg_strike:,.2f}")

                console.print(
                    Panel(
                        stats_table,
                        title="[bold white]Strike Statistics[/bold white]",
                        border_style="white",
                    )
                )

    def __str__(self) -> str:
        return (
            f"Expirations(underlying_symbol={self.underlying_symbol}, "
            f"expiration_date={self.expiration_date}, "
            f"days_to_expiration={self.days_to_expiration})"
        )
