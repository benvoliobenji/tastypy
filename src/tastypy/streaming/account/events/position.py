"""Representation of position events in account streaming."""

from ....account.current_position import CurrentPosition
from .base import AccountEvent
from typing import Any
from .event_type import AccountEventType


class PositionEvent(AccountEvent):
    """
    Event for position changes.

    Wraps the existing CurrentPosition model from the account module.
    """

    def __init__(self, message: dict[str, Any]) -> None:
        """Initialize PositionEvent with position data."""
        super().__init__(AccountEventType.POSITION, message)
        self._position = CurrentPosition(self._data)

    @property
    def position(self) -> CurrentPosition:
        """Get the full CurrentPosition object with all properties and methods."""
        return self._position

    # Convenience properties for quick access to common fields
    @property
    def account_number(self) -> str:
        """The account number."""
        return self._position.account_number

    @property
    def symbol(self) -> str:
        """The symbol."""
        return self._position.symbol

    @property
    def underlying_symbol(self) -> str:
        """The underlying symbol."""
        return self._position.underlying_symbol

    @property
    def quantity(self) -> int:
        """Position quantity (signed: positive = long, negative = short)."""
        return self._position.quantity

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"PositionEvent(account={self.account_number}, "
            f"symbol={self.symbol}, quantity={self.quantity})"
        )
