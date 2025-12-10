"""Configuration event definitions."""

from .base import MarketEvent


class ConfigurationEvent(MarketEvent):
    """Configuration event represents configuration changes in the market data stream."""

    @property
    def version(self) -> str:
        """Configuration version."""
        return str(self.get("version", ""))
