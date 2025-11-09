"""Current session model."""

from rich.console import Console
from rich.table import Table

from tastypy.market_sessions.base.simple_session import SimpleSession
from tastypy.market_sessions.base.next_session import NextSession
from tastypy.market_sessions.base.previous_session import PreviousSession
from ...utils import format_datetime_with_local


class CurrentSession(SimpleSession):
    """
    Represents the current market session with additional context.

    Includes state information and references to previous/next sessions.
    """

    @property
    def state(self) -> str:
        """Current session state (e.g., 'Open', 'Closed', 'Pre-Market', 'Post-Market')."""
        return self._json.get("state", "")

    @property
    def next_session(self) -> NextSession | None:
        """Next market session information."""
        next_data = self._json.get("next-session")
        if next_data:
            return NextSession(next_data)
        return None

    @property
    def previous_session(self) -> PreviousSession | None:
        """Previous market session information."""
        prev_data = self._json.get("previous-session")
        if prev_data:
            return PreviousSession(prev_data)
        return None

    def print_summary(self) -> None:
        """Print a plain text summary of the current session."""
        print(f"\n  Current Session for {self.instrument_collection}:")
        print(f"    State: {self.state}")
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

        if self.next_session:
            print("\n  Next Session:")
            print(f"    Date: {self.next_session.session_date}")
            if self.next_session.start_at:
                print(
                    f"    Start: {self.next_session.start_at.strftime('%Y-%m-%d %H:%M:%S %Z')}"
                )

        if self.previous_session:
            print("\n  Previous Session:")
            print(f"    Date: {self.previous_session.session_date}")
            if self.previous_session.close_at:
                print(
                    f"    Closed: {self.previous_session.close_at.strftime('%Y-%m-%d %H:%M:%S %Z')}"
                )

    def pretty_print(self) -> None:
        """Print a rich formatted output of the current session."""
        console = Console()

        # Main session table
        table = Table(title=f"Current Session: {self.instrument_collection}")
        table.add_column("Field", style="cyan")
        table.add_column("UTC", style="green")
        table.add_column("Local Time", style="yellow")

        table.add_row("State", f"[bold]{self.state}[/bold]", "")
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

        # Next/Previous sessions
        if self.next_session or self.previous_session:
            context_table = Table(title="Adjacent Sessions")
            context_table.add_column("Session", style="yellow")
            context_table.add_column("Date", style="cyan")
            context_table.add_column("Time (UTC)", style="green")
            context_table.add_column("Time (Local)", style="magenta")

            if self.previous_session:
                prev_time_utc = ""
                prev_time_local = ""
                if self.previous_session.close_at:
                    prev_time_utc = (
                        f"Closed: {self.previous_session.close_at.strftime('%H:%M:%S')}"
                    )
                    local_close = self.previous_session.close_at.astimezone()
                    prev_time_local = f"Closed: {local_close.strftime('%H:%M:%S')}"
                context_table.add_row(
                    "Previous",
                    str(self.previous_session.session_date),
                    prev_time_utc,
                    prev_time_local,
                )

            if self.next_session:
                next_time_utc = ""
                next_time_local = ""
                if self.next_session.start_at:
                    next_time_utc = (
                        f"Opens: {self.next_session.start_at.strftime('%H:%M:%S')}"
                    )
                    local_start = self.next_session.start_at.astimezone()
                    next_time_local = f"Opens: {local_start.strftime('%H:%M:%S')}"
                context_table.add_row(
                    "Next",
                    str(self.next_session.session_date),
                    next_time_utc,
                    next_time_local,
                )

            console.print(context_table)
