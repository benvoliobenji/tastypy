"""Order data model."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.utils.decode_json import parse_date, parse_datetime, parse_float

from .enums import (
    ConfirmationStatus,
    ContingentStatus,
    OrderStatus,
    OrderType,
    PriceEffect,
    TimeInForce,
)
from .order_leg import OrderLeg
from .order_rule import OrderRule


class Order:
    """Represents a single order."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize Order from JSON data."""
        self._json = json_data
        self._legs: list[OrderLeg] = []
        self._order_rule: OrderRule | None = None

        # Parse legs if present
        legs_data = self._json.get("legs", [])
        if legs_data:
            self._legs = [OrderLeg(leg) for leg in legs_data]

        # Parse order rule if present
        rule_data = self._json.get("order-rule")
        if rule_data:
            self._order_rule = OrderRule(rule_data)

    @property
    def id(self) -> str:
        """The order ID."""
        return self._json.get("id", "")

    @property
    def account_number(self) -> str:
        """The account number."""
        return self._json.get("account-number", "")

    @property
    def cancel_user_id(self) -> str:
        """The user ID that cancelled the order."""
        return self._json.get("cancel-user-id", "")

    @property
    def cancel_username(self) -> str:
        """The username that cancelled the order."""
        return self._json.get("cancel-username", "")

    @property
    def cancellable(self) -> bool:
        """Whether the order can be cancelled."""
        return bool(self._json.get("cancellable", False))

    @property
    def cancelled_at(self) -> datetime.datetime | None:
        """When the order was cancelled."""
        return parse_datetime(self._json.get("cancelled-at"))

    @property
    def complex_order_id(self) -> str:
        """The complex order ID if part of a complex order."""
        return self._json.get("complex-order-id", "")

    @property
    def complex_order_tag(self) -> str:
        """The complex order tag."""
        return self._json.get("complex-order-tag", "")

    @property
    def confirmation_status(self) -> ConfirmationStatus | None:
        """The confirmation status."""
        value = self._json.get("confirmation-status")
        if value:
            try:
                return ConfirmationStatus(value)
            except ValueError:
                return None
        return None

    @property
    def contingent_status(self) -> ContingentStatus | None:
        """The contingent status."""
        value = self._json.get("contingent-status")
        if value:
            try:
                return ContingentStatus(value)
            except ValueError:
                return None
        return None

    @property
    def editable(self) -> bool:
        """Whether the order can be edited."""
        return bool(self._json.get("editable", False))

    @property
    def edited(self) -> bool:
        """Whether the order has been edited."""
        return bool(self._json.get("edited", False))

    @property
    def external_identifier(self) -> str:
        """External identifier for the order."""
        return self._json.get("external-identifier", "")

    @property
    def global_request_id(self) -> str:
        """Global request ID."""
        return self._json.get("global-request-id", "")

    @property
    def gtc_date(self) -> datetime.date | None:
        """The GTC date for GTD orders."""
        return parse_date(self._json.get("gtc-date"))

    @property
    def in_flight_at(self) -> datetime.datetime | None:
        """When the order was in flight."""
        return parse_datetime(self._json.get("in-flight-at"))

    @property
    def live_at(self) -> datetime.datetime | None:
        """When the order went live."""
        return parse_datetime(self._json.get("live-at"))

    @property
    def order_type(self) -> OrderType | None:
        """The type of order."""
        value = self._json.get("order-type")
        if value:
            try:
                return OrderType(value)
            except ValueError:
                return None
        return None

    @property
    def preflight_id(self) -> str:
        """Preflight ID."""
        return self._json.get("preflight-id", "")

    @property
    def price(self) -> float:
        """The price of the order."""
        return parse_float(self._json.get("price"), 0.0)

    @property
    def price_effect(self) -> PriceEffect | None:
        """If pay or receive payment for placing the order."""
        value = self._json.get("price-effect")
        if value:
            try:
                return PriceEffect(value)
            except ValueError:
                return None
        return None

    @property
    def received_at(self) -> datetime.datetime | None:
        """When the order was received."""
        return parse_datetime(self._json.get("received-at"))

    @property
    def reject_reason(self) -> str:
        """The reason for rejection if rejected."""
        return self._json.get("reject-reason", "")

    @property
    def replaces_order_id(self) -> str:
        """The order ID this order replaces."""
        return self._json.get("replaces-order-id", "")

    @property
    def replacing_order_id(self) -> str:
        """The order ID that replaces this order."""
        return self._json.get("replacing-order-id", "")

    @property
    def size(self) -> str:
        """The size of the order."""
        return self._json.get("size", "")

    @property
    def source(self) -> str:
        """The source of the order."""
        return self._json.get("source", "")

    @property
    def status(self) -> OrderStatus | None:
        """The status of the order."""
        value = self._json.get("status")
        if value:
            try:
                return OrderStatus(value)
            except ValueError:
                return None
        return None

    @property
    def stop_trigger(self) -> str:
        """The stop trigger price."""
        return self._json.get("stop-trigger", "")

    @property
    def terminal_at(self) -> datetime.datetime | None:
        """When the order reached terminal status."""
        return parse_datetime(self._json.get("terminal-at"))

    @property
    def time_in_force(self) -> TimeInForce | None:
        """The time in force."""
        value = self._json.get("time-in-force")
        if value:
            try:
                return TimeInForce(value)
            except ValueError:
                return None
        return None

    @property
    def underlying_instrument_type(self) -> str:
        """The underlying instrument type."""
        return self._json.get("underlying-instrument-type", "")

    @property
    def underlying_symbol(self) -> str:
        """The underlying symbol."""
        return self._json.get("underlying-symbol", "")

    @property
    def updated_at(self) -> str:
        """When the order was last updated."""
        return self._json.get("updated-at", "")

    @property
    def user_id(self) -> str:
        """The user ID that placed the order."""
        return self._json.get("user-id", "")

    @property
    def username(self) -> str:
        """The username that placed the order."""
        return self._json.get("username", "")

    @property
    def value(self) -> float:
        """The value of the order."""
        return parse_float(self._json.get("value"), 0.0)

    @property
    def value_effect(self) -> PriceEffect | None:
        """If pay or receive payment for notional market order."""
        value = self._json.get("value-effect")
        if value:
            try:
                return PriceEffect(value)
            except ValueError:
                return None
        return None

    @property
    def legs(self) -> list[OrderLeg]:
        """The legs of the order."""
        return self._legs

    @property
    def order_rule(self) -> OrderRule | None:
        """The order rule if present."""
        return self._order_rule

    def print_summary(self) -> None:
        """Print a simple text summary of the order."""
        print(f"\n{'=' * 80}")
        print(f"ORDER: {self.id}")
        print(f"{'=' * 80}")
        print(f"Account: {self.account_number}")
        print(f"Status: {self.status.value if self.status else 'Unknown'}")
        print(f"Order Type: {self.order_type.value if self.order_type else 'Unknown'}")
        print(
            f"Time in Force: {self.time_in_force.value if self.time_in_force else 'Unknown'}"
        )
        if self.price > 0:
            print(f"Price: ${self.price:,.2f}")
        if self.stop_trigger:
            print(f"Stop Trigger: {self.stop_trigger}")
        print(f"Size: {self.size}")

        if self.underlying_symbol:
            print(f"Underlying: {self.underlying_symbol}")

        if self.received_at:
            print(f"Received At: {self.received_at}")
        if self.live_at:
            print(f"Live At: {self.live_at}")

        print(f"\nLegs: {len(self.legs)}")
        for i, leg in enumerate(self.legs, 1):
            print(
                f"  {i}. {leg.symbol} - {leg.action.value if leg.action else 'Unknown'} {leg.quantity}"
            )

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the order."""
        console = Console()

        # Order Details Panel
        order_table = Table(show_header=False, box=None)
        order_table.add_column("Field", style="cyan", width=25)
        order_table.add_column("Value", style="white")

        order_table.add_row("Order ID", self.id)
        order_table.add_row("Account", self.account_number)
        order_table.add_row("Status", self.status.value if self.status else "Unknown")
        order_table.add_row(
            "Order Type", self.order_type.value if self.order_type else "Unknown"
        )
        order_table.add_row(
            "Time in Force",
            self.time_in_force.value if self.time_in_force else "Unknown",
        )

        if self.price > 0:
            order_table.add_row("Price", f"${self.price:,.2f}")
        if self.stop_trigger:
            order_table.add_row("Stop Trigger", self.stop_trigger)
        if self.value > 0:
            order_table.add_row("Value", f"${self.value:,.2f}")

        order_table.add_row("Size", str(self.size))
        order_table.add_row("Cancellable", "Yes" if self.cancellable else "No")
        order_table.add_row("Editable", "Yes" if self.editable else "No")

        if self.underlying_symbol:
            order_table.add_row("Underlying", self.underlying_symbol)

        console.print(
            Panel(order_table, title="[bold]Order Details[/bold]", border_style="green")
        )

        # Legs Table
        if self.legs:
            legs_table = Table(title="Order Legs")
            legs_table.add_column("Symbol", style="cyan")
            legs_table.add_column("Action", style="yellow")
            legs_table.add_column("Instrument Type", style="magenta")
            legs_table.add_column("Quantity", style="white")
            legs_table.add_column("Remaining", style="white")
            legs_table.add_column("Fills", style="green")

            for leg in self.legs:
                legs_table.add_row(
                    leg.symbol,
                    leg.action.value if leg.action else "Unknown",
                    leg.instrument_type.value if leg.instrument_type else "Unknown",
                    str(leg.quantity),
                    str(leg.remaining_quantity),
                    str(len(leg.fills)),
                )

            console.print(legs_table)

        # Timestamps
        if any([self.received_at, self.live_at, self.terminal_at, self.cancelled_at]):
            time_table = Table(title="Timestamps", show_header=False, box=None)
            time_table.add_column("Event", style="cyan", width=20)
            time_table.add_column("Time", style="white")

            if self.received_at:
                time_table.add_row("Received", str(self.received_at))
            if self.live_at:
                time_table.add_row("Live", str(self.live_at))
            if self.terminal_at:
                time_table.add_row("Terminal", str(self.terminal_at))
            if self.cancelled_at:
                time_table.add_row("Cancelled", str(self.cancelled_at))

            console.print(time_table)
