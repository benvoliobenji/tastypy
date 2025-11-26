"""Transactions manager for TastyTrade API."""

import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.errors import translate_error_code
from tastypy.session import Session
from tastypy.transactions.enums import InstrumentType, SortOrder, TransactionAction
from tastypy.transactions.transaction import Transaction


class Transactions:
    """
    Manager for account transactions.

    This class provides methods to query account transactions with various
    filters, retrieve individual transactions, and get total fees.
    """

    def __init__(self, account_number: str, session: Session) -> None:
        """
        Initialize the transactions manager.

        Args:
            account_number: The account number to query transactions for.
            session: Active TastyTrade session.
        """
        self._session = session
        self._account_number = account_number
        self._url_endpoint = f"/accounts/{account_number}/transactions"
        self._transactions: list[Transaction] = []
        self._request_json_data: dict[str, Any] = {}
        self._total_fees_data: dict[str, Any] = {}

    def sync(
        self,
        page_offset: int = 0,
        per_page: int = 250,
        currency: str | None = None,
        sort: SortOrder = SortOrder.DESC,
        sub_type: list[str] | None = None,
        type: str | None = None,
        types: list[str] | None = None,
        action: TransactionAction | None = None,
        end_date: datetime.date | None = None,
        futures_symbol: str | None = None,
        instrument_type: InstrumentType | None = None,
        partition_key: str | None = None,
        start_date: datetime.date | None = None,
        symbol: str | None = None,
        underlying_symbol: str | None = None,
        end_at: datetime.datetime | None = None,
        start_at: datetime.datetime | None = None,
    ) -> None:
        """
        Fetch a paginated list of transactions for the account.

        Args:
            page_offset: Page offset for pagination (default: 0).
            per_page: Number of results per page (default: 250, max: 2000).
            currency: Filter by currency.
            sort: Sort order (default: Desc).
            sub_type: Filter by transaction sub-types (array).
            type: Filter by single transaction type.
            types: Filter by multiple transaction types (array).
            action: Filter by transaction action.
            end_date: End date for filtering (defaults to now).
            futures_symbol: Filter by futures symbol (e.g., '/ESZ9').
            instrument_type: Filter by instrument type.
            partition_key: Account partition key.
            start_date: Start date for filtering.
            symbol: Filter by symbol (stock, option, future).
            underlying_symbol: Filter by underlying symbol.
            end_at: DateTime end range for filtering.
            start_at: DateTime start range for filtering.

        Raises:
            translate_error_code: If the API request fails.
        """
        params: dict[str, Any] = {
            "page-offset": page_offset,
            "per-page": per_page,
            "sort": sort.value,
        }

        if currency:
            params["currency"] = currency

        if sub_type:
            params["sub-type"] = sub_type

        if type:
            params["type"] = type

        if types:
            params["types"] = types

        if action:
            params["action"] = action.value

        if end_date:
            params["end-date"] = end_date.strftime("%Y-%m-%d")

        if futures_symbol:
            params["futures-symbol"] = futures_symbol

        if instrument_type:
            params["instrument-type"] = instrument_type.value

        if partition_key:
            params["partition-key"] = partition_key

        if start_date:
            params["start-date"] = start_date.strftime("%Y-%m-%d")

        if symbol:
            params["symbol"] = symbol

        if underlying_symbol:
            params["underlying-symbol"] = underlying_symbol

        if end_at:
            params["end-at"] = end_at.isoformat()

        if start_at:
            params["start-at"] = start_at.isoformat()

        response = self._session.client.get(self._url_endpoint, params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        # Store raw JSON response
        self._request_json_data = response.json()

        # Parse transactions - API returns: {"data": {"items": [...]}}
        data = self._request_json_data.get("data", {})
        items_data = data.get("items", [])

        self._transactions = [Transaction(item) for item in items_data]

    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        """
        Retrieve a specific transaction by ID.

        Args:
            transaction_id: The ID of the transaction to retrieve.

        Returns:
            Transaction object with the requested data.

        Raises:
            translate_error_code: If the API request fails.
        """
        url = f"{self._url_endpoint}/{transaction_id}"
        response = self._session.client.get(url)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        transaction_data = response.json().get("data", {})
        return Transaction(transaction_data)

    def get_total_fees(self, date: datetime.date | None = None) -> dict[str, Any]:
        """
        Get total fees for the account for a given day.

        Args:
            date: The date to get fees for (defaults to today).

        Returns:
            Dictionary containing total fees data.

        Raises:
            translate_error_code: If the API request fails.
        """
        url = f"{self._url_endpoint}/total-fees"
        params: dict[str, Any] = {}

        if date:
            params["date"] = date.strftime("%Y-%m-%d")

        response = self._session.client.get(url, params=params)

        if response.status_code != 200:
            raise translate_error_code(response.status_code, response.text)

        self._total_fees_data = response.json().get("data", {})
        return self._total_fees_data

    @property
    def transactions(self) -> list[Transaction]:
        """List of transactions returned from the last sync."""
        return self._transactions

    @property
    def account_number(self) -> str:
        """The account number for these transactions."""
        return self._account_number

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON response from the API."""
        return self._request_json_data

    @property
    def total_fees(self) -> dict[str, Any]:
        """Total fees data from the last get_total_fees call."""
        return self._total_fees_data

    def print_summary(self) -> None:
        """Print a plain text summary of all transactions."""
        print(f"\n{'=' * 80}")
        print(
            f"TRANSACTIONS for Account {self._account_number} ({len(self._transactions)} transactions)"
        )
        print(f"{'=' * 80}")

        for transaction in self._transactions:
            transaction.print_summary()

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of all transactions."""
        console = Console()

        # Create summary table
        summary_table = Table(
            title=f"Transactions: Account {self._account_number} ({len(self._transactions)} transactions)",
            show_header=True,
            header_style="bold magenta",
        )
        summary_table.add_column("ID", style="cyan", no_wrap=True)
        summary_table.add_column("Date", style="yellow")
        summary_table.add_column("Action", style="blue")
        summary_table.add_column("Symbol", style="green")
        summary_table.add_column("Quantity", style="white", justify="right")
        summary_table.add_column("Price", style="white", justify="right")
        summary_table.add_column("Net Value", style="white", justify="right")
        summary_table.add_column("Type", style="magenta")

        for transaction in self._transactions:
            summary_table.add_row(
                str(transaction.id),
                (
                    str(transaction.transaction_date)
                    if transaction.transaction_date
                    else "N/A"
                ),
                transaction.action,
                transaction.symbol,
                f"{transaction.quantity:.4f}",
                f"${transaction.price:.2f}",
                f"${transaction.net_value:.2f}",
                transaction.transaction_type,
            )

        console.print(summary_table)

        # Optionally print detailed view for each transaction
        if self._transactions and len(self._transactions) <= 5:
            console.print(
                "\n[bold yellow]Detailed Transaction Information:[/bold yellow]\n"
            )
            for transaction in self._transactions:
                transaction.pretty_print()
                console.print()
