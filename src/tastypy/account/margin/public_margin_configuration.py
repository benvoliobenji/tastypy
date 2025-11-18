"""Public margin configuration (global settings)."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...errors import translate_error_code
from ...session import Session
from ...utils.decode_json import parse_float


class PublicMarginConfiguration:
    """Represents publicly accessible, read-only margin configuration.

    This class fetches global margin configuration settings that apply
    across all accounts, such as the risk-free rate used in calculations.
    """

    def __init__(self, session: Session) -> None:
        """Initialize PublicMarginConfiguration with session.

        Args:
            session: Active session with valid authentication
        """
        self._session = session
        self._url_endpoint = "/margin-requirements-public-configuration"
        self._config_json: dict = {}

    def sync(self) -> None:
        """Fetch public margin configuration."""
        response = self._session.client.get(self._url_endpoint)
        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get("data", {})
            # Handle null/None data
            self._config_json = data if data is not None else {}
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
    def risk_free_rate(self) -> float:
        """Get the risk-free rate used in margin calculations."""
        return parse_float(self._config_json.get("risk-free-rate"))

    @property
    def raw_json(self) -> dict:
        """Get the raw JSON response from the API."""
        return self._config_json

    def print_summary(self) -> None:
        """Print a plain text summary of the public margin configuration."""
        print(f"\n{'=' * 80}")
        print("PUBLIC MARGIN CONFIGURATION")
        print(f"{'=' * 80}")
        print(
            f"Risk-Free Rate: {self.risk_free_rate:.6f} ({self.risk_free_rate * 100:.4f}%)"
        )
        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print rich formatted output of the public margin configuration."""
        console = Console()

        # Configuration table
        config_table = Table(
            title="Public Margin Configuration",
            show_header=True,
            header_style="bold blue",
        )
        config_table.add_column("Parameter", style="cyan", no_wrap=True)
        config_table.add_column("Value", style="green", justify="right")

        config_table.add_row("Risk-Free Rate (Decimal)", f"{self.risk_free_rate:.6f}")
        config_table.add_row(
            "Risk-Free Rate (Percentage)", f"{self.risk_free_rate * 100:.4f}%"
        )

        console.print(
            Panel(
                config_table,
                title="[bold blue]Global Margin Settings[/bold blue]",
                border_style="blue",
            )
        )

    def __str__(self) -> str:
        return f"PublicMarginConfiguration(risk_free_rate={self.risk_free_rate:.6f})"
