"""Shared types and enums for margin requirements."""

import enum


class PriceEffect(enum.Enum):
    """Enumeration of price effects for orders."""

    CREDIT = "Credit"
    DEBIT = "Debit"

    def __str__(self):
        return self.value


def parse_price_effect(value: str | None) -> PriceEffect | None:
    """Parse a price effect string from API response.

    Args:
        value: String value from API (e.g., "Credit", "Debit", "None", or None)

    Returns:
        PriceEffect enum or None if value is empty, "None", or invalid
    """
    if value and value != "None":
        try:
            return PriceEffect(value)
        except ValueError:
            return None
    return None
