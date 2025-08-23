import datetime
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .session import Session
from .errors import translate_error_code


class QuoteStreamerTokenAuthResult:
    """A class representing the appropriate API quote streamer endpoint, level and identification token
    for the current customer to receive market data.
    """

    _extension_url = "/api-quote-tokens"
    _session_client: httpx.Client
    _session: Session

    def __init__(self, active_session: Session):
        self._session = active_session
        self._session_client = active_session.client

    def sync(self):
        """Synchronize the token information with the API.

        Raises:
            translate_error_code: Raised when the API request fails.
        """
        response = self._session_client.get(self._extension_url)
        if response.status_code != 200:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)
        else:
            self._request_json_data = response.json()["data"]

    @property
    def dxlink_url(self) -> str:
        return self._request_json_data.get("dxlink-url", "")

    @property
    def expires_at(self) -> datetime.datetime | None:
        expires_at_str = self._request_json_data.get("expires-at", "")
        if not expires_at_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))

    @property
    def issued_at(self) -> datetime.datetime | None:
        issued_at_str = self._request_json_data.get("issued-at", "")
        if not issued_at_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(issued_at_str.replace("Z", "+00:00"))

    @property
    def level(self) -> str:
        return self._request_json_data.get("level", "")

    @property
    def token(self) -> str:
        return self._request_json_data.get("token", "")

    @property
    def websocket_url(self) -> str:
        return self._request_json_data.get("websocket-url", "")

    def print_summary(self) -> None:
        """Print a simple text summary of the quote streamer token authentication result."""
        print(f"\n{'=' * 60}")
        print("QUOTE STREAMER TOKEN SUMMARY")
        print(f"{'=' * 60}")
        print(f"Level: {self.level}")
        print(
            f"Token: {self.token[:20]}...{self.token[-10:] if len(self.token) > 30 else self.token}"
        )
        print(f"DXLink URL: {self.dxlink_url}")
        print(f"WebSocket URL: {self.websocket_url}")
        print(f"Issued At: {self.issued_at}")
        print(f"Expires At: {self.expires_at}")
        if self.expires_at:
            now = datetime.datetime.now(self.expires_at.tzinfo)
            time_until_expiry = self.expires_at - now
            if time_until_expiry.total_seconds() > 0:
                print(f"Time Until Expiry: {time_until_expiry}")
            else:
                print(f"Status: EXPIRED ({abs(time_until_expiry)} ago)")
        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all quote streamer token data in a nicely formatted table."""
        console = Console()

        # Create token information table
        token_table = Table(
            title="Quote Streamer Token Authentication",
            show_header=True,
            header_style="bold blue",
        )
        token_table.add_column("Property", style="cyan", no_wrap=True)
        token_table.add_column("Value", style="green")

        # Token information
        token_table.add_row("Level", str(self.level))
        truncated_token = (
            f"{self.token[:20]}...{self.token[-10:]}"
            if len(self.token) > 30
            else self.token
        )
        token_table.add_row("Token", truncated_token)
        token_table.add_row("DXLink URL", str(self.dxlink_url))
        token_table.add_row("WebSocket URL", str(self.websocket_url))

        # Timing information table
        timing_table = Table(
            title="Token Timing Information",
            show_header=True,
            header_style="bold yellow",
        )
        timing_table.add_column("Property", style="cyan")
        timing_table.add_column("Value", style="green")

        timing_table.add_row(
            "Issued At", str(self.issued_at) if self.issued_at else "N/A"
        )
        timing_table.add_row(
            "Expires At", str(self.expires_at) if self.expires_at else "N/A"
        )

        if self.expires_at:
            now = datetime.datetime.now(self.expires_at.tzinfo)
            time_until_expiry = self.expires_at - now
            if time_until_expiry.total_seconds() > 0:
                timing_table.add_row("Time Until Expiry", str(time_until_expiry))
                timing_table.add_row("Status", "✓ Valid")
            else:
                timing_table.add_row("Time Since Expired", str(abs(time_until_expiry)))
                timing_table.add_row("Status", "✗ EXPIRED")
        else:
            timing_table.add_row("Status", "Unknown")

        # Print all tables
        console.print(
            Panel(
                token_table,
                title="[bold blue]Token Information[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                timing_table,
                title="[bold yellow]Timing Information[/bold yellow]",
                border_style="yellow",
            )
        )

    def __str__(self):
        return f"QuoteStreamerTokenAuthResult(level={self.level}, token={self.token})"
