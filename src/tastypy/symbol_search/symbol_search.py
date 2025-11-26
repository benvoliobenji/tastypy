"""Symbol search functionality for TastyTrade API."""

from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session
from tastypy.symbol_search.symbol_data import SymbolData


class SymbolSearch:
    """
    A class for searching symbols in the TastyTrade API.

    This endpoint allows searching for symbols or symbol fragments,
    returning matching symbols with their metadata.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the symbol search manager.

        Args:
            session: Active TastyTrade session.
        """
        self._session = session
        self._url_endpoint = "/symbols/search"
        self._request_json_data: dict[str, Any] = {}
        self._symbols: list[SymbolData] = []
        self._search_query: str = ""

    def sync(self, symbol: str) -> None:
        """
        Search for symbols matching the given query.

        Args:
            symbol: Symbol or fragment of a symbol to search.
                   For example, "AAP" will return AAP and AAPL data.

        Raises:
            translate_error_code: If the API request fails.
            ValueError: If symbol is empty.
        """
        if not symbol or not symbol.strip():
            raise ValueError("Symbol query cannot be empty.")

        self._search_query = symbol

        response = self._session.client.get(f"{self._url_endpoint}/{symbol}")

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse symbols - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._symbols = [SymbolData(item) for item in items_data]

    @property
    def symbols(self) -> list[SymbolData]:
        """List of symbol data items returned from the search."""
        return self._symbols

    @property
    def search_query(self) -> str:
        """The search query that was used."""
        return self._search_query

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    def print_summary(self) -> None:
        """Print a plain text summary of all search results."""
        print(f"\n{'=' * 80}")
        print(
            f"SYMBOL SEARCH RESULTS for '{self._search_query}' ({len(self._symbols)} results)"
        )
        print(f"{'=' * 80}")

        for symbol_data in self._symbols:
            symbol_data.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all search results."""
        console = Console()

        # Create summary table
        table = Table(
            title=f"Symbol Search Results: '{self._search_query}' ({len(self._symbols)} results)",
            show_header=True,
            header_style="bold blue",
        )
        table.add_column("Symbol", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Market", style="yellow")
        table.add_column("Type", style="magenta")
        table.add_column("Options", style="white")

        for symbol_data in self._symbols:
            table.add_row(
                symbol_data.symbol,
                symbol_data.description,
                symbol_data.listed_market,
                symbol_data.instrument_type,
                "✓" if symbol_data.options else "✗",
            )

        console.print(table)

        # Print detailed info if only one result
        if len(self._symbols) == 1:
            console.print("\n[bold]Detailed Information:[/bold]")
            self._symbols[0].pretty_print()
