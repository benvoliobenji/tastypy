"""Parse market events from raw data."""

from typing import Any

from ..enums import EventType
from .analytic_order import AnalyticOrderEvent
from .base import MarketEvent
from .candle import CandleEvent
from .configuration import ConfigurationEvent
from .greeks import GreeksEvent
from .message import MessageEvent
from .option_sale import OptionSaleEvent
from .order import OrderEvent
from .profile import ProfileEvent
from .quote import QuoteEvent
from .series import SeriesEvent
from .spread_order import SpreadOrderEvent
from .summary import SummaryEvent
from .theoretical_price import TheoreticalPriceEvent
from .time_and_sale import TimeAndSaleEvent
from .trade import TradeETHEvent, TradeEvent
from .underlying import UnderlyingEvent

# Event type to class mapping
EVENT_TYPE_MAP: dict[str, type[MarketEvent]] = {
    EventType.QUOTE.value: QuoteEvent,
    EventType.TRADE.value: TradeEvent,
    EventType.TRADE_ETH.value: TradeETHEvent,
    EventType.PROFILE.value: ProfileEvent,
    EventType.SUMMARY.value: SummaryEvent,
    EventType.GREEKS.value: GreeksEvent,
    EventType.THEO_PRICE.value: TheoreticalPriceEvent,
    EventType.UNDERLYING.value: UnderlyingEvent,
    EventType.CANDLE.value: CandleEvent,
    EventType.TIME_AND_SALE.value: TimeAndSaleEvent,
    EventType.ORDER.value: OrderEvent,
    EventType.SPREAD_ORDER.value: SpreadOrderEvent,
    EventType.ANALYTIC_ORDER.value: AnalyticOrderEvent,
    EventType.SERIES.value: SeriesEvent,
    EventType.OPTION_SALE.value: OptionSaleEvent,
    EventType.CONFIGURATION.value: ConfigurationEvent,
    EventType.MESSAGE.value: MessageEvent,
}


def parse_event(
    data: dict[str, Any] | list[Any], fields: list[str] | None = None
) -> MarketEvent:
    """
    Parse raw event data into the appropriate MarketEvent subclass.

    Args:
        data: Event data (dict for FULL format, list for COMPACT format).
        fields: Field names for COMPACT format (required if data is a list).

    Returns:
        Appropriate MarketEvent subclass instance based on eventType.

    Raises:
        ValueError: If event type is unknown or data format is invalid.

    Example:
        >>> # FULL format
        >>> event_data = {"eventType": "Quote", "eventSymbol": "AAPL", "bidPrice": 150.0}
        >>> event = parse_event(event_data)
        >>> isinstance(event, QuoteEvent)
        True

        >>> # COMPACT format
        >>> event_data = ["Quote", "AAPL", 150.0, 151.0]
        >>> fields = ["eventType", "eventSymbol", "bidPrice", "askPrice"]
        >>> event = parse_event(event_data, fields)
        >>> isinstance(event, QuoteEvent)
        True
    """
    # Determine event type
    if isinstance(data, dict):
        event_type = data.get("eventType")
    elif isinstance(data, list) and fields:
        # COMPACT format: eventType is usually the first field
        try:
            event_type_index = fields.index("eventType")
            event_type = (
                data[event_type_index] if event_type_index < len(data) else None
            )
        except (ValueError, IndexError):
            event_type = None
    else:
        raise ValueError(
            "Invalid data format: data must be dict or list with fields parameter"
        )

    if not event_type:
        raise ValueError("Event type not found in data")

    # Get appropriate event class
    event_class = EVENT_TYPE_MAP.get(str(event_type))

    if event_class is None:
        # Return base MarketEvent for unknown event types
        return MarketEvent(data, fields)

    return event_class(data, fields)


def parse_events(
    events_data: list[dict[str, Any] | list[Any]], fields: list[str] | None = None
) -> list[MarketEvent]:
    """
    Parse multiple events from a list of raw event data.

    Args:
        events_data: List of event data (dicts for FULL format, lists for COMPACT format).
        fields: Field names for COMPACT format (required if events_data contains lists).

    Returns:
        List of parsed MarketEvent instances.

    Example:
        >>> events_data = [
        ...     {"eventType": "Quote", "eventSymbol": "AAPL", "bidPrice": 150.0},
        ...     {"eventType": "Trade", "eventSymbol": "AAPL", "price": 150.5}
        ... ]
        >>> events = parse_events(events_data)
        >>> len(events)
        2
        >>> isinstance(events[0], QuoteEvent)
        True
        >>> isinstance(events[1], TradeEvent)
        True
    """
    return [parse_event(event_data, fields) for event_data in events_data]
