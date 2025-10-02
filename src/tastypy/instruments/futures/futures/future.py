from ....session import Session
from ....errors import translate_error_code
from .future_etf_equivalent import FutureETFEquivalent
from ..products.future_product import FutureProduct
from ...common.tick_sizes import TickSizes
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Future:
    _session: Session
    _endpoint_url: str = ""
    _future_json: dict = {}

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self, symbol: str):
        """Fetch the latest data for the specified future symbol."""
        self._endpoint_url = f"/instruments/futures/{symbol}"

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            self._future_json = data.get("data", {})
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def active(self) -> bool:
        return self._future_json.get("active", False)

    @property
    def active_month(self) -> bool:
        return self._future_json.get("active-month", False)

    @property
    def back_month_first_calendar_symbol(self) -> bool:
        return self._future_json.get("back-month-first-calendar-symbol", False)

    @property
    def closing_only_date(self) -> datetime.date | None:
        date_str = self._future_json.get("closing-only-date", "")
        if date_str:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    @property
    def contract_size(self) -> float:
        value = self._future_json.get("contract-size", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def display_factor(self) -> float:
        value = self._future_json.get("display-factor", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def exchange(self) -> str:
        return self._future_json.get("exchange", "")

    @property
    def exchange_symbol(self) -> str:
        return self._future_json.get("exchange-symbol", "")

    @property
    def expiration_date(self) -> datetime.date | None:
        date_str = self._future_json.get("expiration-date", "")
        if date_str:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    @property
    def expires_at(self) -> datetime.datetime | None:
        datetime_str = self._future_json.get("expires-at", "")
        if datetime_str:
            try:
                # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
                return datetime.datetime.fromisoformat(
                    datetime_str.replace("Z", "+00:00")
                )
            except ValueError:
                return None
        return None

    @property
    def first_notice_date(self) -> datetime.date | None:
        date_str = self._future_json.get("first-notice-date", "")
        if date_str:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    @property
    def product_group(self) -> str:
        return self._future_json.get("product-group", "")

    @property
    def is_closing_only(self) -> bool:
        return self._future_json.get("is-closing-only", False)

    @property
    def last_trade_date(self) -> datetime.date | None:
        date_str = self._future_json.get("last-trade-date", "")
        if date_str:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    @property
    def main_fraction(self) -> float:
        value = self._future_json.get("main-fraction", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def next_active_month(self) -> bool:
        return self._future_json.get("next-active-month", False)

    @property
    def notional_multiplier(self) -> float:
        value = self._future_json.get("notional-multiplier", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def product_code(self) -> str:
        return self._future_json.get("product-code", "")

    @property
    def roll_target_symbol(self) -> str:
        return self._future_json.get("roll-target-symbol", "")

    @property
    def security_id(self) -> str:
        return self._future_json.get("security-id", "")

    @property
    def stops_trading_at(self) -> datetime.datetime | None:
        datetime_str = self._future_json.get("stops-trading-at", "")
        if datetime_str:
            try:
                # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
                return datetime.datetime.fromisoformat(
                    datetime_str.replace("Z", "+00:00")
                )
            except ValueError:
                return None
        return None

    @property
    def streamer_exchange_code(self) -> str:
        return self._future_json.get("streamer-exchange-code", "")

    @property
    def streamer_symbol(self) -> str:
        return self._future_json.get("streamer-symbol", "")

    @property
    def sub_fraction(self) -> float:
        value = self._future_json.get("sub-fraction", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def symbol(self) -> str:
        return self._future_json.get("symbol", "")

    @property
    def tick_size(self) -> float:
        value = self._future_json.get("tick-size", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def is_tradeable(self) -> bool:
        return self._future_json.get("is-tradeable", False)

    @property
    def true_underlying_symbol(self) -> str:
        return self._future_json.get("true-underlying-symbol", "")

    @property
    def future_etf_equivalent(self) -> FutureETFEquivalent | None:
        etf_json = self._future_json.get("future-etf-equivalent")
        if etf_json:
            return FutureETFEquivalent(etf_json)
        return None

    @property
    def future_product(self) -> FutureProduct | None:
        product_json = self._future_json.get("future-product")
        if product_json:
            return FutureProduct.from_json(self._session, product_json)
        return None

    @property
    def option_tick_sizes(self) -> list[TickSizes] | None:
        tick_sizes_json = self._future_json.get("option-tick-sizes")
        if tick_sizes_json:
            return [TickSizes(ts) for ts in tick_sizes_json]
        return None

    @property
    def tick_sizes(self) -> list[TickSizes] | None:
        tick_sizes_json = self._future_json.get("tick-sizes")
        if tick_sizes_json:
            return [TickSizes(ts) for ts in tick_sizes_json]
        return None

    def print_summary(self) -> None:
        """Print a simple text summary of the future contract."""
        print(f"\n{'=' * 60}")
        print(f"FUTURE CONTRACT SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Exchange Symbol: {self.exchange_symbol}")
        print(f"Product Code: {self.product_code}")
        print(f"Exchange: {self.exchange}")
        print(f"Contract Size: {self.contract_size:,.2f}")
        print(f"Tick Size: {self.tick_size:g}")

        # Expiration information
        if self.expiration_date:
            print(f"Expiration Date: {self.expiration_date}")
        if self.expires_at:
            print(f"Expires At: {self.expires_at}")
        if self.stops_trading_at:
            print(f"Stops Trading At: {self.stops_trading_at}")
        if self.last_trade_date:
            print(f"Last Trade Date: {self.last_trade_date}")
        if self.first_notice_date:
            print(f"First Notice Date: {self.first_notice_date}")
        if self.closing_only_date:
            print(f"Closing Only Date: {self.closing_only_date}")

        # Status information
        print(f"Active: {self.active}")
        print(f"Active Month: {self.active_month}")
        print(f"Next Active Month: {self.next_active_month}")
        print(f"Is Tradeable: {self.is_tradeable}")
        print(f"Is Closing Only: {self.is_closing_only}")

        # Additional details
        print(f"Display Factor: {self.display_factor:g}")
        print(f"Notional Multiplier: {self.notional_multiplier:,.2f}")
        print(f"Main Fraction: {self.main_fraction:g}")
        print(f"Sub Fraction: {self.sub_fraction:g}")

        # Identifiers
        print(f"Security ID: {self.security_id}")
        print(f"Streamer Symbol: {self.streamer_symbol}")
        print(f"Streamer Exchange Code: {self.streamer_exchange_code}")
        if self.true_underlying_symbol:
            print(f"True Underlying Symbol: {self.true_underlying_symbol}")
        if self.roll_target_symbol:
            print(f"Roll Target Symbol: {self.roll_target_symbol}")
        if self.product_group:
            print(f"Product Group: {self.product_group}")

        # Tick sizes information
        if self.tick_sizes:
            print(f"Tick Sizes: {len(self.tick_sizes)} defined")
        if self.option_tick_sizes:
            print(f"Option Tick Sizes: {len(self.option_tick_sizes)} defined")

        # Related objects
        if self.future_etf_equivalent:
            print(
                f"ETF Equivalent: {self.future_etf_equivalent.symbol} ({self.future_etf_equivalent.share_quantity:,} shares)"
            )
        if self.future_product:
            print(f"Future Product: {self.future_product.code}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all future contract data in nicely formatted tables."""
        console = Console()

        # Create basic contract information table
        basic_table = Table(
            title=f"Future Contract: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Symbol", str(self.symbol))
        basic_table.add_row("Exchange Symbol", str(self.exchange_symbol))
        basic_table.add_row("Product Code", str(self.product_code))
        basic_table.add_row("Exchange", str(self.exchange))
        basic_table.add_row("Contract Size", f"{self.contract_size:,.2f}")
        basic_table.add_row("Tick Size", f"{self.tick_size:g}")
        if self.product_group:
            basic_table.add_row("Product Group", str(self.product_group))

        # Contract specifications table
        contract_table = Table(
            title="Contract Specifications",
            show_header=True,
            header_style="bold green",
        )
        contract_table.add_column("Property", style="cyan")
        contract_table.add_column("Value", style="green")

        contract_table.add_row("Display Factor", f"{self.display_factor:g}")
        contract_table.add_row(
            "Notional Multiplier", f"{self.notional_multiplier:,.2f}"
        )
        contract_table.add_row("Main Fraction", f"{self.main_fraction:g}")
        contract_table.add_row("Sub Fraction", f"{self.sub_fraction:g}")
        contract_table.add_row(
            "Back Month First Calendar Symbol",
            "Yes" if self.back_month_first_calendar_symbol else "No",
        )

        # Dates table
        dates_table = Table(
            title="Important Dates",
            show_header=True,
            header_style="bold yellow",
        )
        dates_table.add_column("Property", style="cyan")
        dates_table.add_column("Value", style="green")

        if self.expiration_date:
            dates_table.add_row("Expiration Date", str(self.expiration_date))
        if self.expires_at:
            dates_table.add_row("Expires At", str(self.expires_at))
        if self.stops_trading_at:
            dates_table.add_row("Stops Trading At", str(self.stops_trading_at))
        if self.last_trade_date:
            dates_table.add_row("Last Trade Date", str(self.last_trade_date))
        if self.first_notice_date:
            dates_table.add_row("First Notice Date", str(self.first_notice_date))
        if self.closing_only_date:
            dates_table.add_row("Closing Only Date", str(self.closing_only_date))

        # Status table
        status_table = Table(
            title="Status & Trading",
            show_header=True,
            header_style="bold magenta",
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Active", "Yes" if self.active else "No")
        status_table.add_row("Active Month", "Yes" if self.active_month else "No")
        status_table.add_row(
            "Next Active Month", "Yes" if self.next_active_month else "No"
        )
        status_table.add_row("Is Tradeable", "Yes" if self.is_tradeable else "No")
        status_table.add_row("Is Closing Only", "Yes" if self.is_closing_only else "No")

        # Identifiers table
        identifiers_table = Table(
            title="Identifiers & Symbols",
            show_header=True,
            header_style="bold cyan",
        )
        identifiers_table.add_column("Property", style="cyan")
        identifiers_table.add_column("Value", style="green")

        identifiers_table.add_row("Security ID", str(self.security_id))
        identifiers_table.add_row("Streamer Symbol", str(self.streamer_symbol))
        identifiers_table.add_row(
            "Streamer Exchange Code", str(self.streamer_exchange_code)
        )
        if self.true_underlying_symbol:
            identifiers_table.add_row(
                "True Underlying Symbol", str(self.true_underlying_symbol)
            )
        if self.roll_target_symbol:
            identifiers_table.add_row(
                "Roll Target Symbol", str(self.roll_target_symbol)
            )

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

        # Only show dates table if there are dates
        if dates_table.row_count > 0:
            console.print(
                Panel(
                    dates_table,
                    title="[bold yellow]Important Dates[/bold yellow]",
                    border_style="yellow",
                )
            )

        console.print(
            Panel(
                status_table,
                title="[bold magenta]Status & Trading[/bold magenta]",
                border_style="magenta",
            )
        )

        console.print(
            Panel(
                identifiers_table,
                title="[bold cyan]Identifiers & Symbols[/bold cyan]",
                border_style="cyan",
            )
        )

        # Show tick sizes if available
        if self.tick_sizes:
            console.print("\n[bold]Tick Sizes:[/bold]")
            for i, tick_size in enumerate(self.tick_sizes, 1):
                console.print(f"\n[cyan]Tick Size {i}:[/cyan]")
                tick_size.pretty_print()

        if self.option_tick_sizes:
            console.print("\n[bold]Option Tick Sizes:[/bold]")
            for i, tick_size in enumerate(self.option_tick_sizes, 1):
                console.print(f"\n[cyan]Option Tick Size {i}:[/cyan]")
                tick_size.pretty_print()

        # Show ETF equivalent if available
        if self.future_etf_equivalent:
            console.print("\n[bold]ETF Equivalent:[/bold]")
            self.future_etf_equivalent.pretty_print()

        # Show future product details if available
        if self.future_product:
            console.print("\n[bold]Future Product Details:[/bold]")
            self.future_product.pretty_print()
