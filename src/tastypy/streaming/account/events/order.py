"""Representation of order events in account streaming."""

from .base import AccountEvent
from typing import Any
from ....orders.common.order import Order
from .event_type import AccountEventType


class OrderEvent(AccountEvent):
    """
    Event for order status changes.

    Wraps the existing Order model from the orders module.
    """

    def __init__(self, message: dict[str, Any]) -> None:
        """Initialize OrderEvent with order data."""
        super().__init__(AccountEventType.ORDER, message)
        self._order = Order(self._data)

    @property
    def order(self) -> Order:
        """Get the full Order object with all properties and methods."""
        return self._order

    # Convenience properties for quick access to common fields
    @property
    def order_id(self) -> str:
        """The unique order ID."""
        return self._order.id

    @property
    def account_number(self) -> str:
        """The account number for this order."""
        return self._order.account_number

    @property
    def status(self) -> str:
        """Order status (Routed, Live, Filled, Cancelled, etc.)."""
        status_enum = self._order.status
        return status_enum.value if status_enum else ""

    @property
    def underlying_symbol(self) -> str:
        """The underlying symbol."""
        return self._order.underlying_symbol

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"OrderEvent(id={self.order_id}, account={self.account_number}, "
            f"status={self.status}, symbol={self.underlying_symbol})"
        )
