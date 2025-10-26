"""Market data module for fetching market data by instrument type."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.market_data.market_data_item import MarketDataItem
from tastypy.session import Session


class MarketDataByType:
    """
    A class for fetching market data for multiple symbols grouped by instrument type.

    This endpoint allows fetching market data for up to 100 symbols across different
    instrument types in a single request.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the market data fetcher.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._request_json_data: dict[str, Any] = {}
        self._items: list[MarketDataItem] = []

    def sync(
        self,
        indices: list[str] | None = None,
        equities: list[str] | None = None,
        equity_options: list[str] | None = None,
        futures: list[str] | None = None,
        future_options: list[str] | None = None,
        cryptocurrencies: list[str] | None = None,
    ) -> None:
        """
        Fetch market data for the given symbols grouped by instrument type.

        Combined limit across all types is 100 symbols.

        Args:
            indices: List of index symbols (e.g., ["SPX", "VIX"]).
            equities: List of equity symbols (e.g., ["AAPL", "MSFT"]).
            equity_options: List of equity option symbols (OCC format).
            futures: List of futures symbols (e.g., ["/ES", "/NQ"]).
            future_options: List of future option symbols.
            cryptocurrencies: List of cryptocurrency symbols (e.g., ["BTC/USD"]).

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If the total number of symbols exceeds 100.
            NotImplementedError: If the sandbox environment is used.
        """
        if self._session.is_sandbox():
            raise NotImplementedError(
                "MarketDataByType is not supported in the sandbox environment."
            )
        params = {
            "index": indices or [],
            "equity": equities or [],
            "equity-option": equity_options or [],
            "future": futures or [],
            "future-option": future_options or [],
            "cryptocurrency": cryptocurrencies or [],
        }

        # Ensure we do not exceed 100 symbols total
        total_symbols = sum(len(v) for v in params.values())
        if total_symbols > 100:
            raise ValueError(
                "Total number of symbols across all types cannot exceed 100."
            )

        response = self._session.client.get("/market-data/by-type", params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse items - TastyTrade API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._items = [MarketDataItem(item) for item in items_data]

    @property
    def items(self) -> list[MarketDataItem]:
        """List of market data items returned from the API."""
        return self._items

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all market data."""
        print(f"\n{'=' * 80}")
        print(f"MARKET DATA SUMMARY ({len(self._items)} items)")
        print(f"{'=' * 80}")

        for item in self._items:
            item.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all market data."""
        console = Console()

        # Create summary table
        summary_table = Table(
            title=f"Market Data Overview ({len(self._items)} symbols)",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Symbol", style="cyan", no_wrap=True)
        summary_table.add_column("Type", style="yellow")
        summary_table.add_column("Mark", style="green", justify="right")
        summary_table.add_column("Bid", style="magenta", justify="right")
        summary_table.add_column("Ask", style="magenta", justify="right")
        summary_table.add_column("Last", style="green", justify="right")
        summary_table.add_column("Volume", style="blue", justify="right")

        for item in self._items:
            mark_str = f"${item.mark:.2f}" if item.mark else "N/A"
            bid_str = f"${item.bid:.2f}" if item.bid else "N/A"
            ask_str = f"${item.ask:.2f}" if item.ask else "N/A"
            last_str = f"${item.last:.2f}" if item.last else "N/A"
            volume_str = f"{item.volume:,.0f}" if item.volume else "N/A"

            summary_table.add_row(
                item.symbol,
                item.instrument_type.value,
                mark_str,
                bid_str,
                ask_str,
                last_str,
                volume_str,
            )

        console.print(
            Panel(
                summary_table,
                title="[bold blue]Market Data By Type[/bold blue]",
                border_style="blue",
            )
        )
