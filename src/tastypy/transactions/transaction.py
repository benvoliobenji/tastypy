"""Transaction data model."""

import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from tastypy.transactions.lot import Lot
from tastypy.utils.decode_json import parse_datetime, parse_float, parse_int, parse_date


class Transaction:
    """Represents a single transaction."""

    def __init__(self, transaction_json: dict[str, Any]) -> None:
        """
        Initialize a transaction object from JSON data.

        Args:
            transaction_json: Dictionary containing transaction data from API.
        """
        self._json = transaction_json
        self._lots: list[Lot] = []

        # Parse lots if present
        lots_data = self._json.get("lots", [])
        if isinstance(lots_data, list):
            self._lots = [Lot(lot) for lot in lots_data]
        elif isinstance(lots_data, dict):
            # Single lot returned as object
            self._lots = [Lot(lots_data)]

    @property
    def id(self) -> int:
        """Transaction ID."""
        return parse_int(self._json.get("id"))

    @property
    def account_number(self) -> str:
        """Account number."""
        return self._json.get("account-number", "")

    @property
    def action(self) -> str:
        """Transaction action (Buy, Sell, etc.)."""
        return self._json.get("action", "")

    @property
    def agency_price(self) -> float:
        """Agency price."""
        return parse_float(self._json.get("agency-price"))

    @property
    def clearing_fees(self) -> float:
        """Clearing fees."""
        return parse_float(self._json.get("clearing-fees"))

    @property
    def clearing_fees_effect(self) -> str:
        """Effect of clearing fees (Credit/Debit)."""
        return self._json.get("clearing-fees-effect", "")

    @property
    def commission(self) -> float:
        """Commission charged."""
        return parse_float(self._json.get("commission"))

    @property
    def commission_effect(self) -> str:
        """Effect of commission (Credit/Debit)."""
        return self._json.get("commission-effect", "")

    @property
    def lots(self) -> list[Lot]:
        """List of lots in this transaction."""
        return self._lots

    @property
    def cost_basis_reconciliation_date(self) -> datetime.date | None:
        """Cost basis reconciliation date."""
        return parse_date(self._json.get("cost-basis-reconciliation-date"))

    @property
    def currency(self) -> str:
        """Currency of the transaction."""
        return self._json.get("currency", "")

    @property
    def currency_conversion_fees(self) -> float:
        """Currency conversion fees."""
        return parse_float(self._json.get("currency-conversion-fees"))

    @property
    def currency_conversion_fees_effect(self) -> str:
        """Effect of currency conversion fees."""
        return self._json.get("currency-conversion-fees-effect", "")

    @property
    def description(self) -> str:
        """Transaction description."""
        return self._json.get("description", "")

    @property
    def destination_venue(self) -> str:
        """Destination venue."""
        return self._json.get("destination-venue", "")

    @property
    def exchange(self) -> str:
        """Exchange."""
        return self._json.get("exchange", "")

    @property
    def exchange_affiliation_identifier(self) -> str:
        """Exchange affiliation identifier."""
        return self._json.get("exchange-affiliation-identifier", "")

    @property
    def exec_id(self) -> str:
        """Execution ID."""
        return self._json.get("exec-id", "")

    @property
    def executed_at(self) -> datetime.datetime | None:
        """When the transaction was executed."""
        return parse_datetime(self._json.get("executed-at"))

    @property
    def ext_exchange_order_number(self) -> str:
        """External exchange order number."""
        return self._json.get("ext-exchange-order-number", "")

    @property
    def ext_exec_id(self) -> str:
        """External execution ID."""
        return self._json.get("ext-exec-id", "")

    @property
    def ext_global_order_number(self) -> int:
        """External global order number."""
        return parse_int(self._json.get("ext-global-order-number"))

    @property
    def ext_group_fill_id(self) -> str:
        """External group fill ID."""
        return self._json.get("ext-group-fill-id", "")

    @property
    def ext_group_id(self) -> str:
        """External group ID."""
        return self._json.get("ext-group-id", "")

    @property
    def instrument_type(self) -> str:
        """Type of instrument."""
        return self._json.get("instrument-type", "")

    @property
    def is_estimated_fee(self) -> bool:
        """Whether the fee is estimated."""
        return self._json.get("is-estimated-fee", False)

    @property
    def leg_count(self) -> int:
        """Number of legs in the transaction."""
        return parse_int(self._json.get("leg-count"))

    @property
    def net_value(self) -> float:
        """Net value of the transaction."""
        return parse_float(self._json.get("net-value"))

    @property
    def net_value_effect(self) -> str:
        """Effect of net value."""
        return self._json.get("net-value-effect", "")

    @property
    def order_id(self) -> int:
        """Order ID."""
        return parse_int(self._json.get("order-id"))

    @property
    def other_charge(self) -> float:
        """Other charges."""
        return parse_float(self._json.get("other-charge"))

    @property
    def other_charge_description(self) -> str:
        """Description of other charges."""
        return self._json.get("other-charge-description", "")

    @property
    def other_charge_effect(self) -> str:
        """Effect of other charges."""
        return self._json.get("other-charge-effect", "")

    @property
    def price(self) -> float:
        """Transaction price."""
        return parse_float(self._json.get("price"))

    @property
    def principal_price(self) -> float:
        """Principal price."""
        return parse_float(self._json.get("principal-price"))

    @property
    def proprietary_index_option_fees(self) -> float:
        """Proprietary index option fees."""
        return parse_float(self._json.get("proprietary-index-option-fees"))

    @property
    def proprietary_index_option_fees_effect(self) -> str:
        """Effect of proprietary index option fees."""
        return self._json.get("proprietary-index-option-fees-effect", "")

    @property
    def quantity(self) -> float:
        """Quantity traded."""
        return parse_float(self._json.get("quantity"))

    @property
    def regulatory_fees(self) -> float:
        """Regulatory fees."""
        return parse_float(self._json.get("regulatory-fees"))

    @property
    def regulatory_fees_effect(self) -> str:
        """Effect of regulatory fees."""
        return self._json.get("regulatory-fees-effect", "")

    @property
    def reverses_id(self) -> int:
        """ID of transaction this reverses."""
        return parse_int(self._json.get("reverses-id"))

    @property
    def symbol(self) -> str:
        """Symbol traded."""
        return self._json.get("symbol", "")

    @property
    def transaction_date(self) -> datetime.date | None:
        """Date of the transaction."""
        return parse_date(self._json.get("transaction-date"))

    @property
    def transaction_sub_type(self) -> str:
        """Transaction sub-type."""
        return self._json.get("transaction-sub-type", "")

    @property
    def transaction_type(self) -> str:
        """Transaction type."""
        return self._json.get("transaction-type", "")

    @property
    def underlying_symbol(self) -> str:
        """Underlying symbol."""
        return self._json.get("underlying-symbol", "")

    @property
    def value(self) -> float:
        """Transaction value."""
        return parse_float(self._json.get("value"))

    @property
    def value_effect(self) -> str:
        """Effect of value."""
        return self._json.get("value-effect", "")

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data from the API."""
        return self._json

    def print_summary(self) -> None:
        """Print a plain text summary of the transaction."""
        print(f"\nTransaction ID: {self.id}")
        print(f"  Account: {self.account_number}")
        print(f"  Action: {self.action}")
        print(f"  Symbol: {self.symbol}")
        print(f"  Underlying: {self.underlying_symbol}")
        print(f"  Instrument Type: {self.instrument_type}")
        print(f"  Quantity: {self.quantity}")
        print(f"  Price: ${self.price:.2f}")
        print(f"  Value: ${self.value:.2f} ({self.value_effect})")
        print(f"  Net Value: ${self.net_value:.2f} ({self.net_value_effect})")
        print(f"  Commission: ${self.commission:.2f} ({self.commission_effect})")
        print(f"  Executed At: {self.executed_at}")
        print(f"  Transaction Date: {self.transaction_date}")
        print(f"  Transaction Type: {self.transaction_type}")
        print(f"  Transaction Sub-Type: {self.transaction_sub_type}")
        print(f"  Description: {self.description}")

        if self.lots:
            print(f"  Lots ({len(self.lots)}):")
            for lot in self.lots:
                lot.print_summary()

    def pretty_print(self) -> None:
        """Print a rich formatted output of the transaction."""
        console = Console()

        # Main transaction info
        table = Table(
            title=f"Transaction {self.id} - {self.symbol}",
            show_header=True,
            header_style="bold blue",
        )
        table.add_column("Field", style="cyan", no_wrap=True, width=30)
        table.add_column("Value", style="green")

        # Basic info
        table.add_row("Transaction ID", str(self.id))
        table.add_row("Account Number", self.account_number)
        table.add_row("Action", self.action)
        table.add_row("Symbol", self.symbol)
        table.add_row("Underlying Symbol", self.underlying_symbol or "N/A")
        table.add_row("Instrument Type", self.instrument_type)

        # Quantities and prices
        table.add_row("Quantity", f"{self.quantity:.4f}")
        table.add_row("Price", f"${self.price:.2f}")
        table.add_row(
            "Agency Price", f"${self.agency_price:.2f}" if self.agency_price else "N/A"
        )
        table.add_row(
            "Principal Price",
            f"${self.principal_price:.2f}" if self.principal_price else "N/A",
        )

        # Values
        table.add_row("Value", f"${self.value:.2f} ({self.value_effect})")
        table.add_row("Net Value", f"${self.net_value:.2f} ({self.net_value_effect})")

        # Fees
        table.add_row(
            "Commission",
            (
                f"${self.commission:.2f} ({self.commission_effect})"
                if self.commission
                else "N/A"
            ),
        )
        table.add_row(
            "Clearing Fees",
            (
                f"${self.clearing_fees:.2f} ({self.clearing_fees_effect})"
                if self.clearing_fees
                else "N/A"
            ),
        )
        table.add_row(
            "Regulatory Fees",
            (
                f"${self.regulatory_fees:.2f} ({self.regulatory_fees_effect})"
                if self.regulatory_fees
                else "N/A"
            ),
        )
        table.add_row(
            "Other Charges",
            (
                f"${self.other_charge:.2f} ({self.other_charge_effect})"
                if self.other_charge
                else "N/A"
            ),
        )
        table.add_row("Is Estimated Fee", "Yes" if self.is_estimated_fee else "No")

        # Dates and times
        table.add_row(
            "Executed At", str(self.executed_at) if self.executed_at else "N/A"
        )
        table.add_row(
            "Transaction Date",
            str(self.transaction_date) if self.transaction_date else "N/A",
        )

        # Transaction details
        table.add_row("Transaction Type", self.transaction_type)
        table.add_row("Transaction Sub-Type", self.transaction_sub_type or "N/A")
        table.add_row("Description", self.description)
        table.add_row("Order ID", str(self.order_id) if self.order_id else "N/A")
        table.add_row("Leg Count", str(self.leg_count) if self.leg_count else "N/A")

        # Exchange info
        table.add_row("Exchange", self.exchange or "N/A")
        table.add_row("Destination Venue", self.destination_venue or "N/A")

        # IDs
        table.add_row("Exec ID", self.exec_id or "N/A")
        table.add_row("Ext Exec ID", self.ext_exec_id or "N/A")
        table.add_row("Ext Group ID", self.ext_group_id or "N/A")
        table.add_row(
            "Reverses ID", str(self.reverses_id) if self.reverses_id else "N/A"
        )

        console.print(table)

        # Print lots if any
        if self.lots:
            console.print(f"\n[bold yellow]Lots ({len(self.lots)}):[/bold yellow]")
            for lot in self.lots:
                lot.pretty_print()
