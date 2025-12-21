"""Representation of public watchlist events in account streaming."""

from .base import AccountEvent
from typing import Any
from ....watchlists.watchlist import Watchlist, WatchlistEntry
from .event_type import AccountEventType


class PublicWatchlistsEvent(AccountEvent):
    """
    Event for public watchlist updates.

    Wraps the existing Watchlist model from the watchlists module.
    """

    def __init__(self, message: dict[str, Any]) -> None:
        """Initialize PublicWatchlistsEvent with watchlist data."""
        super().__init__(AccountEventType.PUBLIC_WATCHLISTS, message)
        self._watchlist = Watchlist(self._data)

    @property
    def watchlist(self) -> Watchlist:
        """Get the full Watchlist object with all properties and methods."""
        return self._watchlist

    # Convenience properties for quick access to common fields
    @property
    def name(self) -> str:
        """Name of the watchlist."""
        return self._watchlist.name

    @property
    def watchlist_entries(self) -> list[WatchlistEntry]:
        """List of watchlist entries."""
        return self._watchlist.watchlist_entries

    def __repr__(self) -> str:
        """String representation."""
        return f"PublicWatchlistsEvent(name={self.name}, entries={len(self.watchlist_entries)})"
