"""Simple market session model."""

import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.utils.decode_json import parse_date, parse_datetime
from ...utils import format_datetime_with_local


class SimpleSession:
    """
    Represents a simple market session with basic timing information.

    This is the base model for market session data.
    """

    def __init__(self, json_data: dict[str, Any]) -> None:
        """
        Initialize a simple session from API JSON data.

        Args:
            json_data: Raw JSON data from the API.
        """
        self._json = json_data

    @property
    def close_at(self) -> datetime.datetime | None:
        """Market close time (regular hours)."""
        return parse_datetime(self._json.get("close-at"))

    @property
    def close_at_ext(self) -> datetime.datetime | None:
        """Market close time including extended hours."""
        return parse_datetime(self._json.get("close-at-ext"))

    @property
    def instrument_collection(self) -> str:
        """Instrument collection name (e.g., 'Equity', 'CME', 'CFE')."""
        return self._json.get("instrument-collection", "")

    @property
    def open_at(self) -> datetime.datetime | None:
        """Market open time (regular hours)."""
        return parse_datetime(self._json.get("open-at"))

    @property
    def start_at(self) -> datetime.datetime | None:
        """Market session start time (including pre-market)."""
        return parse_datetime(self._json.get("start-at"))

    @property
    def session_date(self) -> datetime.date | None:
        """Session date (only available in some session types)."""
        return parse_date(self._json.get("session-date"))

    def print_summary(self) -> None:
        """Print a plain text summary of the session."""
        print(f"\n  Session for {self.instrument_collection}:")
        if self.session_date:
            print(f"    Date: {self.session_date}")
        if self.start_at:
            print(f"    Start: {self.start_at.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        if self.open_at:
            print(f"    Open: {self.open_at.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        if self.close_at:
            print(f"    Close: {self.close_at.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        if self.close_at_ext:
            print(
                f"    Close (Extended): {self.close_at_ext.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            )

    def pretty_print(self) -> None:
        """Print a rich formatted output of the session."""
        console = Console()

        table = Table(title=f"Session: {self.instrument_collection}")
        table.add_column("Field", style="cyan")
        table.add_column("UTC", style="green")
        table.add_column("Local Time", style="yellow")

        if self.session_date:
            table.add_row("Date", str(self.session_date), "")
        if self.start_at:
            utc_str, local_str = format_datetime_with_local(self.start_at)
            table.add_row("Start", utc_str, local_str)
        if self.open_at:
            utc_str, local_str = format_datetime_with_local(self.open_at)
            table.add_row("Open", utc_str, local_str)
        if self.close_at:
            utc_str, local_str = format_datetime_with_local(self.close_at)
            table.add_row("Close", utc_str, local_str)
        if self.close_at_ext:
            utc_str, local_str = format_datetime_with_local(self.close_at_ext)
            table.add_row("Close (Extended)", utc_str, local_str)

        console.print(table)
