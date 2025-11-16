"""Complex order data model."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.utils.decode_json import parse_float

from .enums import ComplexOrderType, RuleComparator
from .order import Order


class RelatedOrder:
    """Represents a related order in a complex order."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize RelatedOrder from JSON data."""
        self._json = json_data

    @property
    def id(self) -> str:
        """The order ID."""
        return self._json.get("id", "")

    @property
    def complex_order_id(self) -> str:
        """The complex order ID."""
        return self._json.get("complex-order-id", "")

    @property
    def complex_order_tag(self) -> str:
        """The complex order tag."""
        return self._json.get("complex-order-tag", "")

    @property
    def replaces_order_id(self) -> str:
        """The order ID this order replaces."""
        return self._json.get("replaces-order-id", "")

    @property
    def replacing_order_id(self) -> str:
        """The order ID that replaces this order."""
        return self._json.get("replacing-order-id", "")

    @property
    def status(self) -> str:
        """The status of the related order."""
        return self._json.get("status", "")


class ComplexOrder:
    """Represents a complex order (OCO, OTO, OTOCO, PAIRS, BLAST)."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize ComplexOrder from JSON data."""
        self._json = json_data
        self._related_orders: list[RelatedOrder] = []
        self._orders: list[Order] = []
        self._trigger_order: Order | None = None

        # Parse related orders if present
        related_data = self._json.get("related-orders", [])
        if related_data:
            self._related_orders = [RelatedOrder(ro) for ro in related_data]

        # Parse orders if present
        orders_data = self._json.get("orders", [])
        if orders_data:
            self._orders = [Order(order) for order in orders_data]

        # Parse trigger order if present
        trigger_data = self._json.get("trigger-order")
        if trigger_data:
            self._trigger_order = Order(trigger_data)

    @property
    def id(self) -> str:
        """The complex order ID."""
        return self._json.get("id", "")

    @property
    def account_number(self) -> str:
        """The account number."""
        return self._json.get("account-number", "")

    @property
    def ratio_price_comparator(self) -> RuleComparator | None:
        """How to compare against the ratio price."""
        value = self._json.get("ratio-price-comparator")
        if value:
            try:
                return RuleComparator(value)
            except ValueError:
                return None
        return None

    @property
    def ratio_price_is_threshold_based_on_notional(self) -> bool:
        """If comparison is in notional value instead of price."""
        return bool(self._json.get("ratio-price-is-threshold-based-on-notional", False))

    @property
    def ratio_price_threshold(self) -> float:
        """Ratio price for a PAIRS trade."""
        return parse_float(self._json.get("ratio-price-threshold"), 0.0)

    @property
    def terminal_at(self) -> str:
        """When the complex order reached terminal status."""
        return self._json.get("terminal-at", "")

    @property
    def type(self) -> ComplexOrderType | None:
        """The type of complex order strategy."""
        value = self._json.get("type")
        if value:
            try:
                return ComplexOrderType(value)
            except ValueError:
                return None
        return None

    @property
    def related_orders(self) -> list[RelatedOrder]:
        """Non-current orders (replaced, unfilled, terminal)."""
        return self._related_orders

    @property
    def orders(self) -> list[Order]:
        """Orders with complex-order-tag '<type>::order'."""
        return self._orders

    @property
    def trigger_order(self) -> Order | None:
        """Order with complex-order-tag '<type>::trigger-order' for OTO-based orders."""
        return self._trigger_order

    def print_summary(self) -> None:
        """Print a simple text summary of the complex order."""
        print(f"\n{'=' * 80}")
        print(f"COMPLEX ORDER: {self.id}")
        print(f"{'=' * 80}")
        print(f"Account: {self.account_number}")
        print(f"Type: {self.type.value if self.type else 'Unknown'}")

        if self.ratio_price_threshold > 0:
            comparator = (
                self.ratio_price_comparator.value
                if self.ratio_price_comparator
                else "?"
            )
            print(f"Ratio Price: {comparator} {self.ratio_price_threshold}")

        if self.trigger_order:
            print(f"\nTrigger Order: {self.trigger_order.id}")
            print(
                f"  Status: {self.trigger_order.status.value if self.trigger_order.status else 'Unknown'}"
            )

        print(f"\nOrders: {len(self.orders)}")
        for i, order in enumerate(self.orders, 1):
            print(
                f"  {i}. {order.id} - {order.status.value if order.status else 'Unknown'}"
            )

        if self.related_orders:
            print(f"\nRelated Orders: {len(self.related_orders)}")
            for i, ro in enumerate(self.related_orders, 1):
                print(f"  {i}. {ro.id} - {ro.status}")

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the complex order."""
        console = Console()

        # Complex Order Details Panel
        details_table = Table(show_header=False, box=None)
        details_table.add_column("Field", style="cyan", width=30)
        details_table.add_column("Value", style="white")

        details_table.add_row("Complex Order ID", self.id)
        details_table.add_row("Account", self.account_number)
        details_table.add_row("Type", self.type.value if self.type else "Unknown")

        if self.ratio_price_threshold > 0:
            comparator = (
                self.ratio_price_comparator.value
                if self.ratio_price_comparator
                else "?"
            )
            details_table.add_row(
                "Ratio Price", f"{comparator} {self.ratio_price_threshold}"
            )
            details_table.add_row(
                "Based on Notional",
                "Yes" if self.ratio_price_is_threshold_based_on_notional else "No",
            )

        console.print(
            Panel(
                details_table,
                title="[bold]Complex Order Details[/bold]",
                border_style="blue",
            )
        )

        # Trigger Order
        if self.trigger_order:
            console.print("\n[bold yellow]Trigger Order:[/bold yellow]")
            self.trigger_order.pretty_print()

        # Orders
        if self.orders:
            orders_table = Table(title="Component Orders")
            orders_table.add_column("Order ID", style="cyan")
            orders_table.add_column("Status", style="yellow")
            orders_table.add_column("Type", style="magenta")
            orders_table.add_column("Symbol(s)", style="white")
            orders_table.add_column("Price", style="green")

            for order in self.orders:
                symbols = ", ".join([leg.symbol for leg in order.legs])
                price_str = f"${order.price:,.2f}" if order.price > 0 else "-"

                orders_table.add_row(
                    order.id,
                    order.status.value if order.status else "Unknown",
                    order.order_type.value if order.order_type else "Unknown",
                    symbols,
                    price_str,
                )

            console.print(orders_table)

        # Related Orders
        if self.related_orders:
            related_table = Table(title="Related Orders")
            related_table.add_column("Order ID", style="cyan")
            related_table.add_column("Status", style="yellow")
            related_table.add_column("Tag", style="magenta")

            for ro in self.related_orders:
                related_table.add_row(ro.id, ro.status, ro.complex_order_tag)

            console.print(related_table)
