"""InstrumentKey class for market data module."""

from typing import Any

from tastypy.market_data.enums import InstrumentType


class InstrumentKey:
    """Dataclass containing an instrument key."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize instrument key from JSON data."""
        self._data = data

    @property
    def symbol(self) -> str:
        """Symbol for the instrument."""
        return self._data.get("symbol", "")

    @property
    def instrument_type(self) -> InstrumentType:
        """Type of instrument."""
        value = self._data.get("instrument-type", "")
        return InstrumentType(value) if value else InstrumentType.EQUITY
