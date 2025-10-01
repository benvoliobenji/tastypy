from .future_option_product import FutureOptionProduct
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FutureOption:
    """Represents a futures option."""

    _future_option_json: dict

    def __init__(self, future_option_json: dict):
        self._future_option_json = future_option_json

    @property
    def active(self) -> bool:
        return self._future_option_json.get("active", False)

    @property
    def days_to_expiration(self) -> int:
        return self._future_option_json.get("days-to-expiration", 0)

    @property
    def display_factor(self) -> float:
        value = self._future_option_json.get("display-factor", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def exchange(self) -> str:
        return self._future_option_json.get("exchange", "")

    @property
    def exercise_style(self) -> str:
        return self._future_option_json.get("exercise-style", "")

    @property
    def expiration_date(self) -> datetime.date | None:
        date_str = self._future_option_json.get("expiration-date", "")
        if date_str:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return None

    @property
    def expires_at(self) -> datetime.datetime | None:
        expires_at = self._future_option_json.get("expires-at", "")
        if expires_at:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        return None

    @property
    def future_price_ratio(self) -> float:
        value = self._future_option_json.get("future-price-ratio", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def is_closing_only(self) -> bool:
        return self._future_option_json.get("is-closing-only", False)

    @property
    def is_confirmed(self) -> bool:
        return self._future_option_json.get("is-confirmed", False)

    @property
    def is_exercisable_weekly(self) -> bool:
        return self._future_option_json.get("is-exercisable-weekly", False)

    @property
    def is_primary_deliverable(self) -> bool:
        return self._future_option_json.get("is-primary-deliverable", False)

    @property
    def is_vanilla(self) -> bool:
        return self._future_option_json.get("is-vanilla", False)

    @property
    def last_trade_time(self) -> str:
        return self._future_option_json.get("last-trade-time", "")

    @property
    def maturity_date(self) -> datetime.date | None:
        date_str = self._future_option_json.get("maturity-date", "")
        if date_str:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return None

    @property
    def multiplier(self) -> float:
        value = self._future_option_json.get("multiplier", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def notional_value(self) -> float:
        value = self._future_option_json.get("notional-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def option_root_symbol(self) -> str:
        return self._future_option_json.get("option-root-symbol", "")

    @property
    def option_type(self) -> str:
        return self._future_option_json.get("option-type", "")

    @property
    def product_code(self) -> str:
        return self._future_option_json.get("product-code", "")

    @property
    def root_symbol(self) -> str:
        return self._future_option_json.get("root-symbol", "")

    @property
    def security_id(self) -> str:
        return self._future_option_json.get("security-id", "")

    @property
    def settlement_type(self) -> str:
        return self._future_option_json.get("settlement-type", "")

    @property
    def stops_trading_at(self) -> datetime.datetime | None:
        stops_trading_at = self._future_option_json.get("stops-trading-at", "")
        if stops_trading_at:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(
                stops_trading_at.replace("Z", "+00:00")
            )
        return None

    @property
    def streamer_symbol(self) -> str:
        return self._future_option_json.get("streamer-symbol", "")

    @property
    def strike_factor(self) -> float:
        value = self._future_option_json.get("strike-factor", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def strike_price(self) -> float:
        value = self._future_option_json.get("strike-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def symbol(self) -> str:
        return self._future_option_json.get("symbol", "")

    @property
    def underlying_count(self) -> float:
        value = self._future_option_json.get("underlying-count", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def underlying_symbol(self) -> str:
        return self._future_option_json.get("underlying-symbol", "")

    @property
    def future_option_product(self) -> FutureOptionProduct | None:
        product_data = self._future_option_json.get("future-option-product", {})
        return FutureOptionProduct(product_data) if product_data else None

    def __str__(self) -> str:
        return f"FutureOption({self.symbol}): {self.underlying_symbol} {self.option_type} {self.strike_price} exp {self.expiration_date}"

    def print_summary(self) -> None:
        """Print a simple text summary of the futures option."""
        print(f"\n{'=' * 60}")
        print(f"FUTURES OPTION SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Underlying Symbol: {self.underlying_symbol}")
        print(f"Option Type: {self.option_type}")
        print(f"Strike Price: {self.strike_price}")
        print(f"Expiration Date: {self.expiration_date}")
        print(f"Days to Expiration: {self.days_to_expiration}")
        print(f"Exchange: {self.exchange}")

        # Contract specifications
        print(f"Exercise Style: {self.exercise_style}")
        print(f"Settlement Type: {self.settlement_type}")
        print(f"Multiplier: {self.multiplier}")
        print(f"Strike Factor: {self.strike_factor}")
        print(f"Display Factor: {self.display_factor}")
        print(f"Future Price Ratio: {self.future_price_ratio}")
        print(f"Notional Value: {self.notional_value}")
        print(f"Underlying Count: {self.underlying_count}")

        # Status and classifications
        print(f"Active: {self.active}")
        print(f"Is Closing Only: {self.is_closing_only}")
        print(f"Is Confirmed: {self.is_confirmed}")
        print(f"Is Vanilla: {self.is_vanilla}")
        print(f"Is Primary Deliverable: {self.is_primary_deliverable}")
        print(f"Is Exercisable Weekly: {self.is_exercisable_weekly}")

        # Identifiers and symbols
        print(f"Product Code: {self.product_code}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Option Root Symbol: {self.option_root_symbol}")
        print(f"Security ID: {self.security_id}")
        print(f"Streamer Symbol: {self.streamer_symbol}")

        # Important dates/times
        if self.maturity_date:
            print(f"Maturity Date: {self.maturity_date}")
        if self.expires_at:
            print(f"Expires At: {self.expires_at}")
        if self.stops_trading_at:
            print(f"Stops Trading At: {self.stops_trading_at}")
        if self.last_trade_time:
            print(f"Last Trade Time: {self.last_trade_time}")

        # Product information
        if self.future_option_product:
            print(f"Future Option Product: {self.future_option_product.code}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all futures option data in nicely formatted tables."""
        console = Console()

        # Create basic option information table
        basic_table = Table(
            title=f"Futures Option: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Symbol", str(self.symbol))
        basic_table.add_row("Underlying Symbol", str(self.underlying_symbol))
        basic_table.add_row("Option Type", str(self.option_type))
        basic_table.add_row("Strike Price", f"{self.strike_price:,.2f}")
        basic_table.add_row(
            "Expiration Date",
            str(self.expiration_date) if self.expiration_date else "N/A",
        )
        basic_table.add_row("Days to Expiration", str(self.days_to_expiration))
        basic_table.add_row("Exchange", str(self.exchange))
        basic_table.add_row("Product Code", str(self.product_code))

        # Contract specifications table
        contract_table = Table(
            title="Contract Specifications",
            show_header=True,
            header_style="bold green",
        )
        contract_table.add_column("Property", style="cyan")
        contract_table.add_column("Value", style="green")

        contract_table.add_row("Exercise Style", str(self.exercise_style))
        contract_table.add_row("Settlement Type", str(self.settlement_type))
        contract_table.add_row("Multiplier", f"{self.multiplier:,.2f}")
        contract_table.add_row("Strike Factor", f"{self.strike_factor:g}")
        contract_table.add_row("Display Factor", f"{self.display_factor:g}")
        contract_table.add_row("Future Price Ratio", f"{self.future_price_ratio:g}")
        contract_table.add_row("Notional Value", f"{self.notional_value:,.2f}")
        contract_table.add_row("Underlying Count", f"{self.underlying_count:g}")

        # Status and classifications table
        status_table = Table(
            title="Status & Classifications",
            show_header=True,
            header_style="bold yellow",
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Active", "Yes" if self.active else "No")
        status_table.add_row("Is Closing Only", "Yes" if self.is_closing_only else "No")
        status_table.add_row("Is Confirmed", "Yes" if self.is_confirmed else "No")
        status_table.add_row("Is Vanilla", "Yes" if self.is_vanilla else "No")
        status_table.add_row(
            "Is Primary Deliverable", "Yes" if self.is_primary_deliverable else "No"
        )
        status_table.add_row(
            "Is Exercisable Weekly", "Yes" if self.is_exercisable_weekly else "No"
        )

        # Identifiers table
        identifiers_table = Table(
            title="Identifiers & Symbols",
            show_header=True,
            header_style="bold magenta",
        )
        identifiers_table.add_column("Property", style="cyan")
        identifiers_table.add_column("Value", style="green")

        identifiers_table.add_row("Root Symbol", str(self.root_symbol))
        identifiers_table.add_row("Option Root Symbol", str(self.option_root_symbol))
        identifiers_table.add_row("Security ID", str(self.security_id))
        identifiers_table.add_row("Streamer Symbol", str(self.streamer_symbol))

        # Dates and times table
        dates_table = Table(
            title="Important Dates & Times",
            show_header=True,
            header_style="bold cyan",
        )
        dates_table.add_column("Property", style="cyan")
        dates_table.add_column("Value", style="green")

        if self.maturity_date:
            dates_table.add_row("Maturity Date", str(self.maturity_date))
        if self.expires_at:
            dates_table.add_row("Expires At", str(self.expires_at))
        if self.stops_trading_at:
            dates_table.add_row("Stops Trading At", str(self.stops_trading_at))
        if self.last_trade_time:
            dates_table.add_row("Last Trade Time", str(self.last_trade_time))

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
                contract_table,
                title="[bold green]Contract Specifications[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                status_table,
                title="[bold yellow]Status & Classifications[/bold yellow]",
                border_style="yellow",
            )
        )

        console.print(
            Panel(
                identifiers_table,
                title="[bold magenta]Identifiers & Symbols[/bold magenta]",
                border_style="magenta",
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

        # Show future option product details if available
        if self.future_option_product:
            console.print("\n[bold]Future Option Product Details:[/bold]")
            self.future_option_product.pretty_print()
