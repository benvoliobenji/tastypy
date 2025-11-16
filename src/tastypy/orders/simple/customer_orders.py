"""Customer-level orders endpoint operations."""

import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session

from ..common import Order, OrderStatus, SortOrder


class CustomerOrders:
    """Manages orders for a customer across multiple accounts."""

    def __init__(self, session: Session, customer_id: str) -> None:
        """
        Initialize CustomerOrders manager.

        Args:
            session: Active session instance
            customer_id: Customer ID to query orders for
        """
        self._session = session
        self._customer_id = customer_id
        self._url_base = f"/customers/{customer_id}/orders"
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

    def get_orders(
        self,
        account_numbers: list[str],
        page_offset: int = 0,
        per_page: int = 10,
        end_date: datetime.date | None = None,
        futures_symbol: str | None = None,
        start_date: datetime.date | None = None,
        status: list[OrderStatus] | None = None,
        underlying_instrument_type: str | None = None,
        underlying_symbol: str | None = None,
        sort: SortOrder = SortOrder.DESC,
        end_at: datetime.datetime | None = None,
        start_at: datetime.datetime | None = None,
    ) -> None:
        """
        Get orders for the customer with filtering and pagination.

        Args:
            account_numbers: List of account numbers to query
            page_offset: Page offset for pagination
            per_page: Number of results per page (1-200)
            end_date: End date for filtering (date only)
            futures_symbol: Futures symbol to filter by
            start_date: Start date for filtering (date only)
            status: List of order statuses to filter by
            underlying_instrument_type: Underlying instrument type
            underlying_symbol: Underlying symbol to filter by
            sort: Sort order (Desc or Asc)
            end_at: End datetime for filtering (full date-time)
            start_at: Start datetime for filtering (full date-time)
        """
        params: dict[str, Any] = {
            "page-offset": page_offset,
            "per-page": min(max(per_page, 1), 200),  # Clamp between 1-200
            "sort": sort.value,
        }

        # Account numbers are required - add as array
        for acc_num in account_numbers:
            params.setdefault("account-numbers[]", []).append(acc_num)

        # Optional filters
        if end_date:
            params["end-date"] = end_date.isoformat()

        if futures_symbol:
            params["futures-symbol"] = futures_symbol

        if start_date:
            params["start-date"] = start_date.isoformat()

        if status:
            for stat in status:
                params.setdefault("status[]", []).append(stat.value)

        if underlying_instrument_type:
            params["underlying-instrument-type"] = underlying_instrument_type

        if underlying_symbol:
            params["underlying-symbol"] = underlying_symbol

        if end_at:
            params["end-at"] = end_at.isoformat()

        if start_at:
            params["start-at"] = start_at.isoformat()

        response = self._session.client.get(self._url_base, params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})

        if isinstance(data, dict):
            items = data.get("items", [])
        else:
            items = data if isinstance(data, list) else []

        self._orders = [Order(order) for order in items]

    def get_live_orders(self, account_numbers: list[str]) -> None:
        """
        Get live orders from the current trading day.

        Args:
            account_numbers: List of account numbers to query
        """
        params: dict[str, Any] = {}

        # Account numbers are required - add as array
        for acc_num in account_numbers:
            params.setdefault("account-numbers[]", []).append(acc_num)

        url = f"{self._url_base}/live"
        response = self._session.client.get(url, params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._raw_json = response.json()
        data = self._raw_json.get("data", {})

        if isinstance(data, dict):
            items = data.get("items", [])
        else:
            items = data if isinstance(data, list) else []

        self._orders = [Order(order) for order in items]

    def print_summary(self) -> None:
        """Print a simple text summary of orders."""
        print(f"\n{'=' * 80}")
        print(f"ORDERS FOR CUSTOMER {self._customer_id}")
        print(f"{'=' * 80}")
        print(f"Total Orders: {len(self.orders)}")

        if not self.orders:
            print("No orders found.")
            print(f"{'=' * 80}\n")
            return

        # Group by account
        by_account: dict[str, list[Order]] = {}
        for order in self.orders:
            acc = order.account_number
            if acc not in by_account:
                by_account[acc] = []
            by_account[acc].append(order)

        print("\nOrders by Account:")
        for acc, orders in by_account.items():
            print(f"  {acc}: {len(orders)} order(s)")

        print("\nOrder Details:")
        for i, order in enumerate(self.orders, 1):
            print(f"\n{i}. Order {order.id} (Account: {order.account_number})")
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

        orders_table = Table(title=f"Orders for Customer {self._customer_id}")
        orders_table.add_column("Order ID", style="cyan", width=12)
        orders_table.add_column("Account", style="blue", width=10)
        orders_table.add_column("Status", style="yellow")
        orders_table.add_column("Type", style="magenta")
        orders_table.add_column("Symbol(s)", style="white")
        orders_table.add_column("Price", style="green")

        for order in self.orders:
            symbols = ", ".join(
                [leg.symbol for leg in order.legs[:3]]
            )  # Limit to first 3
            if len(order.legs) > 3:
                symbols += "..."
            price_str = f"${order.price:,.2f}" if order.price > 0 else "-"

            orders_table.add_row(
                order.id,
                order.account_number,
                order.status.value if order.status else "Unknown",
                order.order_type.value if order.order_type else "Unknown",
                symbols,
                price_str,
            )

        console.print(orders_table)
