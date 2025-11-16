"""Complex orders endpoint operations."""

from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session

from ..common import ComplexOrder, ComplexOrderBuilder, PlacedOrderResponse


class ComplexOrders:
    """Manages complex orders for an account."""

    def __init__(self, session: Session, account_number: str) -> None:
        """
        Initialize ComplexOrders manager.

        Args:
            session: Active session instance
            account_number: Account number to manage complex orders for
        """
        self._session = session
        self._account_number = account_number
        self._url_base = f"/accounts/{account_number}/complex-orders"
        self._complex_orders: list[ComplexOrder] = []
        self._raw_json: dict[str, Any] = {}

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the last API call."""
        return self._raw_json

    @property
    def complex_orders(self) -> list[ComplexOrder]:
        """List of complex orders."""
        return self._complex_orders

    def get_complex_orders(self, page_offset: int = 0, per_page: int = 10) -> None:
        """
        Get all complex orders for the account with pagination.

        Args:
            page_offset: Page offset for pagination
            per_page: Number of results per page (1-200)
        """
        params: dict[str, Any] = {
            "page-offset": page_offset,
            "per-page": min(max(per_page, 1), 200),  # Clamp between 1-200
        }

        response = self._session.client.get(self._url_base, params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})

        if isinstance(data, dict):
            items = data.get("items", [])
        else:
            items = data if isinstance(data, list) else []

        self._complex_orders = [ComplexOrder(order) for order in items]

    def get_live_complex_orders(self) -> None:
        """Get complex orders where a component was placed today."""
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

        self._complex_orders = [ComplexOrder(order) for order in items]

    def get_complex_order(self, complex_order_id: str) -> ComplexOrder:
        """
        Get a specific complex order by ID.

        Args:
            complex_order_id: The complex order ID to retrieve

        Returns:
            ComplexOrder instance
        """
        url = f"{self._url_base}/{complex_order_id}"
        response = self._session.client.get(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return ComplexOrder(data)

    def place_complex_order(
        self, complex_order_data: dict[str, Any] | ComplexOrderBuilder
    ) -> PlacedOrderResponse:
        """
        Place a new complex order.

        Args:
            complex_order_data: Complex order parameters as dictionary or ComplexOrderBuilder

        Returns:
            PlacedOrderResponse instance

        Example:
            Using ComplexOrderBuilder:
            >>> from tastypy.orders import ComplexOrderBuilder, OrderBuilder, OrderLegBuilder
            >>> leg = OrderLegBuilder().equity("AAPL").quantity(1).buy()
            >>> order = OrderBuilder().limit(150.00).day().add_leg(leg)
            >>> complex = ComplexOrderBuilder.oco().add_order(order).add_order(order)
            >>> response = complex_orders.place_complex_order(complex)
        """
        # Convert ComplexOrderBuilder to dict if needed
        if isinstance(complex_order_data, ComplexOrderBuilder):
            complex_order_data = complex_order_data.build()

        response = self._session.client.post(self._url_base, json=complex_order_data)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return PlacedOrderResponse(data)

    def place_complex_order_dry_run(
        self, complex_order_data: dict[str, Any] | ComplexOrderBuilder
    ) -> PlacedOrderResponse:
        """
        Perform a dry-run of a complex order without placing it.

        Args:
            complex_order_data: Complex order parameters as dictionary or ComplexOrderBuilder

        Returns:
            PlacedOrderResponse instance with validation results

        Example:
            Using ComplexOrderBuilder:
            >>> from tastypy.orders import ComplexOrderBuilder, OrderBuilder, OrderLegBuilder
            >>> leg = OrderLegBuilder().equity("AAPL").quantity(1).buy()
            >>> order = OrderBuilder().limit(150.00).day().add_leg(leg)
            >>> complex = ComplexOrderBuilder.oco().add_order(order).add_order(order)
            >>> response = complex_orders.place_complex_order_dry_run(complex)
        """
        # Convert ComplexOrderBuilder to dict if needed
        if isinstance(complex_order_data, ComplexOrderBuilder):
            complex_order_data = complex_order_data.build()

        url = f"{self._url_base}/dry-run"
        response = self._session.client.post(url, json=complex_order_data)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return PlacedOrderResponse(data)

    def edit_complex_order(
        self, complex_order_id: str, edit_data: dict[str, Any]
    ) -> PlacedOrderResponse:
        """
        Edit threshold-price of a PAIRS trade.

        Args:
            complex_order_id: The complex order ID to edit
            edit_data: Edit parameters (ratio-price-comparator, ratio-price-threshold)

        Returns:
            PlacedOrderResponse instance
        """
        url = f"{self._url_base}/{complex_order_id}"
        response = self._session.client.patch(url, json=edit_data)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return PlacedOrderResponse(data)

    def cancel_complex_order(self, complex_order_id: str) -> ComplexOrder:
        """
        Cancel all non-terminal components of a complex order.

        Args:
            complex_order_id: The complex order ID to cancel

        Returns:
            ComplexOrder instance
        """
        url = f"{self._url_base}/{complex_order_id}"
        response = self._session.client.delete(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return ComplexOrder(data)

    def dry_run_complex_order_edit(
        self, complex_order_id: str, edit_data: dict[str, Any]
    ) -> PlacedOrderResponse:
        """
        Dry-run editing a complex order without actually modifying it.

        Args:
            complex_order_id: The complex order ID to test editing
            edit_data: Edit parameters to test

        Returns:
            PlacedOrderResponse instance with validation results
        """
        url = f"{self._url_base}/{complex_order_id}/dry-run"
        response = self._session.client.post(url, json=edit_data)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})
        return PlacedOrderResponse(data)

    def print_summary(self) -> None:
        """Print a simple text summary of complex orders."""
        print(f"\n{'=' * 80}")
        print(f"COMPLEX ORDERS FOR ACCOUNT {self._account_number}")
        print(f"{'=' * 80}")
        print(f"Total Complex Orders: {len(self.complex_orders)}")

        if not self.complex_orders:
            print("No complex orders found.")
            print(f"{'=' * 80}\n")
            return

        for i, co in enumerate(self.complex_orders, 1):
            print(f"\n{i}. Complex Order {co.id}")
            print(f"   Type: {co.type.value if co.type else 'Unknown'}")
            print(f"   Component Orders: {len(co.orders)}")
            if co.trigger_order:
                print("   Has Trigger Order: Yes")

        print(f"\n{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of complex orders."""
        console = Console()

        if not self.complex_orders:
            console.print("[yellow]No complex orders found.[/yellow]")
            return

        co_table = Table(title=f"Complex Orders for Account {self._account_number}")
        co_table.add_column("Complex Order ID", style="cyan", width=12)
        co_table.add_column("Type", style="magenta")
        co_table.add_column("Component Orders", style="white")
        co_table.add_column("Trigger Order", style="yellow")
        co_table.add_column("Ratio Price", style="green")

        for co in self.complex_orders:
            trigger = "Yes" if co.trigger_order else "No"
            ratio = ""
            if co.ratio_price_threshold > 0:
                comp = (
                    co.ratio_price_comparator.value
                    if co.ratio_price_comparator
                    else "?"
                )
                ratio = f"{comp} {co.ratio_price_threshold}"

            co_table.add_row(
                co.id,
                co.type.value if co.type else "Unknown",
                str(len(co.orders)),
                trigger,
                ratio,
            )

        console.print(co_table)
