"""Order leg representation for margin requirement estimation."""


class MarginRequirementLeg:
    """Represents a single leg of an order for margin requirement estimation.

    Each leg must have a symbol, instrument type, and action. Quantity and
    remaining quantity are optional.
    """

    def __init__(
        self,
        symbol: str,
        instrument_type: str,
        action: str,
        quantity: str | None = None,
        remaining_quantity: str | None = None,
    ):
        """Initialize a margin requirement leg.

        Args:
            symbol: The symbol for this leg (e.g., "AAPL", "SPY 250117C00450000")
            instrument_type: Type of instrument (e.g., "Equity", "Equity Option", "Future")
            action: The action to take (e.g., "Buy to Open", "Sell to Close")
            quantity: Number of contracts/shares (optional)
            remaining_quantity: Remaining quantity for the order (optional)

        Raises:
            ValueError: If required fields are empty
        """
        if not symbol:
            raise ValueError("symbol is required and cannot be empty")
        if not instrument_type:
            raise ValueError("instrument_type is required and cannot be empty")
        if not action:
            raise ValueError("action is required and cannot be empty")

        self._symbol = symbol
        self._instrument_type = instrument_type
        self._action = action
        self._quantity = quantity
        self._remaining_quantity = remaining_quantity

    @property
    def symbol(self) -> str:
        """Get the symbol for this leg."""
        return self._symbol

    @property
    def instrument_type(self) -> str:
        """Get the instrument type."""
        return self._instrument_type

    @property
    def action(self) -> str:
        """Get the action."""
        return self._action

    @property
    def quantity(self) -> str | None:
        """Get the quantity."""
        return self._quantity

    @property
    def remaining_quantity(self) -> str | None:
        """Get the remaining quantity."""
        return self._remaining_quantity

    def to_dict(self) -> dict:
        """Convert the leg to a dictionary for API submission.

        Returns:
            Dictionary with API-formatted keys (kebab-case)
        """
        leg_dict = {
            "symbol": self._symbol,
            "instrument-type": self._instrument_type,
            "action": self._action,
        }

        if self._quantity is not None:
            leg_dict["quantity"] = self._quantity

        if self._remaining_quantity is not None:
            leg_dict["remaining-quantity"] = self._remaining_quantity

        return leg_dict

    def __eq__(self, other) -> bool:
        """Check equality with another leg (for uniqueness validation)."""
        if not isinstance(other, MarginRequirementLeg):
            return False
        return (
            self._symbol == other._symbol
            and self._instrument_type == other._instrument_type
            and self._action == other._action
            and self._quantity == other._quantity
            and self._remaining_quantity == other._remaining_quantity
        )

    def __hash__(self) -> int:
        """Make the leg hashable for uniqueness checking."""
        return hash(
            (
                self._symbol,
                self._instrument_type,
                self._action,
                self._quantity,
                self._remaining_quantity,
            )
        )

    def __repr__(self) -> str:
        """String representation of the leg."""
        return f"MarginRequirementLeg(symbol={self._symbol}, instrument_type={self._instrument_type}, action={self._action})"
