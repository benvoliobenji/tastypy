import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class EquityOption:
    """
    Represents an equity option instrument.
    """

    _option_json: dict

    def __init__(self, option_json: dict):
        self._option_json = option_json

    @property
    def active(self) -> bool:
        return self._option_json.get("active", False)

    @property
    def days_to_expiration(self) -> int:
        return self._option_json.get("days-to-expiration", 0)

    @property
    def exercise_style(self) -> str:
        return self._option_json.get("exercise-style", "")

    @property
    def expiration_date(self) -> datetime.date | None:
        date_str = self._option_json.get("expiration-date", "")
        if date_str:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return None

    @property
    def expiration_type(self) -> str:
        return self._option_json.get("expiration-type", "")

    @property
    def expires_at(self) -> datetime.datetime | None:
        expires_at = self._option_json.get("expires-at", "")
        if expires_at:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        return None

    @property
    def halted_at(self) -> datetime.datetime | None:
        halted_at = self._option_json.get("halted-at", "")
        if halted_at:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(halted_at.replace("Z", "+00:00"))
        return None

    @property
    def instrument_type(self) -> str:
        return self._option_json.get("instrument-type", "")

    @property
    def is_closing_only(self) -> bool:
        return self._option_json.get("is-closing-only", False)

    @property
    def listed_market(self) -> str:
        return self._option_json.get("listed-market", "")

    @property
    def market_time_instrument_collection(self) -> str:
        return self._option_json.get("market-time-instrument-collection", "")

    @property
    def old_security_number(self) -> str:
        return self._option_json.get("old-security-number", "")

    @property
    def option_chain_type(self) -> str:
        return self._option_json.get("option-chain-type", "")

    @property
    def option_type(self) -> str:
        return self._option_json.get("option-type", "")

    @property
    def root_symtol(self) -> str:
        return self._option_json.get("root-symbol", "")

    @property
    def settlement_type(self) -> str:
        return self._option_json.get("settlement-type", "")

    @property
    def shares_per_contract(self) -> int:
        value = self._option_json.get("shares-per-contract", 100)
        return int(value) if value is not None else 100

    @property
    def stops_trading_at(self) -> datetime.datetime | None:
        stops_trading_at = self._option_json.get("stops-trading-at", "")
        if stops_trading_at:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(
                stops_trading_at.replace("Z", "+00:00")
            )
        return None

    @property
    def streamer_symbol(self) -> str:
        return self._option_json.get("streamer-symbol", "")

    @property
    def strike_price(self) -> float:
        value = self._option_json.get("strike-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def symbol(self) -> str:
        return self._option_json.get("symbol", "")

    @property
    def underlying_symbol(self) -> str:
        return self._option_json.get("underlying-symbol", "")

    def __str__(self) -> str:
        return f"EquityOption({self.symbol}): {self.underlying_symbol} {self.option_type} {self.strike_price} Exp: {self.expiration_date}"

    def print_summary(self) -> None:
        """Print a simple text summary of the equity option."""
        print(f"\n{'=' * 60}")
        print(f"EQUITY OPTION SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Symbol: {self.symbol}")
        print(f"Underlying Symbol: {self.underlying_symbol}")
        print(f"Option Type: {self.option_type}")
        print(f"Strike Price: ${self.strike_price:,.2f}")
        print(f"Expiration Date: {self.expiration_date}")
        print(f"Days to Expiration: {self.days_to_expiration}")
        print(f"Instrument Type: {self.instrument_type}")

        # Contract specifications
        print(f"Shares Per Contract: {self.shares_per_contract}")
        print(f"Exercise Style: {self.exercise_style}")
        print(f"Settlement Type: {self.settlement_type}")
        print(f"Expiration Type: {self.expiration_type}")

        # Trading status
        print(f"Active: {self.active}")
        print(f"Is Closing Only: {self.is_closing_only}")

        # Market information
        print(f"Listed Market: {self.listed_market}")
        print(f"Option Chain Type: {self.option_chain_type}")
        print(f"Streamer Symbol: {self.streamer_symbol}")
        print(
            f"Market Time Instrument Collection: {self.market_time_instrument_collection}"
        )

        # Additional identifiers
        print(f"Root Symbol: {self.root_symtol}")
        if self.old_security_number:
            print(f"Old Security Number: {self.old_security_number}")

        # Important dates/times
        if self.expires_at:
            print(f"Expires At: {self.expires_at}")
        if self.halted_at:
            print(f"Halted At: {self.halted_at}")
        if self.stops_trading_at:
            print(f"Stops Trading At: {self.stops_trading_at}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all equity option data in nicely formatted tables."""
        console = Console()

        # Create basic option information table
        basic_table = Table(
            title=f"Equity Option: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Symbol", str(self.symbol))
        basic_table.add_row("Underlying Symbol", str(self.underlying_symbol))
        basic_table.add_row("Option Type", str(self.option_type))
        basic_table.add_row("Strike Price", f"${self.strike_price:,.2f}")
        basic_table.add_row(
            "Expiration Date",
            str(self.expiration_date) if self.expiration_date else "N/A",
        )
        basic_table.add_row("Days to Expiration", str(self.days_to_expiration))
        basic_table.add_row("Instrument Type", str(self.instrument_type))
        basic_table.add_row("Root Symbol", str(self.root_symtol))

        # Contract specifications table
        contract_table = Table(
            title="Contract Specifications",
            show_header=True,
            header_style="bold green",
        )
        contract_table.add_column("Property", style="cyan")
        contract_table.add_column("Value", style="green")

        contract_table.add_row("Shares Per Contract", str(self.shares_per_contract))
        contract_table.add_row("Exercise Style", str(self.exercise_style))
        contract_table.add_row("Settlement Type", str(self.settlement_type))
        contract_table.add_row("Expiration Type", str(self.expiration_type))
        contract_table.add_row("Option Chain Type", str(self.option_chain_type))

        # Trading status table
        trading_table = Table(
            title="Trading Status",
            show_header=True,
            header_style="bold yellow",
        )
        trading_table.add_column("Property", style="cyan")
        trading_table.add_column("Value", style="green")

        trading_table.add_row("Active", "Yes" if self.active else "No")
        trading_table.add_row(
            "Is Closing Only", "Yes" if self.is_closing_only else "No"
        )
        trading_table.add_row("Listed Market", str(self.listed_market))
        trading_table.add_row("Streamer Symbol", str(self.streamer_symbol))
        trading_table.add_row(
            "Market Time Instrument Collection",
            str(self.market_time_instrument_collection),
        )

        # Additional identifiers table (only if there are values)
        identifiers_table = Table(
            title="Additional Identifiers",
            show_header=True,
            header_style="bold magenta",
        )
        identifiers_table.add_column("Property", style="cyan")
        identifiers_table.add_column("Value", style="green")

        if self.old_security_number:
            identifiers_table.add_row(
                "Old Security Number", str(self.old_security_number)
            )

        # Dates and times table
        dates_table = Table(
            title="Important Dates & Times",
            show_header=True,
            header_style="bold cyan",
        )
        dates_table.add_column("Property", style="cyan")
        dates_table.add_column("Value", style="green")

        if self.expires_at:
            dates_table.add_row("Expires At", str(self.expires_at))
        if self.halted_at:
            dates_table.add_row("Halted At", str(self.halted_at))
        if self.stops_trading_at:
            dates_table.add_row("Stops Trading At", str(self.stops_trading_at))

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
                trading_table,
                title="[bold yellow]Trading Status[/bold yellow]",
                border_style="yellow",
            )
        )

        # Only show identifiers table if there are identifiers
        if identifiers_table.row_count > 0:
            console.print(
                Panel(
                    identifiers_table,
                    title="[bold magenta]Additional Identifiers[/bold magenta]",
                    border_style="magenta",
                )
            )

        # Only show dates table if there are dates
        if dates_table.row_count > 0:
            console.print(
                Panel(
                    dates_table,
                    title="[bold cyan]Important Dates[/bold cyan]",
                    border_style="cyan",
                )
            )
