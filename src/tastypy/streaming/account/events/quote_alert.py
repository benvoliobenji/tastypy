"""Representation of quote alert events in account streaming."""

from .base import AccountEvent
from typing import Any
from ....quote_alerts.quote_alert import QuoteAlert
import datetime
from .event_type import AccountEventType


class QuoteAlertEvent(AccountEvent):
    """
    Event for quote alert triggers.

    Wraps the existing QuoteAlert model from the quote_alerts module.
    """

    def __init__(self, message: dict[str, Any]) -> None:
        """Initialize QuoteAlertEvent with alert data."""
        super().__init__(AccountEventType.QUOTE_ALERT, message)
        self._alert = QuoteAlert(self._data)

    @property
    def alert(self) -> QuoteAlert:
        """Get the full QuoteAlert object with all properties and methods."""
        return self._alert

    # Convenience properties for quick access to common fields
    @property
    def alert_external_id(self) -> str:
        """External ID of the triggered alert."""
        return self._alert.alert_external_id

    @property
    def symbol(self) -> str:
        """The symbol that triggered the alert."""
        return self._alert.symbol

    @property
    def triggered_at(self) -> datetime.datetime | None:
        """When the alert was triggered."""
        return self._alert.triggered_at

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"QuoteAlertEvent(symbol={self.symbol}, alert_id={self.alert_external_id})"
        )
