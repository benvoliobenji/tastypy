from .base import AccountEvent
from typing import Any
from .order import OrderEvent
from .position import PositionEvent
from .balance import BalanceEvent
from .quote_alert import QuoteAlertEvent
from .public_watchlists import PublicWatchlistsEvent
from .complex_order import ComplexOrderEvent
from .event_type import AccountEventType


def parse_account_event(message: dict[str, Any]) -> AccountEvent:
    """
    Parse a raw account streamer message into the appropriate event type.

    Args:
        message: Raw message from account streamer.

    Returns:
        Typed event object (OrderEvent, BalanceEvent, etc.).
    """
    message_type = message.get("type", "")

    event_type = AccountEventType.from_message_type(message_type)

    event_classes: dict[AccountEventType, type[AccountEvent]] = {
        AccountEventType.ORDER: OrderEvent,
        AccountEventType.POSITION: PositionEvent,
        AccountEventType.BALANCE: BalanceEvent,
        AccountEventType.QUOTE_ALERT: QuoteAlertEvent,
        AccountEventType.PUBLIC_WATCHLISTS: PublicWatchlistsEvent,
        AccountEventType.COMPLEX_ORDER: ComplexOrderEvent,
    }

    # If we don't recognize the event type, return a generic AccountEvent
    if not event_type:
        return AccountEvent(None, message)

    # Else, map it to the correct class
    event_class = event_classes.get(event_type, AccountEvent)
    return event_class(event_type, message)


def parse_account_events(messages: list[dict[str, Any]]) -> list[AccountEvent]:
    """
    Parse a list of raw account streamer messages into the appropriate event types.

    Args:
        messages: List of raw messages from account streamer.

    Returns:
        List of typed event objects (OrderEvent, BalanceEvent, etc.).
    """
    return [parse_account_event(message) for message in messages]
