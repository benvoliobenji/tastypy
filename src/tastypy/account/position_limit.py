"""Position limits for an account."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..errors import translate_error_code
from ..session import Session
from ..utils.decode_json import parse_int


class PositionLimit:
    """Represents position limits for an account.

    This class fetches the position size and order size limits that apply
    to various instrument types for an account.
    """

    def __init__(self, account_number: str, session: Session) -> None:
        """Initialize PositionLimit with account number and session.

        Args:
            account_number: The account number to fetch position limits for
            session: Active session with valid authentication
        """
        self._session = session
        self._account_number = account_number
        self._url_endpoint = f"/accounts/{account_number}/position-limit"
        self._limit_json: dict = {}

    def sync(self) -> None:
        """Fetch position limits for the account."""
        response = self._session.client.get(self._url_endpoint)
        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get("data", {})
            # Handle null/None data
            self._limit_json = data if data is not None else {}
        else:
            error_code = response.status_code
            try:
                error_message = (
                    response.json().get("error", {}).get("message", "Unknown error")
                )
            except Exception:
                error_message = f"HTTP {error_code}: {response.text[:200]}"
            raise translate_error_code(error_code, error_message)

    @property
    def id(self) -> int:
        """Get the position limit ID."""
        return parse_int(self._limit_json.get("id"))

    @property
    def account_number(self) -> str:
        """Get the account number."""
        return self._limit_json.get("account-number", self._account_number)

    @property
    def equity_order_size(self) -> int:
        """Get the equity order size limit."""
        return parse_int(self._limit_json.get("equity-order-size"))

    @property
    def equity_option_order_size(self) -> int:
        """Get the equity option order size limit."""
        return parse_int(self._limit_json.get("equity-option-order-size"))

    @property
    def future_order_size(self) -> int:
        """Get the future order size limit."""
        return parse_int(self._limit_json.get("future-order-size"))

    @property
    def future_option_order_size(self) -> int:
        """Get the future option order size limit."""
        return parse_int(self._limit_json.get("future-option-order-size"))

    @property
    def underlying_opening_order_limit(self) -> int:
        """Get the underlying opening order limit."""
        return parse_int(self._limit_json.get("underlying-opening-order-limit"))

    @property
    def equity_position_size(self) -> int:
        """Get the equity position size limit."""
        return parse_int(self._limit_json.get("equity-position-size"))

    @property
    def equity_option_position_size(self) -> int:
        """Get the equity option position size limit."""
        return parse_int(self._limit_json.get("equity-option-position-size"))

    @property
    def future_position_size(self) -> int:
        """Get the future position size limit."""
        return parse_int(self._limit_json.get("future-position-size"))

    @property
    def future_option_position_size(self) -> int:
        """Get the future option position size limit."""
        return parse_int(self._limit_json.get("future-option-position-size"))

    @property
    def raw_json(self) -> dict:
        """Get the raw JSON response from the API."""
        return self._limit_json

    def print_summary(self) -> None:
        """Print a plain text summary of the position limits."""
        print(f"\n{'=' * 80}")
        print(f"POSITION LIMITS: {self.account_number}")
        print(f"{'=' * 80}")
        print(f"ID: {self.id}")
        print()
        print("Order Size Limits:")
        print(f"  Equity Order Size: {self.equity_order_size:,}")
        print(f"  Equity Option Order Size: {self.equity_option_order_size:,}")
        print(f"  Future Order Size: {self.future_order_size:,}")
        print(f"  Future Option Order Size: {self.future_option_order_size:,}")
        print(
            f"  Underlying Opening Order Limit: {self.underlying_opening_order_limit:,}"
        )
        print()
        print("Position Size Limits:")
        print(f"  Equity Position Size: {self.equity_position_size:,}")
        print(f"  Equity Option Position Size: {self.equity_option_position_size:,}")
        print(f"  Future Position Size: {self.future_position_size:,}")
        print(f"  Future Option Position Size: {self.future_option_position_size:,}")
        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print rich formatted output of the position limits."""
        console = Console()

        # Main info table
        info_table = Table(
            title=f"Position Limits: {self.account_number}",
            show_header=True,
            header_style="bold blue",
        )
        info_table.add_column("Property", style="cyan", no_wrap=True)
        info_table.add_column("Value", style="green")

        info_table.add_row("ID", str(self.id))
        info_table.add_row("Account Number", self.account_number)

        # Order size limits table
        order_table = Table(
            title="Order Size Limits",
            show_header=True,
            header_style="bold yellow",
        )
        order_table.add_column("Instrument Type", style="cyan")
        order_table.add_column("Limit", style="green", justify="right")

        order_table.add_row("Equity Order Size", f"{self.equity_order_size:,}")
        order_table.add_row(
            "Equity Option Order Size", f"{self.equity_option_order_size:,}"
        )
        order_table.add_row("Future Order Size", f"{self.future_order_size:,}")
        order_table.add_row(
            "Future Option Order Size", f"{self.future_option_order_size:,}"
        )
        order_table.add_row(
            "Underlying Opening Order Limit", f"{self.underlying_opening_order_limit:,}"
        )

        # Position size limits table
        position_table = Table(
            title="Position Size Limits",
            show_header=True,
            header_style="bold magenta",
        )
        position_table.add_column("Instrument Type", style="cyan")
        position_table.add_column("Limit", style="green", justify="right")

        position_table.add_row("Equity Position Size", f"{self.equity_position_size:,}")
        position_table.add_row(
            "Equity Option Position Size", f"{self.equity_option_position_size:,}"
        )
        position_table.add_row("Future Position Size", f"{self.future_position_size:,}")
        position_table.add_row(
            "Future Option Position Size", f"{self.future_option_position_size:,}"
        )

        # Print all tables
        console.print(
            Panel(
                info_table,
                title="[bold blue]Account Information[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                order_table,
                title="[bold yellow]Order Size Limits[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                position_table,
                title="[bold magenta]Position Size Limits[/bold magenta]",
                border_style="magenta",
            )
        )

    def __str__(self) -> str:
        return f"PositionLimit({self.account_number})"
