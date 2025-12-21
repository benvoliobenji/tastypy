"""Account event type enumeration."""

from enum import Enum


class AccountEventType(str, Enum):
    """Types of account events available for subscription."""

    ORDER = "Order"
    BALANCE = "Balance"
    POSITION = "Position"
    QUOTE_ALERT = "QuoteAlert"
    PUBLIC_WATCHLISTS = "PublicWatchlists"
    COMPLEX_ORDER = "ComplexOrder"

    @staticmethod
    def from_message_type(message_type: str) -> "AccountEventType | None":
        """
        Map API message type to AccountEventType.

        Handles cases where API message type differs from enum value.

        Args:
            message_type: The "type" field from the API message.

        Returns:
            Corresponding AccountEventType or None if unknown.
        """
        type_mapping = {
            "Order": AccountEventType.ORDER,
            "CurrentPosition": AccountEventType.POSITION,
            "TradingStatus": AccountEventType.BALANCE,
            "AccountBalance": AccountEventType.BALANCE,
            "QuoteAlert": AccountEventType.QUOTE_ALERT,
            "PublicWatchlists": AccountEventType.PUBLIC_WATCHLISTS,
            "ComplexOrder": AccountEventType.COMPLEX_ORDER,
        }
        return type_mapping.get(message_type)
