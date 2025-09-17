import datetime
import enum

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..tick_sizes import TickSizes


class Lendability(enum.Enum):
    EASY_TO_BORROW = "Easy To Borrow"
    LOCATE_REQUIRED = "Locate Required (Hard to Borrow)"
    PREBORROW = "Preborrow"

    @staticmethod
    def from_string(lendability_str: str) -> "Lendability | None":
        if lendability_str == "Easy To Borrow":
            return Lendability.EASY_TO_BORROW
        elif lendability_str == "Locate Required (Hard to Borrow)":
            return Lendability.LOCATE_REQUIRED
        elif lendability_str == "Preborrow":
            return Lendability.PREBORROW
        raise ValueError(f"Unknown Lendability value: {lendability_str}")


class Equity:
    """Represents an equity instrument with various properties."""

    _equity_json: dict

    def __init__(self, equity_json: dict):
        self._equity_json = equity_json

    @property
    def active(self) -> bool:
        return self._equity_json.get("active", False)

    @property
    def borrow_rate(self) -> float:
        value = self._equity_json.get("borrow-rate", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def bypass_manual_review(self) -> bool:
        return self._equity_json.get("bypass-manual-review", False)

    @property
    def country_of_incorporation(self) -> str:
        return self._equity_json.get("country-of-incorporation", "")

    @property
    def country_of_taxation(self) -> str:
        return self._equity_json.get("country-of-taxation", "")

    @property
    def description(self) -> str:
        return self._equity_json.get("description", "")

    @property
    def halted_at(self) -> datetime.datetime | None:
        halted_at = self._equity_json.get("halted-at", "")
        if not halted_at:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(halted_at.replace("Z", "+00:00"))

    @property
    def instrument_sub_type(self) -> str:
        return self._equity_json.get("instrument-sub-type", "")

    @property
    def instrument_type(self) -> str:
        return self._equity_json.get("instrument-type", "")

    @property
    def is_closing_only(self) -> bool:
        return self._equity_json.get("is-closing-only", False)

    @property
    def is_etf(self) -> bool:
        return self._equity_json.get("is-etf", False)

    @property
    def is_fractional_quantity_eligible(self) -> bool:
        return self._equity_json.get("is-fractional-quantity-eligible", False)

    @property
    def is_illiquid(self) -> bool:
        return self._equity_json.get("is-illiquid", False)

    @property
    def is_index(self) -> bool:
        return self._equity_json.get("is-index", False)

    @property
    def is_options_closing_only(self) -> bool:
        return self._equity_json.get("is-options-closing-only", False)

    @property
    def lendability(self) -> Lendability | None:
        lendability_str = self._equity_json.get("lendability", "")
        if not lendability_str:
            return None
        try:
            return Lendability.from_string(lendability_str)
        except ValueError:
            return None

    @property
    def listed_market(self) -> str:
        return self._equity_json.get("listed-market", "")

    @property
    def market_time_instrument_collection(self) -> str:
        return self._equity_json.get("market-time-instrument-collection", "")

    @property
    def overnight_trading_permitted(self) -> bool:
        return self._equity_json.get("overnight-trading-permitted", False)

    @property
    def short_description(self) -> str:
        return self._equity_json.get("short-description", "")

    @property
    def stops_trading_at(self) -> datetime.datetime | None:
        stops_trading_at = self._equity_json.get("stops-trading-at", "")
        if not stops_trading_at:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(stops_trading_at.replace("Z", "+00:00"))

    @property
    def streamer_symbol(self) -> str:
        return self._equity_json.get("streamer-symbol", "")

    @property
    def symbol(self) -> str:
        return self._equity_json.get("symbol", "")

    @property
    def underlying_product_type(self) -> str:
        return self._equity_json.get("underlying-product-type", "")

    @property
    def option_tick_sizes(self) -> list[TickSizes] | None:
        option_tick_sizes_data = self._equity_json.get("option-tick-sizes", None)
        if option_tick_sizes_data:
            if isinstance(option_tick_sizes_data, list):
                return [TickSizes(item) for item in option_tick_sizes_data]
            else:
                return [TickSizes(option_tick_sizes_data)]
        return None

    @property
    def tick_sizes(self) -> list[TickSizes] | None:
        tick_sizes_data = self._equity_json.get("tick-sizes", None)
        if tick_sizes_data:
            if isinstance(tick_sizes_data, list):
                return [TickSizes(item) for item in tick_sizes_data]
            else:
                return [TickSizes(tick_sizes_data)]
        return None

    def __str__(self) -> str:
        return f"Equity({self.symbol}): {self.description}"

    def print_summary(self) -> None:
        """Print a simple text summary of the equity."""
        print(f"\n{'=' * 60}")
        print(f"EQUITY SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Description: {self.description}")
        print(f"Short Description: {self.short_description}")
        print(f"Instrument Type: {self.instrument_type}")
        print(f"Instrument Sub Type: {self.instrument_sub_type}")
        print(f"Active: {self.active}")

        # Trading status
        print(f"Is Closing Only: {self.is_closing_only}")
        print(f"Is Options Closing Only: {self.is_options_closing_only}")
        print(f"Overnight Trading Permitted: {self.overnight_trading_permitted}")

        # Classifications
        print(f"Is ETF: {self.is_etf}")
        print(f"Is Index: {self.is_index}")
        print(f"Is Illiquid: {self.is_illiquid}")
        print(
            f"Is Fractional Quantity Eligible: {self.is_fractional_quantity_eligible}"
        )

        # Borrowing/Lending
        print(f"Lendability: {self.lendability.value if self.lendability else 'N/A'}")
        print(f"Borrow Rate: {self.borrow_rate:.4f}%")
        print(f"Bypass Manual Review: {self.bypass_manual_review}")

        # Geographic information
        print(f"Listed Market: {self.listed_market}")
        print(f"Country of Incorporation: {self.country_of_incorporation}")
        print(f"Country of Taxation: {self.country_of_taxation}")

        # Market data
        print(f"Streamer Symbol: {self.streamer_symbol}")
        print(f"Underlying Product Type: {self.underlying_product_type}")
        print(
            f"Market Time Instrument Collection: {self.market_time_instrument_collection}"
        )

        # Important dates/times
        if self.halted_at:
            print(f"Halted At: {self.halted_at}")
        if self.stops_trading_at:
            print(f"Stops Trading At: {self.stops_trading_at}")

        # Tick sizes
        if self.tick_sizes:
            print(f"Has Tick Sizes: Yes ({len(self.tick_sizes)} entries)")
        if self.option_tick_sizes:
            print(f"Has Option Tick Sizes: Yes ({len(self.option_tick_sizes)} entries)")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all equity data in nicely formatted tables."""
        console = Console()

        # Create basic equity information table
        basic_table = Table(
            title=f"Equity: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Symbol", str(self.symbol))
        basic_table.add_row("Description", str(self.description))
        basic_table.add_row("Short Description", str(self.short_description))
        basic_table.add_row("Instrument Type", str(self.instrument_type))
        basic_table.add_row("Instrument Sub Type", str(self.instrument_sub_type))
        basic_table.add_row("Active", "Yes" if self.active else "No")
        basic_table.add_row("Listed Market", str(self.listed_market))
        basic_table.add_row("Streamer Symbol", str(self.streamer_symbol))

        # Trading status table
        trading_table = Table(
            title="Trading Status & Restrictions",
            show_header=True,
            header_style="bold green",
        )
        trading_table.add_column("Property", style="cyan")
        trading_table.add_column("Value", style="green")

        trading_table.add_row(
            "Is Closing Only", "Yes" if self.is_closing_only else "No"
        )
        trading_table.add_row(
            "Is Options Closing Only", "Yes" if self.is_options_closing_only else "No"
        )
        trading_table.add_row(
            "Overnight Trading Permitted",
            "Yes" if self.overnight_trading_permitted else "No",
        )
        trading_table.add_row(
            "Bypass Manual Review", "Yes" if self.bypass_manual_review else "No"
        )
        trading_table.add_row(
            "Is Fractional Quantity Eligible",
            "Yes" if self.is_fractional_quantity_eligible else "No",
        )

        # Classifications table
        classifications_table = Table(
            title="Classifications",
            show_header=True,
            header_style="bold yellow",
        )
        classifications_table.add_column("Property", style="cyan")
        classifications_table.add_column("Value", style="green")

        classifications_table.add_row("Is ETF", "Yes" if self.is_etf else "No")
        classifications_table.add_row("Is Index", "Yes" if self.is_index else "No")
        classifications_table.add_row(
            "Is Illiquid", "Yes" if self.is_illiquid else "No"
        )
        classifications_table.add_row(
            "Underlying Product Type", str(self.underlying_product_type)
        )

        # Borrowing/Lending table
        borrowing_table = Table(
            title="Borrowing & Lending Information",
            show_header=True,
            header_style="bold red",
        )
        borrowing_table.add_column("Property", style="cyan")
        borrowing_table.add_column("Value", style="green")

        borrowing_table.add_row(
            "Lendability", self.lendability.value if self.lendability else "N/A"
        )
        borrowing_table.add_row("Borrow Rate", f"{self.borrow_rate:.4f}%")

        # Geographic information table
        geographic_table = Table(
            title="Geographic Information",
            show_header=True,
            header_style="bold magenta",
        )
        geographic_table.add_column("Property", style="cyan")
        geographic_table.add_column("Value", style="green")

        geographic_table.add_row(
            "Country of Incorporation", str(self.country_of_incorporation)
        )
        geographic_table.add_row("Country of Taxation", str(self.country_of_taxation))
        geographic_table.add_row(
            "Market Time Instrument Collection",
            str(self.market_time_instrument_collection),
        )

        # Dates and times table
        dates_table = Table(
            title="Important Dates & Times",
            show_header=True,
            header_style="bold cyan",
        )
        dates_table.add_column("Property", style="cyan")
        dates_table.add_column("Value", style="green")

        if self.halted_at:
            dates_table.add_row("Halted At", str(self.halted_at))
        if self.stops_trading_at:
            dates_table.add_row("Stops Trading At", str(self.stops_trading_at))

        # Tick sizes table
        tick_sizes_table = Table(
            title="Tick Size Information",
            show_header=True,
            header_style="bold white",
        )
        tick_sizes_table.add_column("Type", style="cyan")
        tick_sizes_table.add_column("Available", style="green")

        tick_sizes_table.add_row(
            "Regular Tick Sizes",
            f"Yes ({len(self.tick_sizes)} entries)" if self.tick_sizes else "No",
        )
        tick_sizes_table.add_row(
            "Option Tick Sizes",
            (
                f"Yes ({len(self.option_tick_sizes)} entries)"
                if self.option_tick_sizes
                else "No"
            ),
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
                trading_table,
                title="[bold green]Trading Status[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                classifications_table,
                title="[bold yellow]Classifications[/bold yellow]",
                border_style="yellow",
            )
        )

        console.print(
            Panel(
                borrowing_table,
                title="[bold red]Borrowing & Lending[/bold red]",
                border_style="red",
            )
        )

        console.print(
            Panel(
                geographic_table,
                title="[bold magenta]Geographic Information[/bold magenta]",
                border_style="magenta",
            )
        )

        # Only show dates table if there are dates
        if self.halted_at or self.stops_trading_at:
            console.print(
                Panel(
                    dates_table,
                    title="[bold cyan]Important Dates[/bold cyan]",
                    border_style="cyan",
                )
            )

        console.print(
            Panel(
                tick_sizes_table,
                title="[bold white]Tick Size Information[/bold white]",
                border_style="white",
            )
        )

        # Show detailed tick sizes if available
        if self.tick_sizes:
            console.print("\n[bold]Regular Tick Sizes Details:[/bold]")
            for i, tick_size in enumerate(self.tick_sizes, 1):
                console.print(f"[dim]Entry {i}:[/dim]")
                tick_size.pretty_print()

        if self.option_tick_sizes:
            console.print("\n[bold]Option Tick Sizes Details:[/bold]")
            for i, tick_size in enumerate(self.option_tick_sizes, 1):
                console.print(f"[dim]Entry {i}:[/dim]")
                tick_size.pretty_print()
