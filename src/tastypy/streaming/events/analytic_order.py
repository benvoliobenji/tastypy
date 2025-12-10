"""Analytic order event definition."""

from .order import OrderEvent
from ...utils.decode_json import parse_json_double


class AnalyticOrderEvent(OrderEvent):
    """
    Represents an extension of Order introducing analytic information,
    e.g. adding to this order iceberg related information (iceberg_peak_size,
    iceberg_hidden_size, iceberg_executed_size).

    The collection of analytic order events of a symbol represents the most
    recent analytic information that is available about orders on the market
    at any given moment of time.
    """

    @property
    def iceberg_peak_size(self) -> float:
        """Iceberg peak size."""
        value = self.get("icebergPeakSize", 0.0)
        return parse_json_double(value)

    @property
    def iceberg_hidden_size(self) -> float:
        """Iceberg hidden size."""
        value = self.get("icebergHiddenSize", 0.0)
        return parse_json_double(value)

    @property
    def iceberg_executed_size(self) -> float:
        """Iceberg executed size."""
        value = self.get("icebergExecutedSize", 0.0)
        return parse_json_double(value)

    @property
    def iceberg_type(self) -> str:
        """Iceberg type."""
        return str(self.get("icebergType", ""))
