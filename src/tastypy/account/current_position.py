import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class CurrentPosition:
    _position_json: dict

    def __init__(self, position_json: dict):
        self._position_json = position_json

    @property
    def account_number(self) -> str:
        return self._position_json.get("account-number", "")

    @property
    def instrument_type(self) -> str:
        return self._position_json.get("instrument-type", "")

    @property
    def symbol(self) -> str:
        return self._position_json.get("symbol", "")

    @property
    def underlying_symbol(self) -> str:
        return self._position_json.get("underlying-symbol", "")

    @property
    def quantity(self) -> int:
        return int(self._position_json.get("quantity", 0))

    @property
    def average_daily_market_close_price(self) -> float:
        value = self._position_json.get("average-daily-market-close-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def average_open_price(self) -> float:
        value = self._position_json.get("average-open-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def average_yearly_market_close_price(self) -> float:
        value = self._position_json.get("average-yearly-market-close-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def close_price(self) -> float:
        value = self._position_json.get("close-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cost_effect(self) -> str:
        return self._position_json.get("cost-effect", "")

    @property
    def is_frozen(self) -> bool:
        return self._position_json.get("is-frozen", False)

    @property
    def is_suppressed(self) -> bool:
        return self._position_json.get("is-suppressed", False)

    @property
    def mark(self) -> float:
        value = self._position_json.get("mark", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def mark_price(self) -> float:
        value = self._position_json.get("mark-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def multiplier(self) -> int:
        value = self._position_json.get("multiplier", 1)
        return int(value) if value is not None else 1

    @property
    def quantity_direction(self) -> str:
        return self._position_json.get("quantity-direction", "")

    @property
    def restricted_quantity(self) -> dict:
        return self._position_json.get("restricted-quantity", {})

    @property
    def expires_at(self) -> datetime.datetime | None:
        expires_at = self._position_json.get("expires-at", "")
        if not expires_at:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(expires_at.replace("Z", "+00:00"))

    @property
    def deliverable_type(self) -> str:
        return self._position_json.get("deliverable-type", "")

    @property
    def fixing_price(self) -> float:
        value = self._position_json.get("fixing-price", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def realized_day_gain(self) -> float:
        value = self._position_json.get("realized-day-gain", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def realized_day_gain_date(self) -> datetime.date | None:
        realized_day_gain_date_str = self._position_json.get(
            "realized-day-gain-date", ""
        )
        if not realized_day_gain_date_str:
            return None
        # This is just YYY-MM-DD
        return datetime.datetime.strptime(realized_day_gain_date_str, "%Y-%m-%d").date()

    @property
    def realized_day_gain_effect(self) -> str:
        return self._position_json.get("realized-day-gain-effect", "")

    @property
    def realized_today(self) -> float:
        value = self._position_json.get("realized-today", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def realized_today_date(self) -> datetime.date | None:
        realized_today_date_str = self._position_json.get("realized-today-date", "")
        if not realized_today_date_str:
            return None
        # This is just YYY-MM-DD
        return datetime.datetime.strptime(realized_today_date_str, "%Y-%m-%d").date()

    @property
    def realized_today_effect(self) -> str:
        return self._position_json.get("realized-today-effect", "")

    @property
    def face_value(self) -> float:
        value = self._position_json.get("face-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def par_size(self) -> float:
        value = self._position_json.get("par-size", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def created_at(self) -> datetime.datetime | None:
        created_at = self._position_json.get("created-at", "")
        if not created_at:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))

    @property
    def updated_at(self) -> datetime.datetime | None:
        updated_at = self._position_json.get("updated-at", "")
        if not updated_at:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(updated_at.replace("Z", "+00:00"))

    @property
    def order_id(self) -> int:
        value = self._position_json.get("order-id", 0)
        return int(value) if value is not None else 0

    @property
    def update_type(self) -> str:
        return self._position_json.get("update-type", "")

    def __str__(self) -> str:
        return f"Position({self.symbol}, {self.instrument_type})"

    def print_summary(self) -> None:
        """Print a simple text summary of the position."""
        print(f"\n{'=' * 60}")
        print(f"POSITION SUMMARY: {self.symbol}")
        print(f"{'=' * 60}")
        print(f"Account Number: {self.account_number}")
        print(f"Symbol: {self.symbol}")
        print(f"Underlying Symbol: {self.underlying_symbol}")
        print(f"Instrument Type: {self.instrument_type}")

        # Quantity information
        quantity = self.quantity
        if quantity:
            print(f"Quantity: {quantity}")
        print(f"Quantity Direction: {self.quantity_direction}")

        # Price information
        print(f"Mark Price: ${self.mark_price:,.2f}")
        print(f"Mark: ${self.mark:,.2f}")
        print(f"Close Price: ${self.close_price:,.2f}")
        print(f"Average Open Price: ${self.average_open_price:,.2f}")
        print(
            f"Average Daily Market Close Price: ${self.average_daily_market_close_price:,.2f}"
        )
        print(
            f"Average Yearly Market Close Price: ${self.average_yearly_market_close_price:,.2f}"
        )

        # Additional information
        print(f"Multiplier: {self.multiplier}")
        print(f"Cost Effect: {self.cost_effect}")
        print(f"Is Frozen: {self.is_frozen}")
        print(f"Is Suppressed: {self.is_suppressed}")

        # Realized gains
        if self.realized_day_gain != 0.0:
            print(
                f"Realized Day Gain: ${self.realized_day_gain:,.2f} ({self.realized_day_gain_effect})"
            )
            if self.realized_day_gain_date:
                print(f"Realized Day Gain Date: {self.realized_day_gain_date}")

        if self.realized_today != 0.0:
            print(
                f"Realized Today: ${self.realized_today:,.2f} ({self.realized_today_effect})"
            )
            if self.realized_today_date:
                print(f"Realized Today Date: {self.realized_today_date}")

        # Dates
        if self.expires_at:
            print(f"Expires At: {self.expires_at}")
        if self.created_at:
            print(f"Created At: {self.created_at}")
        if self.updated_at:
            print(f"Updated At: {self.updated_at}")

        # Additional fields for bonds/fixed income
        if self.face_value != 0.0:
            print(f"Face Value: ${self.face_value:,.2f}")
        if self.par_size != 0.0:
            print(f"Par Size: {self.par_size}")
        if self.fixing_price != 0.0:
            print(f"Fixing Price: ${self.fixing_price:,.2f}")

        # Order information
        if self.order_id != 0:
            print(f"Order ID: {self.order_id}")
        if self.update_type:
            print(f"Update Type: {self.update_type}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all position data in a nicely formatted table."""
        console = Console()

        # Create basic position information table
        basic_table = Table(
            title=f"Position: {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Account Number", str(self.account_number))
        basic_table.add_row("Symbol", str(self.symbol))
        basic_table.add_row("Underlying Symbol", str(self.underlying_symbol))
        basic_table.add_row("Instrument Type", str(self.instrument_type))
        basic_table.add_row("Quantity Direction", str(self.quantity_direction))
        basic_table.add_row("Deliverable Type", str(self.deliverable_type))
        basic_table.add_row("Cost Effect", str(self.cost_effect))
        basic_table.add_row("Is Frozen", str(self.is_frozen))
        basic_table.add_row("Is Suppressed", str(self.is_suppressed))

        # Quantity table
        quantity_table = Table(
            title="Quantity Information",
            show_header=True,
            header_style="bold green",
        )
        quantity_table.add_column("Type", style="cyan")
        quantity_table.add_column("Value", style="green")

        quantity = self.quantity
        if quantity:
            quantity_table.add_row("Quantity", str(quantity))

        restricted_quantity = self.restricted_quantity
        if restricted_quantity:
            quantity_table.add_row("--- Restricted Quantities ---", "")
            for key, value in restricted_quantity.items():
                quantity_table.add_row(
                    f"Restricted {key.replace('-', ' ').title()}", str(value)
                )

        quantity_table.add_row("Multiplier", str(self.multiplier))

        # Price information table
        price_table = Table(
            title="Price Information",
            show_header=True,
            header_style="bold yellow",
        )
        price_table.add_column("Price Type", style="cyan")
        price_table.add_column("Amount", style="green")

        price_table.add_row("Mark Price", f"${self.mark_price:,.2f}")
        price_table.add_row("Mark", f"${self.mark:,.2f}")
        price_table.add_row("Close Price", f"${self.close_price:,.2f}")
        price_table.add_row("Average Open Price", f"${self.average_open_price:,.2f}")
        price_table.add_row(
            "Average Daily Market Close Price",
            f"${self.average_daily_market_close_price:,.2f}",
        )
        price_table.add_row(
            "Average Yearly Market Close Price",
            f"${self.average_yearly_market_close_price:,.2f}",
        )

        if self.fixing_price != 0.0:
            price_table.add_row("Fixing Price", f"${self.fixing_price:,.2f}")

        # Realized gains table
        gains_table = Table(
            title="Realized Gains/Losses",
            show_header=True,
            header_style="bold red",
        )
        gains_table.add_column("Type", style="cyan")
        gains_table.add_column("Amount", style="green")
        gains_table.add_column("Effect", style="yellow")
        gains_table.add_column("Date", style="blue")

        if self.realized_day_gain != 0.0:
            gains_table.add_row(
                "Day Gain",
                f"${self.realized_day_gain:,.2f}",
                str(self.realized_day_gain_effect),
                (
                    str(self.realized_day_gain_date)
                    if self.realized_day_gain_date
                    else "N/A"
                ),
            )

        if self.realized_today != 0.0:
            gains_table.add_row(
                "Today",
                f"${self.realized_today:,.2f}",
                str(self.realized_today_effect),
                str(self.realized_today_date) if self.realized_today_date else "N/A",
            )

        # Dates and metadata table
        dates_table = Table(
            title="Dates & Metadata",
            show_header=True,
            header_style="bold magenta",
        )
        dates_table.add_column("Property", style="cyan")
        dates_table.add_column("Value", style="green")

        if self.expires_at:
            dates_table.add_row("Expires At", str(self.expires_at))
        if self.created_at:
            dates_table.add_row("Created At", str(self.created_at))
        if self.updated_at:
            dates_table.add_row("Updated At", str(self.updated_at))
        if self.order_id != 0:
            dates_table.add_row("Order ID", str(self.order_id))
        if self.update_type:
            dates_table.add_row("Update Type", str(self.update_type))

        # Bond/Fixed Income specific information
        bond_table = None
        if self.face_value != 0.0 or self.par_size != 0.0:
            bond_table = Table(
                title="Bond/Fixed Income Information",
                show_header=True,
                header_style="bold cyan",
            )
            bond_table.add_column("Property", style="cyan")
            bond_table.add_column("Value", style="green")

            if self.face_value != 0.0:
                bond_table.add_row("Face Value", f"${self.face_value:,.2f}")
            if self.par_size != 0.0:
                bond_table.add_row("Par Size", str(self.par_size))

        # Print all tables
        console.print(
            Panel(
                basic_table,
                title="[bold blue]Basic Information[/bold blue]",
                border_style="blue",
            )
        )

        if quantity or restricted_quantity:
            console.print(
                Panel(
                    quantity_table,
                    title="[bold green]Quantity Information[/bold green]",
                    border_style="green",
                )
            )

        console.print(
            Panel(
                price_table,
                title="[bold yellow]Price Information[/bold yellow]",
                border_style="yellow",
            )
        )

        if self.realized_day_gain != 0.0 or self.realized_today != 0.0:
            console.print(
                Panel(
                    gains_table,
                    title="[bold red]Realized Gains/Losses[/bold red]",
                    border_style="red",
                )
            )

        if (
            self.expires_at
            or self.created_at
            or self.updated_at
            or self.order_id != 0
            or self.update_type
        ):
            console.print(
                Panel(
                    dates_table,
                    title="[bold magenta]Dates & Metadata[/bold magenta]",
                    border_style="magenta",
                )
            )

        if bond_table:
            console.print(
                Panel(
                    bond_table,
                    title="[bold cyan]Bond/Fixed Income Information[/bold cyan]",
                    border_style="cyan",
                )
            )
