"""Effective margin requirements for a specific underlying symbol."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...errors import translate_error_code
from ...session import Session
from ...utils.decode_json import parse_float


class EffectiveMarginRequirement:
    """Represents the effective margin requirements for a specific underlying symbol.

    This class fetches margin requirement parameters that apply to a specific
    underlying symbol for an account.
    """

    def __init__(
        self, account_number: str, underlying_symbol: str, session: Session
    ) -> None:
        """Initialize EffectiveMarginRequirement with account number, symbol and session.

        Args:
            account_number: The account number to fetch margin requirements for
            underlying_symbol: The underlying symbol to fetch requirements for
            session: Active session with valid authentication
        """
        self._session = session
        self._account_number = account_number
        self._underlying_symbol = underlying_symbol
        self._url_endpoint = f"/accounts/{account_number}/margin-requirements/{underlying_symbol}/effective"
        self._margin_json: dict = {}

    def sync(self) -> None:
        """Fetch effective margin requirements for the underlying symbol."""
        response = self._session.client.get(self._url_endpoint)
        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get("data", {})
            # Handle null/None data
            self._margin_json = data if data is not None else {}
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
    def underlying_symbol(self) -> str:
        """Get the underlying symbol."""
        return self._margin_json.get("underlying-symbol", self._underlying_symbol)

    @property
    def long_equity_initial(self) -> float:
        """Get the long equity initial margin requirement."""
        return parse_float(self._margin_json.get("long-equity-initial"))

    @property
    def short_equity_initial(self) -> float:
        """Get the short equity initial margin requirement."""
        return parse_float(self._margin_json.get("short-equity-initial"))

    @property
    def long_equity_maintenance(self) -> float:
        """Get the long equity maintenance margin requirement."""
        return parse_float(self._margin_json.get("long-equity-maintenance"))

    @property
    def short_equity_maintenance(self) -> float:
        """Get the short equity maintenance margin requirement."""
        return parse_float(self._margin_json.get("short-equity-maintenance"))

    @property
    def naked_option_standard(self) -> float:
        """Get the naked option standard margin requirement."""
        return parse_float(self._margin_json.get("naked-option-standard"))

    @property
    def naked_option_minimum(self) -> float:
        """Get the naked option minimum margin requirement."""
        return parse_float(self._margin_json.get("naked-option-minimum"))

    @property
    def naked_option_floor(self) -> float:
        """Get the naked option floor margin requirement."""
        return parse_float(self._margin_json.get("naked-option-floor"))

    @property
    def clearing_identifier(self) -> str:
        """Get the clearing identifier."""
        return self._margin_json.get("clearing-identifier", "")

    @property
    def is_deleted(self) -> bool:
        """Check if this margin requirement has been deleted."""
        return bool(self._margin_json.get("is-deleted", False))

    @property
    def raw_json(self) -> dict:
        """Get the raw JSON response from the API."""
        return self._margin_json

    def print_summary(self) -> None:
        """Print a plain text summary of the effective margin requirements."""
        print(f"\n{'=' * 80}")
        print(f"EFFECTIVE MARGIN REQUIREMENTS: {self.underlying_symbol}")
        print(f"{'=' * 80}")
        print(f"Account Number: {self._account_number}")
        print(f"Clearing Identifier: {self.clearing_identifier}")
        print(f"Is Deleted: {self.is_deleted}")
        print()
        print("Equity Requirements:")
        print(f"  Long Equity Initial: {self.long_equity_initial:.4f}")
        print(f"  Short Equity Initial: {self.short_equity_initial:.4f}")
        print(f"  Long Equity Maintenance: {self.long_equity_maintenance:.4f}")
        print(f"  Short Equity Maintenance: {self.short_equity_maintenance:.4f}")
        print()
        print("Naked Option Requirements:")
        print(f"  Standard: {self.naked_option_standard:.4f}")
        print(f"  Minimum: {self.naked_option_minimum:.4f}")
        print(f"  Floor: {self.naked_option_floor:.4f}")
        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print rich formatted output of the effective margin requirements."""
        console = Console()

        # Main info table
        info_table = Table(
            title=f"Effective Margin Requirements: {self.underlying_symbol}",
            show_header=True,
            header_style="bold blue",
        )
        info_table.add_column("Property", style="cyan", no_wrap=True)
        info_table.add_column("Value", style="green")

        info_table.add_row("Account Number", self._account_number)
        info_table.add_row("Underlying Symbol", self.underlying_symbol)
        info_table.add_row("Clearing Identifier", self.clearing_identifier)
        info_table.add_row("Is Deleted", "Yes" if self.is_deleted else "No")

        # Equity requirements table
        equity_table = Table(
            title="Equity Margin Requirements",
            show_header=True,
            header_style="bold yellow",
        )
        equity_table.add_column("Requirement Type", style="cyan")
        equity_table.add_column("Value", style="green", justify="right")

        equity_table.add_row("Long Equity Initial", f"{self.long_equity_initial:.4f}")
        equity_table.add_row("Short Equity Initial", f"{self.short_equity_initial:.4f}")
        equity_table.add_row(
            "Long Equity Maintenance", f"{self.long_equity_maintenance:.4f}"
        )
        equity_table.add_row(
            "Short Equity Maintenance", f"{self.short_equity_maintenance:.4f}"
        )

        # Naked option requirements table
        option_table = Table(
            title="Naked Option Requirements",
            show_header=True,
            header_style="bold magenta",
        )
        option_table.add_column("Requirement Type", style="cyan")
        option_table.add_column("Value", style="green", justify="right")

        option_table.add_row("Standard", f"{self.naked_option_standard:.4f}")
        option_table.add_row("Minimum", f"{self.naked_option_minimum:.4f}")
        option_table.add_row("Floor", f"{self.naked_option_floor:.4f}")

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
                equity_table,
                title="[bold yellow]Equity Requirements[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                option_table,
                title="[bold magenta]Option Requirements[/bold magenta]",
                border_style="magenta",
            )
        )

    def __str__(self) -> str:
        return f"EffectiveMarginRequirement({self.underlying_symbol})"
