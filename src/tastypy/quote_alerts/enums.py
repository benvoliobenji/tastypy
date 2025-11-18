"""Enums for quote alerts module."""

import enum


class FieldType(str, enum.Enum):
    """Quote alert field types that can be monitored."""

    LAST = "Last"
    BID = "Bid"
    ASK = "Ask"
    IV = "IV"

    def __str__(self) -> str:
        return self.value


class OperatorType(str, enum.Enum):
    """Quote alert comparison operators."""

    GREATER_THAN = ">"
    LESS_THAN = "<"

    def __str__(self) -> str:
        return self.value
