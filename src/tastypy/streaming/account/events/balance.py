"""Represents account balance update events in the streaming API."""

from .event_type import AccountEventType
from .base import AccountEvent
from typing import Any
from ....account.balance_snapshot import BalanceSnapshot


class BalanceEvent(AccountEvent):
    """
    Event for account balance updates (TradingStatus messages).

    Wraps the existing BalanceSnapshot model from the account module.
    """

    def __init__(self, message: dict[str, Any]) -> None:
        """Initialize BalanceEvent with balance snapshot data."""
        super().__init__(AccountEventType.BALANCE, message)
        self._balance = BalanceSnapshot(self._data)

    @property
    def balance(self) -> BalanceSnapshot:
        """Get the full BalanceSnapshot object with all properties and methods."""
        return self._balance

    # Convenience properties for quick access to common fields
    @property
    def account_number(self) -> str:
        """The account number."""
        return self._balance.account_number

    @property
    def cash_balance(self) -> float:
        """Cash balance."""
        return self._balance.cash_balance

    @property
    def net_liquidating_value(self) -> float:
        """Net liquidating value."""
        return self._balance.net_liquidating_value

    @property
    def buying_power(self) -> float:
        """Buying power."""
        return self._balance.derivative_buying_power

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"BalanceEvent(account={self.account_number}, "
            f"nlv={self.net_liquidating_value:.2f}, "
            f"buying_power={self.buying_power:.2f})"
        )
