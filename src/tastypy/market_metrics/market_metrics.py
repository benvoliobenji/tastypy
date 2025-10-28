from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.market_metrics.market_metric_info import MarketMetricInfo
from tastypy.session import Session


class MarketMetrics:
    """
    A class for fetching market metrics (volatility and liquidity) for multiple symbols.

    This endpoint returns implied volatility and liquidity data for underlyings,
    as well as option expiration-specific IV data.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the market metrics fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._metrics: list[MarketMetricInfo] = []

    def sync(self, symbols: list[str]) -> None:
        """
        Fetch market metrics for the given symbols.

        Args:
            symbols: List of symbols to fetch metrics for (e.g., ["AAPL", "FB", "BRK/B"]).
                     Note: Use URL encoding for special characters (e.g., "BRK%2FB" for "BRK/B").

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If symbols list is empty.
        """
        if not symbols:
            raise ValueError("At least one symbol is required.")

        # Join symbols with comma for query parameter
        symbols_param = ",".join(symbols)

        response = self._session.client.get(
            "/market-metrics", params={"symbols": symbols_param}
        )

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse metrics - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._metrics = [MarketMetricInfo(item) for item in items_data]

    @property
    def metrics(self) -> list[MarketMetricInfo]:
        """List of market metric items returned from the API."""
        return self._metrics

    def print_summary(self) -> None:
        """Print a plain text summary of all market metrics."""
        print(f"\n{'=' * 80}")
        print(f"MARKET METRICS SUMMARY ({len(self._metrics)} symbols)")
        print(f"{'=' * 80}")

        for metric in self._metrics:
            metric.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all market metrics."""
        console = Console()

        # Create summary table
        summary_table = Table(
            title=f"Market Metrics Overview ({len(self._metrics)} symbols)",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Symbol", style="cyan", no_wrap=True)
        summary_table.add_column("IV Index", style="green", justify="right")
        summary_table.add_column("IV Rank", style="yellow", justify="right")
        summary_table.add_column("IV %ile", style="yellow", justify="right")
        summary_table.add_column("Liquidity", style="magenta", justify="right")
        summary_table.add_column("Liq Rating", style="blue", justify="right")
        summary_table.add_column("# Expirations", style="white", justify="right")

        for metric in self._metrics:
            summary_table.add_row(
                metric.symbol,
                f"{metric.implied_volatility_index * 100:.2f}%",
                f"{metric.implied_volatility_rank * 100:.2f}%",
                f"{metric.implied_volatility_percentile * 100:.2f}%",
                f"{metric.liquidity:.2f}",
                str(metric.liquidity_rating),
                str(len(metric.option_expiration_implied_volatilities)),
            )

        console.print(
            Panel(
                summary_table,
                title="[bold blue]Market Metrics[/bold blue]",
                border_style="blue",
            )
        )
