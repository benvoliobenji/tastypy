from .current_position import CurrentPosition
from ..session import Session
from ..errors import translate_error_code
from typing import Optional
import enum
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class InstrumentType(enum.Enum):
    BOND = "Bond"
    CRYPTO = "Cryptocurrency"
    CURRENCY_PAIR = "Currency Pair"
    EQUITY = "Equity"
    EQUITY_OFFERING = "Equity Offering"
    EQUITY_OPTION = "Equity Option"
    FIXED_INCOME_SECURITY = "Fixed Income Security"
    FUTURE = "Future"
    FUTURE_OPTION = "Future Option"
    INDEX = "Index"
    LIQUIDITY_POOL = "Liquidity Pool"
    UNKNOWN = "Unknown"
    WARRANT = "Warrant"


class Positions:
    """Represents the positions in a Tastyworks account."""

    def __init__(self, account_number: str, session: Session):
        self._session = session
        self._url_endpoint = f"/accounts/{account_number}/positions"

    def sync(
        self,
        include_closed_positions: bool = False,
        include_marks: bool = True,
        instrument_type: Optional[InstrumentType] = None,
        net_positions: bool = False,
        symbol: Optional[str] = None,
        underlying_product_code: Optional[str] = None,
        underlying_symbol: Optional[list[str]] = None,
        partition_keys: Optional[list[str]] = None,
    ):
        params: dict = {
            "include-closed-positions": include_closed_positions,
            "include-marks": include_marks,
            "net-positions": net_positions,
        }

        if instrument_type:
            params["instrument-type"] = instrument_type.value

        if symbol:
            params["symbol"] = symbol

        if underlying_product_code:
            params["underlying-product-code"] = underlying_product_code

        if underlying_symbol:
            # Parse this as underlying-symbol[]={value1}&underlying-symbol[]={value2}
            params["underlying-symbol"] = [f"{value}" for value in underlying_symbol]

        if partition_keys:
            # Parse this as partition-keys[]={value1}&partition-keys[]={value2}
            params["partition-keys"] = [f"{value}" for value in partition_keys]

        response = self._session.client.get(self._url_endpoint, params=params)
        if response.status_code == 200:
            self._positions_data_array = (
                response.json().get("data", {}).get("items", [])
            )
            self._positions_data = [
                CurrentPosition(data) for data in self._positions_data_array
            ]
        else:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)

    @property
    def positions(self) -> list[CurrentPosition]:
        if not hasattr(self, "_positions_data"):
            raise ValueError("Positions data has not been loaded. Call sync() first.")
        return self._positions_data

    def __str__(self):
        return f"Positions: {len(self.positions)} positions loaded"

    def print_summary(self) -> None:
        """Print a simple text summary of all positions."""
        if not hasattr(self, "_positions_data"):
            print("No positions data loaded. Call sync() first.")
            return

        print(f"\n{'=' * 60}")
        print("POSITIONS SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Positions: {len(self.positions)}")

        if not self.positions:
            print("No positions found.")
            print(f"{'=' * 60}\n")
            return

        # Group positions by instrument type
        by_instrument_type = {}
        total_value = 0.0

        for position in self.positions:
            instrument_type = position.instrument_type or "Unknown"
            if instrument_type not in by_instrument_type:
                by_instrument_type[instrument_type] = []
            by_instrument_type[instrument_type].append(position)

            # Calculate position value (mark price * quantity if available)
            mark_price = position.mark_price
            quantity = position.quantity
            if quantity and mark_price:
                try:
                    total_value += mark_price * quantity * position.multiplier
                except (ValueError, TypeError):
                    pass

        print(f"Estimated Total Position Value: ${total_value:,.2f}")
        print()

        # Summary by instrument type
        print("Positions by Instrument Type:")
        for instrument_type, positions_list in by_instrument_type.items():
            print(f"  {instrument_type}: {len(positions_list)} positions")

        print()
        print("Position Details:")
        print("-" * 60)

        for i, position in enumerate(self.positions, 1):
            print(f"{i:2d}. {position.symbol} ({position.instrument_type})")
            print(f"    Quantity Direction: {position.quantity_direction}")
            print(f"    Mark Price: ${position.mark_price:,.2f}")
            if position.quantity:
                print(f"    Quantity: {position.quantity}")
            if position.underlying_symbol:
                print(f"    Underlying: {position.underlying_symbol}")
            print()

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all positions data in nicely formatted tables."""
        if not hasattr(self, "_positions_data"):
            console = Console()
            console.print("[red]No positions data loaded. Call sync() first.[/red]")
            return

        console = Console()

        if not self.positions:
            console.print(
                Panel(
                    "[yellow]No positions found.[/yellow]",
                    title="[bold blue]Positions Summary[/bold blue]",
                    border_style="blue",
                )
            )
            return

        # Summary statistics
        summary_table = Table(
            title="Positions Overview",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        # Group positions by instrument type for summary
        by_instrument_type = {}
        total_value = 0.0
        total_unrealized_pnl = 0.0

        for position in self.positions:
            instrument_type = position.instrument_type or "Unknown"
            if instrument_type not in by_instrument_type:
                by_instrument_type[instrument_type] = []
            by_instrument_type[instrument_type].append(position)

            # Calculate position value and P&L
            mark_price = position.mark_price
            quantity = position.quantity
            if quantity and mark_price:
                try:
                    position_value = mark_price * quantity * position.multiplier
                    total_value += position_value

                    # Calculate unrealized P&L if we have average open price
                    if position.average_open_price:
                        unrealized = (
                            (mark_price - position.average_open_price)
                            * quantity
                            * position.multiplier
                        )
                        total_unrealized_pnl += unrealized
                except (ValueError, TypeError):
                    pass

        summary_table.add_row("Total Positions", str(len(self.positions)))
        summary_table.add_row("Estimated Total Value", f"${total_value:,.2f}")
        summary_table.add_row(
            "Estimated Unrealized P&L", f"${total_unrealized_pnl:,.2f}"
        )
        summary_table.add_row("Instrument Types", str(len(by_instrument_type)))

        # Instrument type breakdown table
        instrument_table = Table(
            title="Positions by Instrument Type",
            show_header=True,
            header_style="bold green",
        )
        instrument_table.add_column("Instrument Type", style="cyan")
        instrument_table.add_column("Count", style="green")
        instrument_table.add_column("Estimated Value", style="yellow")

        for instrument_type, positions_list in sorted(by_instrument_type.items()):
            type_value = 0.0
            for position in positions_list:
                mark_price = position.mark_price
                quantity = position.quantity
                if quantity and mark_price:
                    try:
                        type_value += mark_price * quantity * position.multiplier
                    except (ValueError, TypeError):
                        pass

            instrument_table.add_row(
                instrument_type, str(len(positions_list)), f"${type_value:,.2f}"
            )

        # Detailed positions table
        positions_table = Table(
            title="Detailed Positions",
            show_header=True,
            header_style="bold yellow",
        )
        positions_table.add_column("#", style="dim", width=3)
        positions_table.add_column("Symbol", style="cyan", no_wrap=True)
        positions_table.add_column("Type", style="blue")
        positions_table.add_column("Direction", style="magenta")
        positions_table.add_column("Mark Price", style="green")
        positions_table.add_column("Avg Open", style="yellow")
        positions_table.add_column("Unrealized P&L", style="red")
        positions_table.add_column("Frozen", style="dim")

        for i, position in enumerate(self.positions, 1):
            # Calculate unrealized P&L
            unrealized_pnl = "N/A"
            if (
                position.mark_price
                and position.average_open_price
                and position.quantity
            ):
                try:
                    pnl = (
                        (position.mark_price - position.average_open_price)
                        * position.quantity
                        * position.multiplier
                    )
                    unrealized_pnl = f"${pnl:,.2f}"
                except Exception:
                    unrealized_pnl = "N/A"

            positions_table.add_row(
                str(i),
                position.symbol,
                (
                    position.instrument_type[:15]
                    if position.instrument_type
                    else "Unknown"
                ),
                (
                    position.quantity_direction[:6]
                    if position.quantity_direction
                    else "N/A"
                ),
                f"${position.mark_price:,.2f}" if position.mark_price else "N/A",
                (
                    f"${position.average_open_price:,.2f}"
                    if position.average_open_price
                    else "N/A"
                ),
                unrealized_pnl,
                "Yes" if position.is_frozen else "No",
            )

        # Additional details table for positions with interesting data
        details_table = Table(
            title="Position Details (Non-Zero Values)",
            show_header=True,
            header_style="bold magenta",
        )
        details_table.add_column("Symbol", style="cyan")
        details_table.add_column("Property", style="yellow")
        details_table.add_column("Value", style="green")

        for position in self.positions:
            # Show interesting non-zero values
            if position.realized_day_gain != 0.0:
                details_table.add_row(
                    position.symbol,
                    "Realized Day Gain",
                    f"${position.realized_day_gain:,.2f} ({position.realized_day_gain_effect})",
                )

            if position.realized_today != 0.0:
                details_table.add_row(
                    position.symbol,
                    "Realized Today",
                    f"${position.realized_today:,.2f} ({position.realized_today_effect})",
                )

            if position.expires_at:
                details_table.add_row(
                    position.symbol, "Expires At", str(position.expires_at)
                )

            if (
                position.underlying_symbol
                and position.underlying_symbol != position.symbol
            ):
                details_table.add_row(
                    position.symbol, "Underlying Symbol", position.underlying_symbol
                )

        # Print all tables
        console.print(
            Panel(
                summary_table,
                title="[bold blue]Positions Overview[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                instrument_table,
                title="[bold green]Breakdown by Instrument Type[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                positions_table,
                title="[bold yellow]All Positions[/bold yellow]",
                border_style="yellow",
            )
        )

        # Only show details table if there are interesting details
        if details_table.row_count > 0:
            console.print(
                Panel(
                    details_table,
                    title="[bold magenta]Additional Details[/bold magenta]",
                    border_style="magenta",
                )
            )
