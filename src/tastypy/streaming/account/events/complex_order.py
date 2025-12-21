"""Representation of complex order events in account streaming."""

from .base import AccountEvent
from typing import Any
from ....orders.common.complex_order import ComplexOrder, ComplexOrderType
from .event_type import AccountEventType


class ComplexOrderEvent(AccountEvent):
    """
    Event for complex order status changes.

    Wraps the existing ComplexOrder model from the orders module.
    """

    def __init__(self, message: dict[str, Any]) -> None:
        """Initialize ComplexOrderEvent with complex order data."""
        super().__init__(AccountEventType.COMPLEX_ORDER, message)
        self._complex_order = ComplexOrder(self._data)

    @property
    def complex_order(self) -> ComplexOrder:
        """Get the full ComplexOrder object with all properties and methods."""
        return self._complex_order

    # Convenience properties for quick access to common fields
    @property
    def complex_order_id(self) -> str:
        """The unique complex order ID."""
        return self._complex_order.id

    @property
    def account_number(self) -> str:
        """The account number for this complex order."""
        return self._complex_order.account_number

    @property
    def type(self) -> ComplexOrderType | None:
        """The type of complex order (OCO, OTO, OTOCO, PAIRS, BLAST)."""
        return self._complex_order.type

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ComplexOrderEvent(id={self.complex_order_id}, "
            f"account={self.account_number})"
        )
