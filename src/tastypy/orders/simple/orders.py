"""Simple orders endpoint operations."""

from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session

from ..common import Order, OrderBuilder, PlacedOrderResponse


class Orders:
    """Manages simple orders for an account."""

    def __init__(self, session: Session, account_number: str) -> None:
        """
        Initialize Orders manager.

        Args:
            session: Active session instance
            account_number: Account number to manage orders for
        """
        self._session = session
        self._account_number = account_number
        self._url_base = f"/accounts/{account_number}/orders"
        self._orders: list[Order] = []
        self._raw_json: dict[str, Any] = {}

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the last API call."""
        return self._raw_json

    @property
    def orders(self) -> list[Order]:
        """List of orders."""
        return self._orders

    def get_live_orders(self) -> None:
        """
        Get all orders from the current trading day (deprecated endpoint).

        Note: This endpoint is deprecated. Use customer-level orders instead.
        """
        url = f"{self._url_base}/live"
        response = self._session.client.get(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})

        if isinstance(data, dict):
            items = data.get("items", [])
        else:
            items = data if isinstance(data, list) else []

        self._orders = [Order(order) for order in items]

    def get_order(self, order_id: str) -> Order:
        """
        Get a specific order by ID.

        Args:
            order_id: The order ID to retrieve

        Returns:
            Order instance
        """
        url = f"{self._url_base}/{order_id}"
        response = self._session.client.get(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return Order(data)

    def place_order(
        self, order_data: dict[str, Any] | OrderBuilder
    ) -> PlacedOrderResponse:
        """
        Place a new order.

        Args:
            order_data: Order parameters as dictionary or OrderBuilder instance

        Returns:
            PlacedOrderResponse instance

        Example:
            Using OrderBuilder:
            >>> from tastypy.orders import OrderBuilder, OrderLegBuilder
            >>> leg = OrderLegBuilder().equity("AAPL").quantity(1).buy_to_open()
            >>> order = OrderBuilder().limit(150.00).day().debit().add_leg(leg)
            >>> response = orders.place_order(order)
        """
        # Convert OrderBuilder to dict if needed
        if isinstance(order_data, OrderBuilder):
            order_data = order_data.build()

        url = self._url_base
        response = self._session.client.post(url, json=order_data)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return PlacedOrderResponse(data)

    def place_order_dry_run(
        self, order_data: dict[str, Any] | OrderBuilder
    ) -> PlacedOrderResponse:
        """
        Perform a dry-run of an order without placing it.

        Args:
            order_data: Order parameters as dictionary or OrderBuilder instance

        Returns:
            PlacedOrderResponse instance with validation results

        Example:
            Using OrderBuilder:
            >>> from tastypy.orders import OrderBuilder, OrderLegBuilder
            >>> leg = OrderLegBuilder().equity("AAPL").quantity(1).buy_to_open()
            >>> order = OrderBuilder().limit(150.00).day().debit().add_leg(leg)
            >>> response = orders.place_order_dry_run(order)
        """
        # Convert OrderBuilder to dict if needed
        if isinstance(order_data, OrderBuilder):
            order_data = order_data.build()

        url = f"{self._url_base}/dry-run"
        response = self._session.client.post(url, json=order_data)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return PlacedOrderResponse(data)

    def replace_order(
        self, order_id: str, order_data: dict[str, Any] | OrderBuilder
    ) -> Order:
        """
        Replace a live order with a new one (PUT).

        Args:
            order_id: The order ID to replace
            order_data: New order parameters as dictionary or OrderBuilder instance

        Returns:
            Order instance
        """
        # Convert OrderBuilder to dict if needed
        if isinstance(order_data, OrderBuilder):
            order_data = order_data.build()

        url = f"{self._url_base}/{order_id}"
        response = self._session.client.put(url, json=order_data)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return Order(data)

    def edit_order(
        self, order_id: str, order_data: dict[str, Any] | OrderBuilder
    ) -> Order:
        """
        Edit price and execution properties of a live order (PATCH).

        Args:
            order_id: The order ID to edit
            order_data: Order parameters to update as dictionary or OrderBuilder instance

        Returns:
            Order instance
        """
        # Convert OrderBuilder to dict if needed
        if isinstance(order_data, OrderBuilder):
            order_data = order_data.build()

        url = f"{self._url_base}/{order_id}"
        response = self._session.client.patch(url, json=order_data)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return Order(data)

    def cancel_order(self, order_id: str) -> Order:
        """
        Cancel an order.

        Args:
            order_id: The order ID to cancel

        Returns:
            Order instance
        """
        url = f"{self._url_base}/{order_id}"
        response = self._session.client.delete(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return Order(data)

    def dry_run_edit(
        self, order_id: str, order_data: dict[str, Any]
    ) -> PlacedOrderResponse:
        """
        Dry-run an order edit without actually modifying it.

        Args:
            order_id: The order ID to test editing
            order_data: Order parameters to test

        Returns:
            PlacedOrderResponse instance with validation results
        """
        url = f"{self._url_base}/{order_id}/dry-run"
        response = self._session.client.post(url, json=order_data)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return PlacedOrderResponse(data)

    def reconfirm_order(self, order_id: str) -> Order:
        """
        Reconfirm an order.

        Args:
            order_id: The order ID to reconfirm

        Returns:
            Order instance
        """
        url = f"{self._url_base}/{order_id}/reconfirm"
        response = self._session.client.post(url)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return Order(data)

    def print_summary(self) -> None:
        """Print a simple text summary of orders."""
        print(f"\n{'=' * 80}")
        print(f"ORDERS FOR ACCOUNT {self._account_number}")
        print(f"{'=' * 80}")
        print(f"Total Orders: {len(self.orders)}")

        if not self.orders:
            print("No orders found.")
            print(f"{'=' * 80}\n")
            return

        for i, order in enumerate(self.orders, 1):
            print(f"\n{i}. Order {order.id}")
            print(f"   Status: {order.status.value if order.status else 'Unknown'}")
            print(
                f"   Type: {order.order_type.value if order.order_type else 'Unknown'}"
            )
            if order.price > 0:
                print(f"   Price: ${order.price:,.2f}")
            symbols = ", ".join([leg.symbol for leg in order.legs])
            print(f"   Symbols: {symbols}")

        print(f"\n{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of orders."""
        console = Console()

        if not self.orders:
            console.print("[yellow]No orders found.[/yellow]")
            return

        orders_table = Table(title=f"Orders for Account {self._account_number}")
        orders_table.add_column("Order ID", style="cyan", width=12)
        orders_table.add_column("Status", style="yellow")
        orders_table.add_column("Type", style="magenta")
        orders_table.add_column("Symbol(s)", style="white")
        orders_table.add_column("Price", style="green")
        orders_table.add_column("Size", style="white")

        for order in self.orders:
            symbols = ", ".join([leg.symbol for leg in order.legs])
            price_str = f"${order.price:,.2f}" if order.price > 0 else "-"

            orders_table.add_row(
                order.id,
                order.status.value if order.status else "Unknown",
                order.order_type.value if order.order_type else "Unknown",
                symbols,
                price_str,
                order.size,
            )

        console.print(orders_table)
