"""Series event definitions."""

from .base import MarketEvent


class SeriesEvent(MarketEvent):
    """Series event is a snapshot of computed values that are available
    for all option series for a given underlying symbol based on the
    option prices on the market.

    It represents the most recent information that is available about
    the corresponding values on the market at any given moment of time.
    """

    pass
