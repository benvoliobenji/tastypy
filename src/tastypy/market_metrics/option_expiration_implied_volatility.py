import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.utils.decode_json import parse_datetime, parse_float


class OptionExpirationImpliedVolatility:
    """Dataclass containing implied volatility data for a specific option expiration."""

    def __init__(self, data: dict[str, Any]) -> None:
        """
        Initialize option expiration IV data from JSON data.

        Args:
            data: Dictionary containing option expiration IV data from API.
        """
        self._data = data

    @property
    def expiration_date(self) -> datetime.datetime | None:
        """Option expiration date."""
        value = self._data.get("expiration-date")
        return parse_datetime(value)

    @property
    def settlement_type(self) -> str:
        """AM or PM settlement."""
        return self._data.get("settlement-type", "")

    @property
    def option_chain_type(self) -> str:
        """Option chain type (e.g., Standard or Non-standard)."""
        return self._data.get("option-chain-type", "")

    @property
    def implied_volatility(self) -> float:
        """Implied volatility of option expiration."""
        return parse_float(self._data.get("implied-volatility"), 0.0)

    def print_summary(self) -> None:
        """Print a plain text summary of the option expiration IV."""
        exp_date_str = (
            self.expiration_date.strftime("%Y-%m-%d") if self.expiration_date else "N/A"
        )
        print(
            f"  Exp: {exp_date_str}, Settlement: {self.settlement_type}, "
            f"Type: {self.option_chain_type}, IV: {self.implied_volatility * 100:.2f}%"
        )

    def pretty_print(self) -> None:
        """Print a rich formatted output of the option expiration IV."""
        console = Console()

        table = Table(
            title="Option Expiration IV Details",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        exp_date_str = (
            self.expiration_date.strftime("%Y-%m-%d %H:%M:%S")
            if self.expiration_date
            else "N/A"
        )
        table.add_row("Expiration Date", exp_date_str)
        table.add_row("Settlement Type", self.settlement_type)
        table.add_row("Option Chain Type", self.option_chain_type)
        table.add_row("Implied Volatility", f"{self.implied_volatility * 100:.2f}%")

        console.print(table)
