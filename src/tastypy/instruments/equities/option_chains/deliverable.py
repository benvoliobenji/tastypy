"""
Deliverable class for equity option chains.

Represents what is delivered when an option is exercised, which may include
cash, equity shares, or other instruments. Most standard equity options deliver
100 shares of the underlying, but non-standard options may have different deliverables.
"""

from typing import Any


class Deliverable:
    """
    Represents a deliverable for an option contract.

    When an option is exercised, the contract may deliver various assets.
    Standard equity options typically deliver shares of the underlying stock,
    but adjusted options may deliver cash, multiple securities, or other instruments.
    """

    def __init__(self, deliverable_json: dict[str, Any]):
        """
        Initialize a Deliverable from JSON data.

        Args:
            deliverable_json: The JSON data representing the deliverable.
        """
        self._deliverable_json = deliverable_json

    @property
    def id(self) -> int:
        """Get the unique identifier for this deliverable."""
        value = self._deliverable_json.get("id", 0)
        return int(value) if value is not None else 0

    @property
    def amount(self) -> float:
        """Get the amount/quantity of the deliverable."""
        value = self._deliverable_json.get("amount", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def deliverable_type(self) -> str:
        """Get the type of deliverable (e.g., 'Equity', 'Cash')."""
        return self._deliverable_json.get("deliverable-type", "")

    @property
    def description(self) -> str:
        """Get the description of the deliverable."""
        return self._deliverable_json.get("description", "")

    @property
    def instrument_type(self) -> str:
        """Get the instrument type of the deliverable."""
        return self._deliverable_json.get("instrument-type", "")

    @property
    def percent(self) -> str:
        """Get the percentage representation of the deliverable."""
        return self._deliverable_json.get("percent", "")

    @property
    def root_symbol(self) -> str:
        """Get the root symbol for the deliverable."""
        return self._deliverable_json.get("root-symbol", "")

    @property
    def symbol(self) -> str:
        """Get the symbol of the deliverable."""
        return self._deliverable_json.get("symbol", "")

    def __str__(self) -> str:
        return f"Deliverable: {self.symbol} ({self.amount} {self.deliverable_type})"

    def print_summary(self) -> None:
        """Print a simple text summary of the deliverable information."""
        print(f"  Deliverable ID: {self.id}")
        print(f"  Symbol: {self.symbol}")
        print(f"  Type: {self.deliverable_type}")
        print(f"  Amount: {self.amount}")
        print(f"  Instrument Type: {self.instrument_type}")
        if self.description:
            print(f"  Description: {self.description}")
        if self.percent:
            print(f"  Percent: {self.percent}")
        if self.root_symbol:
            print(f"  Root Symbol: {self.root_symbol}")
