import datetime
import enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..errors import translate_error_code
from ..session import Session
from ..utils.decode_json import parse_datetime, parse_float


class TimeBack(str, enum.Enum):
    """Time period options for net liquidating value history requests."""

    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1m"
    THREE_MONTHS = "3m"
    SIX_MONTHS = "6m"
    ONE_YEAR = "1y"
    ALL = "all"

    def __str__(self) -> str:
        return self.value


class NetLiqHistoryItem:
    """Represents a single net liquidating value data point in the history."""

    def __init__(self, item_data: dict[str, Any]) -> None:
        """
        Initialize a net liq history item.

        Args:
            item_data: Dictionary containing the item data from the API.
        """
        self._data = item_data

    @property
    def open(self) -> float:
        """Opening net liquidating value."""
        return parse_float(self._data.get("open"), 0.0)

    @property
    def high(self) -> float:
        """Highest net liquidating value during the period."""
        return parse_float(self._data.get("high"), 0.0)

    @property
    def low(self) -> float:
        """Lowest net liquidating value during the period."""
        return parse_float(self._data.get("low"), 0.0)

    @property
    def close(self) -> float:
        """Closing net liquidating value."""
        return parse_float(self._data.get("close"), 0.0)

    @property
    def pending_cash_open(self) -> float:
        """Opening pending cash value."""
        return parse_float(self._data.get("pending-cash-open"), 0.0)

    @property
    def pending_cash_high(self) -> float:
        """Highest pending cash value during the period."""
        return parse_float(self._data.get("pending-cash-high"), 0.0)

    @property
    def pending_cash_low(self) -> float:
        """Lowest pending cash value during the period."""
        return parse_float(self._data.get("pending-cash-low"), 0.0)

    @property
    def pending_cash_close(self) -> float:
        """Closing pending cash value."""
        return parse_float(self._data.get("pending-cash-close"), 0.0)

    @property
    def total_open(self) -> float:
        """Opening total value (net liq + pending cash)."""
        return parse_float(self._data.get("total-open"), 0.0)

    @property
    def total_high(self) -> float:
        """Highest total value during the period."""
        return parse_float(self._data.get("total-high"), 0.0)

    @property
    def total_low(self) -> float:
        """Lowest total value during the period."""
        return parse_float(self._data.get("total-low"), 0.0)

    @property
    def total_close(self) -> float:
        """Closing total value (net liq + pending cash)."""
        return parse_float(self._data.get("total-close"), 0.0)

    @property
    def time(self) -> datetime.datetime | None:
        """Timestamp of this data point."""
        return parse_datetime(self._data.get("time"))

    def print_summary(self) -> None:
        """Print a plain text summary of this history item."""
        time_str = self.time.strftime("%Y-%m-%d %H:%M:%S") if self.time else "N/A"
        print(f"  Time: {time_str}")
        print(
            f"    Net Liq - O: ${self.open:,.2f}, H: ${self.high:,.2f}, L: ${self.low:,.2f}, C: ${self.close:,.2f}"
        )
        print(
            f"    Pending - O: ${self.pending_cash_open:,.2f}, H: ${self.pending_cash_high:,.2f}, L: ${self.pending_cash_low:,.2f}, C: ${self.pending_cash_close:,.2f}"
        )
        print(
            f"    Total   - O: ${self.total_open:,.2f}, H: ${self.total_high:,.2f}, L: ${self.total_low:,.2f}, C: ${self.total_close:,.2f}"
        )

    def pretty_print(self) -> None:
        """Print a rich formatted output of this history item."""
        console = Console()

        table = Table(
            title=f"Net Liq Snapshot - {self.time.strftime('%Y-%m-%d %H:%M:%S') if self.time else 'N/A'}",
            show_header=True,
            header_style="bold blue",
        )
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Open", style="green", justify="right")
        table.add_column("High", style="yellow", justify="right")
        table.add_column("Low", style="red", justify="right")
        table.add_column("Close", style="magenta", justify="right")

        table.add_row(
            "Net Liq",
            f"${self.open:,.2f}",
            f"${self.high:,.2f}",
            f"${self.low:,.2f}",
            f"${self.close:,.2f}",
        )
        table.add_row(
            "Pending Cash",
            f"${self.pending_cash_open:,.2f}",
            f"${self.pending_cash_high:,.2f}",
            f"${self.pending_cash_low:,.2f}",
            f"${self.pending_cash_close:,.2f}",
        )
        table.add_row(
            "Total",
            f"${self.total_open:,.2f}",
            f"${self.total_high:,.2f}",
            f"${self.total_low:,.2f}",
            f"${self.total_close:,.2f}",
        )

        console.print(table)


