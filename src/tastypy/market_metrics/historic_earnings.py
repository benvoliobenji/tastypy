import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.market_metrics.earnings_info import EarningsInfo
from tastypy.session import Session


class HistoricEarnings:
    """
    A class for fetching historical earnings data for a symbol.

    This endpoint returns historical earnings information including dates and EPS.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the historic earnings fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._earnings: list[EarningsInfo] = []
        self._symbol: str = ""

    def sync(
        self,
        symbol: str,
        start_date: datetime.date,
        end_date: datetime.date | None = None,
    ) -> None:
        """
        Fetch historical earnings data for the given symbol.

        Args:
            symbol: Symbol to get earnings data for (e.g., "AAPL").
            start_date: Limits earnings data from start_date until now (or end_date if provided).
            end_date: Optional end date to limit earnings data range.

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If symbol is empty or start_date is not provided.
        """
        if not symbol:
            raise ValueError("Symbol is required.")
        if not start_date:
            raise ValueError("Start date is required.")

        self._symbol = symbol

        # Build query parameters
        params = {"start-date": start_date.strftime("%Y-%m-%d")}

        if end_date:
            params["end-date"] = end_date.strftime("%Y-%m-%d")

        response = self._session.client.get(
            f"/market-metrics/historic-corporate-events/earnings-reports/{symbol}",
            params=params,
        )

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse earnings - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._earnings = [EarningsInfo(item) for item in items_data]

    @property
    def symbol(self) -> str:
        """Symbol that earnings data was fetched for."""
        return self._symbol

    @property
    def earnings(self) -> list[EarningsInfo]:
        """List of earnings items returned from the API."""
        return self._earnings

    def print_summary(self) -> None:
        """Print a plain text summary of all earnings."""
        print(f"\n{'=' * 80}")
        print(f"HISTORIC EARNINGS FOR {self._symbol} ({len(self._earnings)} records)")
        print(f"{'=' * 80}")

        for earning in self._earnings:
            earning.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all earnings."""
        console = Console()

        # Create earnings table
        earnings_table = Table(
            title=f"Historic Earnings for {self._symbol} ({len(self._earnings)} records)",
            show_header=True,
            header_style="bold blue",
        )
        earnings_table.add_column("Date", style="cyan", no_wrap=True)
        earnings_table.add_column("EPS", style="green", justify="right")

        for earning in self._earnings:
            date_str = str(earning.occurred_date) if earning.occurred_date else "N/A"
            earnings_table.add_row(date_str, f"${earning.eps:.4f}")

        console.print(
            Panel(
                earnings_table,
                title=f"[bold blue]Earnings - {self._symbol}[/bold blue]",
                border_style="blue",
            )
        )
