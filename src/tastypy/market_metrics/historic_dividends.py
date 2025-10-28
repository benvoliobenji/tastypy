from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.market_metrics.dividend_info import DividendInfo
from tastypy.session import Session


class HistoricDividends:
    """
    A class for fetching historical dividend data for a symbol.

    This endpoint returns historical dividend information including dates and amounts.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the historic dividends fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._dividends: list[DividendInfo] = []
        self._symbol: str = ""

    def sync(self, symbol: str) -> None:
        """
        Fetch historical dividend data for the given symbol.

        Args:
            symbol: Symbol to get dividend data for (e.g., "AAPL").

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If symbol is empty.
        """
        if not symbol:
            raise ValueError("Symbol is required.")

        self._symbol = symbol

        response = self._session.client.get(
            f"/market-metrics/historic-corporate-events/dividends/{symbol}"
        )

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse dividends - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._dividends = [DividendInfo(item) for item in items_data]

    @property
    def symbol(self) -> str:
        """Symbol that dividend data was fetched for."""
        return self._symbol

    @property
    def dividends(self) -> list[DividendInfo]:
        """List of dividend items returned from the API."""
        return self._dividends

    def print_summary(self) -> None:
        """Print a plain text summary of all dividends."""
        print(f"\n{'=' * 80}")
        print(f"HISTORIC DIVIDENDS FOR {self._symbol} ({len(self._dividends)} records)")
        print(f"{'=' * 80}")

        for dividend in self._dividends:
            dividend.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all dividends."""
        console = Console()

        # Create dividends table
        dividends_table = Table(
            title=f"Historic Dividends for {self._symbol} ({len(self._dividends)} records)",
            show_header=True,
            header_style="bold blue",
        )
        dividends_table.add_column("Date", style="cyan", no_wrap=True)
        dividends_table.add_column("Amount", style="green", justify="right")

        for dividend in self._dividends:
            date_str = str(dividend.occurred_date) if dividend.occurred_date else "N/A"
            dividends_table.add_row(date_str, f"${dividend.amount:.4f}")

        console.print(
            Panel(
                dividends_table,
                title=f"[bold blue]Dividends - {self._symbol}[/bold blue]",
                border_style="blue",
            )
        )
