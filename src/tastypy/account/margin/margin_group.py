"""Margin requirement group for underlying symbols."""

from .margin_types import PriceEffect, parse_price_effect
from ...utils.decode_json import parse_float


class MarginRequirementGroup:
    """Represents a margin requirement group for an underlying symbol.

    Groups contain detailed margin calculations for specific positions,
    including expected price ranges and nested position entries.
    """

    def __init__(self, group_data: dict):
        """Initialize a margin requirement group from API data.

        Args:
            group_data: Dictionary containing group data from the API
        """
        self._group_data = group_data

    @property
    def description(self) -> str:
        """Get the group description."""
        return self._group_data.get("description", "")

    @property
    def code(self) -> str:
        """Get the group code."""
        return self._group_data.get("code", "")

    @property
    def underlying_symbol(self) -> str:
        """Get the underlying symbol."""
        return self._group_data.get("underlying-symbol", "")

    @property
    def underlying_type(self) -> str:
        """Get the underlying type (e.g., 'Equity', 'Future')."""
        return self._group_data.get("underlying-type", "")

    @property
    def expected_price_range_up_percent(self) -> float:
        """Get the expected price range up percent."""
        return parse_float(self._group_data.get("expected-price-range-up-percent"))

    @property
    def expected_price_range_down_percent(self) -> float:
        """Get the expected price range down percent."""
        return parse_float(self._group_data.get("expected-price-range-down-percent"))

    @property
    def point_of_no_return_percent(self) -> float:
        """Get the point of no return percent."""
        return parse_float(self._group_data.get("point-of-no-return-percent"))

    @property
    def margin_calculation_type(self) -> str:
        """Get the margin calculation type."""
        return self._group_data.get("margin-calculation-type", "")

    @property
    def margin_requirement(self) -> float:
        """Get the margin requirement amount."""
        return parse_float(self._group_data.get("margin-requirement"))

    @property
    def margin_requirement_effect(self) -> PriceEffect | None:
        """Get the margin requirement effect (Debit/Credit)."""
        return parse_price_effect(self._group_data.get("margin-requirement-effect"))

    @property
    def initial_requirement(self) -> float:
        """Get the initial requirement amount."""
        return parse_float(self._group_data.get("initial-requirement"))

    @property
    def initial_requirement_effect(self) -> PriceEffect | None:
        """Get the initial requirement effect (Debit/Credit)."""
        return parse_price_effect(self._group_data.get("initial-requirement-effect"))

    @property
    def maintenance_requirement(self) -> float:
        """Get the maintenance requirement amount."""
        return parse_float(self._group_data.get("maintenance-requirement"))

    @property
    def maintenance_requirement_effect(self) -> PriceEffect | None:
        """Get the maintenance requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._group_data.get("maintenance-requirement-effect")
        )

    @property
    def buying_power(self) -> float:
        """Get the buying power amount."""
        return parse_float(self._group_data.get("buying-power"))

    @property
    def buying_power_effect(self) -> PriceEffect | None:
        """Get the buying power effect (Debit/Credit)."""
        return parse_price_effect(self._group_data.get("buying-power-effect"))

    @property
    def nested_groups(self) -> list:
        """Get nested groups (e.g., LONG_UNDERLYING, SHORT_CALL, etc.)."""
        return self._group_data.get("groups", [])

    @property
    def price_increase_percent(self) -> float:
        """Get the price increase percent."""
        return parse_float(self._group_data.get("price-increase-percent"))

    @property
    def price_decrease_percent(self) -> float:
        """Get the price decrease percent."""
        return parse_float(self._group_data.get("price-decrease-percent"))

    @property
    def has_elevated_earnings_requirements(self) -> bool:
        """Check if the group has elevated earnings requirements."""
        return bool(self._group_data.get("has-elevated-earnings-requirements", False))

    def __repr__(self) -> str:
        """String representation of the group."""
        return f"MarginRequirementGroup(symbol={self.underlying_symbol}, type={self.margin_calculation_type}, requirement=${self.margin_requirement:,.2f})"
