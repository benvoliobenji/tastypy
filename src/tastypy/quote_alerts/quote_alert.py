"""Individual quote alert data model."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.quote_alerts.enums import FieldType, OperatorType
from tastypy.utils.decode_json import parse_datetime, parse_float


class QuoteAlert:
    """Represents an individual quote alert."""

    def __init__(self, alert_json: dict[str, Any]) -> None:
        """
        Initialize a quote alert from JSON data.

        Args:
            alert_json: Dictionary containing alert data from API.
        """
        self._alert_json = alert_json

    @property
    def alert_external_id(self) -> str:
        """External ID of the alert."""
        return self._alert_json.get("alert-external-id", "")

    @property
    def user_external_id(self) -> str:
        """External ID of the user who created the alert."""
        return self._alert_json.get("user-external-id", "")

    @property
    def symbol(self) -> str:
        """Symbol being monitored."""
        return self._alert_json.get("symbol", "")

    @property
    def dx_symbol(self) -> str:
        """DXFeed symbol representation."""
        return self._alert_json.get("dx-symbol", "")

    @property
    def instrument_type(self) -> str:
        """Type of instrument being monitored."""
        return self._alert_json.get("instrument-type", "")

    @property
    def field(self) -> str:
        """Field being monitored (Last, Bid, Ask, IV)."""
        return self._alert_json.get("field", "")

    @property
    def field_type(self) -> FieldType | None:
        """Field type enum."""
        field = self.field
        if field:
            try:
                return FieldType(field)
            except ValueError:
                return None
        return None

    @property
    def operator(self) -> str:
        """Comparison operator (> or <)."""
        return self._alert_json.get("operator", "")

    @property
    def operator_type(self) -> OperatorType | None:
        """Operator type enum."""
        operator = self.operator
        if operator:
            try:
                return OperatorType(operator)
            except ValueError:
                return None
        return None

    @property
    def threshold(self) -> str:
        """Threshold value as string."""
        return self._alert_json.get("threshold", "")

    @property
    def threshold_numeric(self) -> float:
        """Threshold value as numeric."""
        return parse_float(self._alert_json.get("threshold-numeric"), 0.0)

    @property
    def provider(self) -> str:
        """Provider of the alert data."""
        return self._alert_json.get("provider", "")

    @property
    def created_at(self) -> datetime.datetime | None:
        """When the alert was created."""
        return parse_datetime(self._alert_json.get("created-at"))

    @property
    def expires_at(self) -> str:
        """When the alert expires (as string)."""
        return self._alert_json.get("expires-at", "")

    @property
    def expired_at(self) -> datetime.datetime | None:
        """When the alert actually expired."""
        return parse_datetime(self._alert_json.get("expired-at"))

    @property
    def triggered_at(self) -> datetime.datetime | None:
        """When the alert was triggered."""
        return parse_datetime(self._alert_json.get("triggered-at"))

    @property
    def completed_at(self) -> datetime.datetime | None:
        """When the alert was completed."""
        return parse_datetime(self._alert_json.get("completed-at"))

    @property
    def dismissed_at(self) -> datetime.datetime | None:
        """When the alert was dismissed."""
        return parse_datetime(self._alert_json.get("dismissed-at"))

    @property
    def is_active(self) -> bool:
        """Whether the alert is still active (not triggered, expired, or dismissed)."""
        return not any([self.triggered_at, self.expired_at, self.dismissed_at])

    def print_summary(self) -> None:
        """Print a plain text summary of the alert."""
        print(f"  Alert ID: {self.alert_external_id}")
        print(f"    Symbol: {self.symbol}")
        print(f"    Condition: {self.field} {self.operator} {self.threshold}")
        print(f"    Instrument Type: {self.instrument_type}")
        print(f"    Provider: {self.provider}")
        print(f"    Created: {self.created_at}")
        print(f"    Expires: {self.expires_at}")
        if self.triggered_at:
            print(f"    Triggered: {self.triggered_at}")
        if self.expired_at:
            print(f"    Expired: {self.expired_at}")
        if self.dismissed_at:
            print(f"    Dismissed: {self.dismissed_at}")
        if self.completed_at:
            print(f"    Completed: {self.completed_at}")
        print(f"    Status: {'Active' if self.is_active else 'Inactive'}")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the alert."""
        console = Console()

        # Create alert details table
        table = Table(show_header=False, box=None)
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Alert ID", self.alert_external_id)
        table.add_row("Symbol", self.symbol)
        table.add_row("DX Symbol", self.dx_symbol)
        table.add_row("Instrument Type", self.instrument_type)
        table.add_row("Condition", f"{self.field} {self.operator} {self.threshold}")
        table.add_row("Threshold (numeric)", f"{self.threshold_numeric:.4f}")
        table.add_row("Provider", self.provider)
        table.add_row("Created", str(self.created_at) if self.created_at else "")
        table.add_row("Expires", self.expires_at)

        if self.triggered_at:
            table.add_row("Triggered", str(self.triggered_at))
        if self.expired_at:
            table.add_row("Expired", str(self.expired_at))
        if self.dismissed_at:
            table.add_row("Dismissed", str(self.dismissed_at))
        if self.completed_at:
            table.add_row("Completed", str(self.completed_at))

        status_style = "green" if self.is_active else "red"
        status_text = "Active" if self.is_active else "Inactive"
        table.add_row("Status", f"[{status_style}]{status_text}[/{status_style}]")

        title = f"[bold blue]Quote Alert - {self.symbol}[/bold blue]"
        border_style = "green" if self.is_active else "red"

        console.print(Panel(table, title=title, border_style=border_style))
