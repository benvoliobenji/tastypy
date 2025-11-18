"""Quote alerts management for TastyTrade API."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.quote_alerts.enums import FieldType, OperatorType
from tastypy.quote_alerts.quote_alert import QuoteAlert
from tastypy.session import Session


class QuoteAlerts:
    """
    A class for managing quote alerts.

    Quote alerts notify users when a symbol's price or implied volatility
    crosses a specified threshold.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the quote alerts manager.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._url_endpoint = "/quote-alerts"
        self._request_json_data: dict[str, Any] = {}
        self._alerts: list[QuoteAlert] = []

    def sync(self) -> None:
        """
        Fetch all quote alerts for the current user.

        Raises:
            translate_error_code: If the API request fails.
        """
        response = self._session.client.get(self._url_endpoint)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse alerts - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._alerts = [QuoteAlert(item) for item in items_data]

    def create(
        self,
        symbol: str,
        field: FieldType,
        operator: OperatorType,
        threshold: str,
        expires_at: str | None = None,
        dx_symbol: str | None = None,
        instrument_type: str | None = None,
        threshold_numeric: str | None = None,
    ) -> QuoteAlert:
        """
        Create a new quote alert.

        Args:
            symbol: Symbol to monitor (required).
            field: Field to monitor (Last, Bid, Ask, IV) (required).
            operator: Comparison operator (> or <) (required).
            threshold: Threshold value as string (required).
            expires_at: Optional expiration date/time for the alert.
            dx_symbol: Optional DXFeed symbol representation.
            instrument_type: Optional instrument type.
            threshold_numeric: Optional numeric threshold value.

        Returns:
            QuoteAlert: The newly created alert.

        Raises:
            translate_error_code: If the API request fails.
        """
        payload: dict[str, str] = {
            "symbol": symbol,
            "field": field.value,
            "operator": operator.value,
            "threshold": threshold,
        }

        if expires_at:
            payload["expires-at"] = expires_at
        if dx_symbol:
            payload["dx-symbol"] = dx_symbol
        if instrument_type:
            payload["instrument-type"] = instrument_type
        if threshold_numeric:
            payload["threshold-numeric"] = threshold_numeric

        response = self._session.client.post(self._url_endpoint, json=payload)

        if response.status_code != 201:
            raise translate_error_code(response.status_code, response.text)

        # Parse the created alert
        response_data = response.json()
        alert_data = response_data.get("data", {})

        return QuoteAlert(alert_data)

    def delete(self, alert_external_id: int | str) -> None:
        """
        Delete (cancel) a quote alert.

        Args:
            alert_external_id: The external ID of the alert to delete.

        Raises:
            translate_error_code: If the API request fails.
        """
        url = f"{self._url_endpoint}/{alert_external_id}"
        response = self._session.client.delete(url)

        if response.status_code != 204:
            raise translate_error_code(response.status_code, response.text)

    @property
    def alerts(self) -> list[QuoteAlert]:
        """List of quote alerts returned from the API."""
        return self._alerts

    @property
    def active_alerts(self) -> list[QuoteAlert]:
        """List of active (not triggered/expired/dismissed) alerts."""
        return [alert for alert in self._alerts if alert.is_active]

    @property
    def inactive_alerts(self) -> list[QuoteAlert]:
        """List of inactive (triggered/expired/dismissed) alerts."""
        return [alert for alert in self._alerts if not alert.is_active]

    def print_summary(self) -> None:
        """Print a plain text summary of all quote alerts."""
        print(f"\n{'=' * 80}")
        print(
            f"QUOTE ALERTS SUMMARY (Total: {len(self._alerts)}, Active: {len(self.active_alerts)})"
        )
        print(f"{'=' * 80}")

        if not self._alerts:
            print("No quote alerts found.")
            print(f"{'=' * 80}\n")
            return

        # Active alerts
        if self.active_alerts:
            print(f"\nActive Alerts ({len(self.active_alerts)}):")
            print("-" * 80)
            for alert in self.active_alerts:
                alert.print_summary()
                print()

        # Inactive alerts
        if self.inactive_alerts:
            print(f"\nInactive Alerts ({len(self.inactive_alerts)}):")
            print("-" * 80)
            for alert in self.inactive_alerts:
                alert.print_summary()
                print()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all quote alerts."""
        console = Console()

        # Create summary table
        summary_table = Table(
            title=f"Quote Alerts Overview (Total: {len(self._alerts)}, Active: {len(self.active_alerts)})",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("ID", style="cyan", no_wrap=True)
        summary_table.add_column("Symbol", style="green", no_wrap=True)
        summary_table.add_column("Condition", style="yellow")
        summary_table.add_column("Created", style="white")
        summary_table.add_column("Expires", style="white")
        summary_table.add_column("Status", style="magenta")

        for alert in self._alerts:
            status = "Active" if alert.is_active else "Inactive"
            status_style = "green" if alert.is_active else "red"

            created_str = (
                alert.created_at.strftime("%Y-%m-%d %H:%M") if alert.created_at else ""
            )
            condition = f"{alert.field} {alert.operator} {alert.threshold}"

            summary_table.add_row(
                alert.alert_external_id,
                alert.symbol,
                condition,
                created_str,
                alert.expires_at,
                f"[{status_style}]{status}[/{status_style}]",
            )

        console.print(
            Panel(
                summary_table,
                title="[bold blue]Quote Alerts[/bold blue]",
                border_style="blue",
            )
        )

        # Print detailed info for active alerts
        if self.active_alerts:
            console.print(
                f"\n[bold green]Active Alerts ({len(self.active_alerts)}):[/bold green]"
            )
            for alert in self.active_alerts:
                alert.pretty_print()
