"""Watchlist entry data model."""

from typing import Any

from tastypy.watchlists.enums import InstrumentType


class WatchlistEntry:
    """Represents a single entry (instrument) in a watchlist."""

    def __init__(self, entry_json: dict[str, Any]) -> None:
        """
        Initialize a watchlist entry from JSON data.

        Args:
            entry_json: Dictionary containing watchlist entry data from API.
        """
        self._json = entry_json

    @property
    def symbol(self) -> str:
        """Symbol of the instrument."""
        return self._json.get("symbol", "")

    @property
    def instrument_type(self) -> str:
        """Type of instrument as string."""
        return self._json.get("instrument-type", "")

    @property
    def instrument_type_enum(self) -> InstrumentType | None:
        """Type of instrument as enum."""
        try:
            return InstrumentType(self.instrument_type)
        except (ValueError, KeyError):
            return None

    @property
    def raw_json(self) -> dict[str, Any]:
        """Raw JSON data for this entry."""
        return self._json

    def to_dict(self) -> dict[str, str]:
        """
        Convert entry to dictionary for API requests.

        Returns:
            Dictionary with symbol and optional instrument-type.
        """
        result: dict[str, str] = {"symbol": self.symbol}
        if self.instrument_type:
            result["instrument-type"] = self.instrument_type
        return result

    def print_summary(self) -> None:
        """Print a plain text summary of the entry."""
        print(f"  Symbol: {self.symbol}")
        if self.instrument_type:
            print(f"    Type: {self.instrument_type}")
