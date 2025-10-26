"""Instrument class for market data module."""

from typing import Any

from tastypy.market_data.enums import ExchangeType, InstrumentType
from tastypy.market_data.instrument_key import InstrumentKey


class Instrument:
    """Dataclass containing information about an instrument."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize instrument from JSON data."""
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

    @property
    def instrument_key(self) -> InstrumentKey | None:
        """Instrument key."""
        data = self._data.get("instrument-key")
        return InstrumentKey(data) if data else None

    @property
    def underlying_instrument(self) -> str:
        """Underlying instrument symbol."""
        return self._data.get("underlying-instrument", "")

    @property
    def root_symbol(self) -> str:
        """Root symbol."""
        return self._data.get("root-symbol", "")

    @property
    def exchange(self) -> ExchangeType:
        """Exchange type."""
        value = self._data.get("exchange", "Unknown")
        try:
            return ExchangeType(value)
        except ValueError:
            return ExchangeType.UNKNOWN
