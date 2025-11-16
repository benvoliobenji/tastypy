"""Order leg and fill data models."""

import datetime
from typing import Any

from tastypy.utils.decode_json import parse_datetime, parse_float

from .enums import InstrumentType, OrderAction


class OrderFill:
    """Represents a single fill for an order leg."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize OrderFill from JSON data."""
        self._json = json_data

    @property
    def destination_venue(self) -> str:
        """The destination venue for the fill."""
        return self._json.get("destination-venue", "")

    @property
    def ext_exec_id(self) -> str:
        """External execution ID."""
        return self._json.get("ext-exec-id", "")

    @property
    def ext_group_fill_id(self) -> str:
        """External group fill ID."""
        return self._json.get("ext-group-fill-id", "")

    @property
    def fill_id(self) -> str:
        """The fill ID."""
        return self._json.get("fill-id", "")

    @property
    def fill_price(self) -> float:
        """The price at which the fill occurred."""
        return parse_float(self._json.get("fill-price"), 0.0)

    @property
    def filled_at(self) -> datetime.datetime | None:
        """The timestamp when the fill occurred."""
        return parse_datetime(self._json.get("filled-at"))

    @property
    def quantity(self) -> str:
        """The quantity filled."""
        return self._json.get("quantity", "")


class OrderLeg:
    """Represents a single leg of an order."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize OrderLeg from JSON data."""
        self._json = json_data
        self._fills: list[OrderFill] = []

        # Parse fills if present
        fills_data = self._json.get("fills", [])
        if fills_data:
            self._fills = [OrderFill(fill) for fill in fills_data]

    @property
    def action(self) -> OrderAction | None:
        """The directional action of the leg."""
        value = self._json.get("action")
        if value:
            try:
                return OrderAction(value)
            except ValueError:
                return None
        return None

    @property
    def instrument_type(self) -> InstrumentType | None:
        """The type of instrument."""
        value = self._json.get("instrument-type")
        if value:
            try:
                return InstrumentType(value)
            except ValueError:
                return None
        return None

    @property
    def quantity(self) -> str:
        """The size of the contract."""
        return self._json.get("quantity", "")

    @property
    def remaining_quantity(self) -> str:
        """The remaining quantity to be filled."""
        return self._json.get("remaining-quantity", "")

    @property
    def symbol(self) -> str:
        """The symbol for the leg."""
        return self._json.get("symbol", "")

    @property
    def fills(self) -> list[OrderFill]:
        """The fills for this leg."""
        return self._fills
