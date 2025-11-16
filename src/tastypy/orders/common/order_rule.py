"""Order rule and condition data models."""

import datetime
from typing import Any

from tastypy.utils.decode_json import parse_datetime, parse_float

from .enums import (
    InstrumentType,
    QuantityDirection,
    RuleAction,
    RuleComparator,
    RuleIndicator,
)


class PriceComponent:
    """Represents a price component in an order condition."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize PriceComponent from JSON data."""
        self._json = json_data

    @property
    def instrument_type(self) -> InstrumentType | None:
        """The instrument's type in relation to the symbol."""
        value = self._json.get("instrument-type")
        if value:
            try:
                return InstrumentType(value)
            except ValueError:
                return None
        return None

    @property
    def quantity(self) -> str:
        """The ratio quantity in relation to the symbol."""
        return self._json.get("quantity", "")

    @property
    def quantity_direction(self) -> QuantityDirection | None:
        """The quantity direction (Long or Short) in relation to the symbol."""
        value = self._json.get("quantity-direction")
        if value:
            try:
                return QuantityDirection(value)
            except ValueError:
                return None
        return None

    @property
    def symbol(self) -> str:
        """The symbol to apply the condition to."""
        return self._json.get("symbol", "")


class OrderCondition:
    """Represents a condition in an order rule."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize OrderCondition from JSON data."""
        self._json = json_data
        self._price_components: list[PriceComponent] = []

        # Parse price components if present
        price_comp_data = self._json.get("price-components", [])
        if price_comp_data:
            self._price_components = [PriceComponent(pc) for pc in price_comp_data]

    @property
    def id(self) -> str:
        """The condition ID."""
        return self._json.get("id", "")

    @property
    def action(self) -> RuleAction | None:
        """The action in which the trigger is enacted."""
        value = self._json.get("action")
        if value:
            try:
                return RuleAction(value)
            except ValueError:
                return None
        return None

    @property
    def comparator(self) -> RuleComparator | None:
        """How to compare against the threshold."""
        value = self._json.get("comparator")
        if value:
            try:
                return RuleComparator(value)
            except ValueError:
                return None
        return None

    @property
    def indicator(self) -> RuleIndicator | None:
        """The indicator for the trigger."""
        value = self._json.get("indicator")
        if value:
            try:
                return RuleIndicator(value)
            except ValueError:
                return None
        return None

    @property
    def instrument_type(self) -> InstrumentType | None:
        """The instrument's type in relation to the condition."""
        value = self._json.get("instrument-type")
        if value:
            try:
                return InstrumentType(value)
            except ValueError:
                return None
        return None

    @property
    def is_threshold_based_on_notional(self) -> bool:
        """If comparison is based on notional value."""
        return bool(self._json.get("is-threshold-based-on-notional", False))

    @property
    def symbol(self) -> str:
        """The symbol to apply the condition to."""
        return self._json.get("symbol", "")

    @property
    def threshold(self) -> float:
        """The price at which the condition triggers."""
        return parse_float(self._json.get("threshold"), 0.0)

    @property
    def triggered_at(self) -> datetime.datetime | None:
        """When the condition was triggered."""
        return parse_datetime(self._json.get("triggered-at"))

    @property
    def triggered_value(self) -> float:
        """The value when the condition was triggered."""
        return parse_float(self._json.get("triggered-value"), 0.0)

    @property
    def price_components(self) -> list[PriceComponent]:
        """The price components for this condition."""
        return self._price_components


class OrderRule:
    """Represents order rules and conditions."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize OrderRule from JSON data."""
        self._json = json_data
        self._order_conditions: list[OrderCondition] = []

        # Parse order conditions if present
        conditions_data = self._json.get("order-conditions", [])
        if conditions_data:
            self._order_conditions = [OrderCondition(cond) for cond in conditions_data]

    @property
    def cancel_at(self) -> datetime.datetime | None:
        """Latest time an order should be canceled at."""
        return parse_datetime(self._json.get("cancel-at"))

    @property
    def cancelled_at(self) -> datetime.datetime | None:
        """When the order was cancelled."""
        return parse_datetime(self._json.get("cancelled-at"))

    @property
    def route_after(self) -> datetime.datetime | None:
        """Earliest time an order should route at."""
        return parse_datetime(self._json.get("route-after"))

    @property
    def routed_at(self) -> datetime.datetime | None:
        """When the order was routed."""
        return parse_datetime(self._json.get("routed-at"))

    @property
    def order_conditions(self) -> list[OrderCondition]:
        """The conditions for this rule."""
        return self._order_conditions