class NetLiqHistory:
    """Represents the net liquidating value history for an account."""

    def __init__(self, account_number: str, session: Session) -> None:
        """
        Initialize the net liq history.

        Args:
            account_number: The account number to fetch history for.
            session: Active TastyTrade session.
        """
        self._session = session
        self._account_number = account_number
        self._url_endpoint = f"/accounts/{account_number}/net-liq/history"
        self._request_json_data: dict[str, Any] = {}
        self._items: list[NetLiqHistoryItem] = []

    def sync(
        self,
        time_back: TimeBack | None = None,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
        interval: str | None = None,
    ) -> None:
        """
        Fetch net liquidating value history from the API.

        Either use time_back for a relative time period, or start_time/end_time for a specific window.
        You cannot use both time_back and start_time/end_time together.

        Args:
            time_back: Relative time period (e.g., TimeBack.ONE_DAY, TimeBack.ONE_WEEK).
            start_time: Start time of the window (ISO 8601 format with timezone).
            end_time: End time of the window (ISO 8601 format with timezone).
            interval: Time interval for data points (e.g., "1m", "5m", "1h", "1d").

        Raises:
            ValueError: If both time_back and start_time/end_time are provided, or if neither is provided.
            translate_error_code: If the API request fails.
        """
        # Validate parameters
        has_time_back = time_back is not None
        has_window = start_time is not None or end_time is not None

        if has_time_back and has_window:
            raise ValueError(
                "Cannot use both time_back and start_time/end_time. Choose one approach."
            )

        if not has_time_back and not has_window:
            raise ValueError("Must provide either time_back or start_time/end_time.")

        # Build query parameters
        params: dict[str, Any] = {}

        if time_back:
            params["time-back"] = time_back.value

        if start_time:
            # Format as ISO 8601 with timezone
            params["start-time"] = start_time.isoformat()

        if end_time:
            # Format as ISO 8601 with timezone
            params["end-time"] = end_time.isoformat()

        if interval:
            params["interval"] = interval

        # Make API request
        response = self._session.client.get(self._url_endpoint, params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse items - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._items = [NetLiqHistoryItem(item) for item in items_data]

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    @property
    def account_number(self) -> str:
        """Account number for this history."""
        return self._account_number

    @property
    def items(self) -> list[NetLiqHistoryItem]:
        """List of net liquidating value history items."""
        return self._items

    def print_summary(self) -> None:
        """Print a plain text summary of the net liq history."""
        print(f"\n{'=' * 80}")
        print(f"NET LIQUIDATING VALUE HISTORY - Account {self._account_number}")
        print(f"Total Data Points: {len(self._items)}")
        print(f"{'=' * 80}")

        if self._items:
            print(
                f"First: {self._items[0].time.strftime('%Y-%m-%d %H:%M:%S') if self._items[0].time else 'N/A'}"
            )
            print(
                f"Last:  {self._items[-1].time.strftime('%Y-%m-%d %H:%M:%S') if self._items[-1].time else 'N/A'}"
            )
            print("\nShowing up to first 10 entries:")
            print("-" * 80)

            for item in self._items[:10]:
                item.print_summary()
                print()
        else:
            print("\nNo data points available.")

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the net liq history."""
        console = Console()

        # Create summary panel
        if self._items:
            first_time = (
                self._items[0].time.strftime("%Y-%m-%d %H:%M:%S")
                if self._items[0].time
                else "N/A"
            )
            last_time = (
                self._items[-1].time.strftime("%Y-%m-%d %H:%M:%S")
                if self._items[-1].time
                else "N/A"
            )
            summary = f"[bold]Account:[/bold] {self._account_number}\n"
            summary += f"[bold]Data Points:[/bold] {len(self._items)}\n"
            summary += f"[bold]Period:[/bold] {first_time} to {last_time}"
        else:
            summary = f"[bold]Account:[/bold] {self._account_number}\n[yellow]No data available[/yellow]"

        console.print(
            Panel(summary, title="Net Liquidating Value History", border_style="green")
        )

        if not self._items:
            return

        # Create table with summary of all items
        table = Table(
            title=f"Net Liq History Overview ({len(self._items)} data points)",
            show_header=True,
            header_style="bold blue",
        )
        table.add_column("Time", style="cyan", no_wrap=True)
        table.add_column("Net Liq Close", style="green", justify="right")
        table.add_column("Pending Cash", style="yellow", justify="right")
        table.add_column("Total Close", style="magenta", justify="right")
        table.add_column("Change (O to C)", style="white", justify="right")

        # Show up to 20 entries in the table
        for item in self._items[:20]:
            time_str = item.time.strftime("%Y-%m-%d %H:%M") if item.time else "N/A"
            change = item.close - item.open
            change_str = f"${change:+,.2f}" if change != 0 else "$0.00"

            table.add_row(
                time_str,
                f"${item.close:,.2f}",
                f"${item.pending_cash_close:,.2f}",
                f"${item.total_close:,.2f}",
                change_str,
            )

        console.print(table)

        if len(self._items) > 20:
            console.print(
                f"\n[dim]Showing first 20 of {len(self._items)} data points[/dim]"
            )
