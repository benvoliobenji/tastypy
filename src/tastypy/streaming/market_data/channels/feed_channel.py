"""Feed channel for streaming specifically FEED market data."""

import asyncio
import logging
from typing import Any, Callable

from ..enums import (
    EventType,
    FeedContract,
    FeedDataFormat,
    MessageType,
    ServiceType,
)
from ..events import MarketEvent, parse_event
from ..messages import (
    ChannelCancelMessage,
    ChannelOpenedMessage,
    ChannelRequestMessage,
    FeedConfigMessage,
    FeedDataMessage,
    FeedSetupMessage,
    FeedSubscriptionMessage,
    Message,
)
from .subscription import Subscription

logger = logging.getLogger(__name__)


class FeedChannel:
    """
    Manages a FEED service channel for streaming market data.

    A channel is a virtual connection for subscribing to market events.
    Each channel can have multiple subscriptions to different symbols and event types.
    """

    def __init__(
        self,
        channel_id: int,
        connection: Any,  # DXLinkConnection type
        contract: FeedContract = FeedContract.AUTO,
    ) -> None:
        """
        Initialize a feed channel.

        Args:
            channel_id: The channel ID (must be > 0).
            connection: The DXLink connection to use.
            contract: The feed contract type (TICKER, STREAM, HISTORY, AUTO).
        """
        if channel_id <= 0:
            raise ValueError("Channel ID must be greater than 0")

        self.channel_id = channel_id
        self.connection = connection
        self.contract = contract

        self._is_open = False
        self._is_configured = False
        self._subscriptions: dict[tuple[str, EventType], Subscription] = {}
        self._event_handlers: list[Callable[[MarketEvent], None]] = []
        self._event_fields: dict[str, list[str]] = {}

        # Register message handlers
        self.connection.register_handler(
            MessageType.CHANNEL_OPENED, self._handle_channel_opened
        )
        self.connection.register_handler(
            MessageType.CHANNEL_CLOSED, self._handle_channel_closed
        )
        self.connection.register_handler(
            MessageType.FEED_CONFIG, self._handle_feed_config
        )
        self.connection.register_handler(MessageType.FEED_DATA, self._handle_feed_data)

    @property
    def is_open(self) -> bool:
        """Check if the channel is open."""
        return self._is_open

    async def open(self) -> None:
        """
        Open the channel.

        Sends a CHANNEL_REQUEST message to the server and waits for confirmation.
        """
        if self._is_open:
            logger.warning(f"Channel {self.channel_id} is already open")
            return

        logger.info(f"Opening channel {self.channel_id}")
        request_msg = ChannelRequestMessage(
            self.channel_id,
            ServiceType.FEED,
            {"contract": self.contract.value},
        )
        await self.connection.send_message(request_msg)

        # Wait for channel to be opened (with timeout)
        max_wait = 10  # seconds
        wait_interval = 0.1
        elapsed = 0.0
        while not self._is_open and elapsed < max_wait:
            await asyncio.sleep(wait_interval)
            elapsed += wait_interval

        if not self._is_open:
            raise TimeoutError(
                f"Channel {self.channel_id} failed to open within {max_wait}s"
            )

    async def close(self) -> None:
        """
        Close the channel.

        Sends a CHANNEL_CANCEL message to the server.
        """
        if not self._is_open:
            logger.warning(f"Channel {self.channel_id} is not open")
            return

        logger.info(f"Closing channel {self.channel_id}")
        cancel_msg = ChannelCancelMessage(self.channel_id)
        await self.connection.send_message(cancel_msg)
        self._is_open = False

    async def configure(
        self,
        event_fields: dict[str, list[str]] | None = None,
        aggregation_period: float | None = None,
    ) -> None:
        """
        Configure the feed channel.

        Args:
            event_fields: Map of event types to field names to receive.
            aggregation_period: Aggregation period in seconds.
        """
        if not self._is_open:
            raise RuntimeError(
                f"Channel {self.channel_id} must be opened before configuring"
            )

        logger.info(f"Configuring channel {self.channel_id}")

        # Use default fields if none provided
        if event_fields is None:
            event_fields = self._get_default_event_fields()

        # Don't clear event_fields during reconfiguration - keep old ones until new config arrives
        # self._event_fields = event_fields

        setup_msg = FeedSetupMessage(
            self.channel_id,
            accept_aggregation_period=aggregation_period,
            accept_data_format=FeedDataFormat.COMPACT,
            accept_event_fields=event_fields,
        )
        await self.connection.send_message(setup_msg)

        # Mark as waiting for reconfiguration
        self._is_configured = False

        # Wait for configuration to complete (with timeout)
        max_wait = 10  # seconds
        wait_interval = 0.1
        elapsed = 0.0
        while not self._is_configured and elapsed < max_wait:
            await asyncio.sleep(wait_interval)
            elapsed += wait_interval

        if not self._is_configured:
            raise TimeoutError(
                f"Channel {self.channel_id} failed to configure within {max_wait}s"
            )

    async def subscribe(
        self,
        symbol: str,
        event_type: EventType,
        from_time: int | None = None,
    ) -> None:
        """
        Subscribe to market events for a symbol.

        Args:
            symbol: The symbol to subscribe to (e.g., "AAPL", "SPY", "AAPL{=5m}").
            event_type: The type of event (Quote, Trade, Candle, etc.).
            from_time: For time-series events like Candle, the start time in epoch milliseconds.
        """
        if not self._is_open:
            raise RuntimeError(
                f"Channel {self.channel_id} must be opened before subscribing"
            )

        key = (symbol, event_type)
        if key in self._subscriptions:
            logger.warning(f"Already subscribed to {event_type.value} for {symbol}")
            return

        # Configure channel if not already done (send config with all event types)
        # The server will dynamically add event types as subscriptions are made
        if not self._is_configured:
            await self.configure()

        # Add event type to our local event_fields if not present
        # This ensures we can parse events even if server hasn't confirmed yet
        if event_type.value not in self._event_fields:
            all_fields = self._get_default_event_fields()
            if event_type.value in all_fields:
                self._event_fields[event_type.value] = all_fields[event_type.value]
                logger.debug(
                    f"Added {event_type.value} to channel {self.channel_id} event fields"
                )

        subscription = Subscription(symbol, event_type, from_time)
        self._subscriptions[key] = subscription

        sub_dict = subscription.to_dict()
        logger.info(
            f"Subscribing to {event_type.value} for {symbol} on channel {self.channel_id}"
        )

        sub_msg = FeedSubscriptionMessage(self.channel_id, add=[sub_dict])
        await self.connection.send_message(sub_msg)

    async def unsubscribe(self, symbol: str, event_type: EventType) -> None:
        """
        Unsubscribe from market events for a symbol.

        Args:
            symbol: The symbol to unsubscribe from.
            event_type: The type of event.
        """
        key = (symbol, event_type)
        if key not in self._subscriptions:
            logger.warning(f"Not subscribed to {event_type.value} for {symbol}")
            return

        logger.info(
            f"Unsubscribing from {event_type.value} for {symbol} on channel {self.channel_id}"
        )

        subscription = self._subscriptions.pop(key)
        sub_msg = FeedSubscriptionMessage(
            self.channel_id, remove=[subscription.to_dict()]
        )
        await self.connection.send_message(sub_msg)

    async def unsubscribe_all(self) -> None:
        """Unsubscribe from all symbols on this channel."""
        if not self._subscriptions:
            return

        logger.info(f"Unsubscribing from all symbols on channel {self.channel_id}")
        self._subscriptions.clear()

        sub_msg = FeedSubscriptionMessage(self.channel_id, reset=True)
        await self.connection.send_message(sub_msg)

    def register_event_handler(self, handler: Callable[[MarketEvent], None]) -> None:
        """
        Register a handler to receive market events.

        Args:
            handler: Callback function that receives MarketEvent objects.
        """
        self._event_handlers.append(handler)

    def unregister_event_handler(self, handler: Callable[[MarketEvent], None]) -> None:
        """
        Unregister an event handler.

        Args:
            handler: The handler to remove.
        """
        try:
            self._event_handlers.remove(handler)
        except ValueError:
            pass

    def _handle_channel_opened(self, message: Message) -> None:
        """Handle CHANNEL_OPENED message."""
        if not isinstance(message, ChannelOpenedMessage):
            logger.debug(
                f"Channel {self.channel_id} received non-ChannelOpenedMessage: {type(message)}"
            )
            return
        if message.channel != self.channel_id:
            logger.debug(
                f"Channel {self.channel_id} ignoring CHANNEL_OPENED for channel {message.channel}"
            )
            return

        self._is_open = True
        logger.info(f"Channel {self.channel_id} opened successfully")

    def _handle_channel_closed(self, message: Message) -> None:
        """Handle CHANNEL_CLOSED message."""
        if message.channel != self.channel_id:
            return

        self._is_open = False
        logger.info(f"Channel {self.channel_id} closed")

    def _handle_feed_config(self, message: Message) -> None:
        """Handle FEED_CONFIG message."""
        if not isinstance(message, FeedConfigMessage):
            return
        if message.channel != self.channel_id:
            return

        self._is_configured = True
        # Store the event fields that the server confirmed it will send
        # Note: The server may return a subset of what we requested
        # Merge with our local event_fields to keep types from active subscriptions
        old_types = list(self._event_fields.keys()) if self._event_fields else []

        # Keep event types that have active subscriptions even if server doesn't confirm yet
        active_event_types = {sub[1].value for sub in self._subscriptions.keys()}
        all_default_fields = self._get_default_event_fields()

        # Start with server's confirmed fields
        merged_fields = dict(message.event_fields)

        # Add any active subscription types that aren't in server's response yet
        for event_type in active_event_types:
            if event_type not in merged_fields and event_type in all_default_fields:
                merged_fields[event_type] = all_default_fields[event_type]

        self._event_fields = merged_fields
        new_types = list(merged_fields.keys())
        logger.info(
            f"Channel {self.channel_id} configured with format: {message.data_format.value}, "
            f"event types: {new_types} (server: {list(message.event_fields.keys())}, was: {old_types})"
        )

    def _handle_feed_data(self, message: Message) -> None:
        """Handle FEED_DATA message."""
        if not isinstance(message, FeedDataMessage):
            return
        if message.channel != self.channel_id:
            return

        # Check if channel is configured and has event fields
        if not self._event_fields:
            # During initial configuration or reconfiguration, event_fields may be empty
            # Just skip processing until FEED_CONFIG arrives
            logger.debug(
                f"Channel {self.channel_id} received FEED_DATA before FEED_CONFIG - skipping"
            )
            return

        # Parse events from COMPACT format
        # Format: array<oneOf> where even elements are event types, odd elements are values
        # Example: [Quote, AAPL, Quote, 123, 123, AMZN, Quote, 321, 321, Trade, AAPL, Trade, 321, 22]
        # OR legacy format: [event_type, [values...], [values...], ...]
        # OR concatenated format: [event_type, [all_values_flat]]
        data = message.data
        if not data:
            logger.debug(f"Channel {self.channel_id} received empty FEED_DATA")
            return

        events_parsed = 0

        # Detect format by checking structure
        if len(data) >= 2 and isinstance(data[0], str) and isinstance(data[1], list):
            # Legacy formats: [event_type, [values...], ...] or [event_type, [flat_array]]
            event_type_str = data[0]
            if event_type_str not in self._event_fields:
                logger.warning(
                    f"Channel {self.channel_id}: Unknown event type '{event_type_str}'. "
                    f"Configured types: {list(self._event_fields.keys())}"
                )
                return

            fields = self._event_fields[event_type_str]
            num_fields = len(fields)

            if len(data) == 2 and len(data[1]) > num_fields:
                # Concatenated format: split the large array into chunks
                flat_data = data[1]
                num_events = len(flat_data) // num_fields

                logger.debug(
                    f"Channel {self.channel_id} received FEED_DATA with {num_events} {event_type_str} events (concatenated format)"
                )

                for i in range(num_events):
                    start_idx = i * num_fields
                    end_idx = start_idx + num_fields
                    event_data = flat_data[start_idx:end_idx]

                    event = parse_event(event_data, fields)
                    self._dispatch_event(event)
                    events_parsed += 1
            else:
                # Legacy array format: each element after data[0] is a separate event
                num_events = len(data) - 1

                logger.debug(
                    f"Channel {self.channel_id} received FEED_DATA with {num_events} {event_type_str} events (legacy array format)"
                )

                for event_data in data[1:]:
                    if isinstance(event_data, list):
                        event = parse_event(event_data, fields)
                        self._dispatch_event(event)
                        events_parsed += 1
        else:
            # New array<oneOf> format: alternating event types and values
            # [EventType, values..., EventType, values..., ...]
            logger.debug(
                f"Channel {self.channel_id} received FEED_DATA in array<oneOf> format with {len(data)} elements"
            )

            i = 0
            while i < len(data):
                if not isinstance(data[i], str):
                    logger.warning(
                        f"Expected event type string at index {i}, got {type(data[i])}"
                    )
                    break

                event_type_str = data[i]
                if event_type_str not in self._event_fields:
                    logger.warning(f"Unknown event type: {event_type_str}")
                    i += 1
                    continue

                fields = self._event_fields[event_type_str]
                num_fields = len(fields)

                # The next num_fields elements are the values for this event
                if i + num_fields >= len(data):
                    logger.warning(
                        f"Not enough data for event type {event_type_str} "
                        f"(need {num_fields} fields, have {len(data) - i - 1})"
                    )
                    break

                # Extract the values for this event
                event_values = data[i + 1 : i + 1 + num_fields]

                # Parse the event
                event = parse_event(event_values, fields)
                self._dispatch_event(event)
                events_parsed += 1

                # Move to next event (skip event type + field count)
                i += 1 + num_fields

        logger.debug(
            f"Channel {self.channel_id} parsed and dispatched {events_parsed} events"
        )

    def _dispatch_event(self, event: MarketEvent) -> None:
        """
        Dispatch an event to all registered handlers.

        Args:
            event: The market event to dispatch.
        """
        for handler in self._event_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")

    def _get_default_event_fields(self) -> dict[str, list[str]]:
        """
        Get default event fields configuration by introspecting event classes.

        Dynamically discovers all property names from each event class
        and converts them to camelCase for the API.
        """
        from ..events import (
            AnalyticOrderEvent,
            CandleEvent,
            ConfigurationEvent,
            GreeksEvent,
            MessageEvent,
            OptionSaleEvent,
            OrderEvent,
            ProfileEvent,
            QuoteEvent,
            SeriesEvent,
            SpreadOrderEvent,
            SummaryEvent,
            TheoreticalPriceEvent,
            TimeAndSaleEvent,
            TradeETHEvent,
            TradeEvent,
            UnderlyingEvent,
        )

        # Map event type names to their classes
        event_classes = {
            "Quote": QuoteEvent,
            "Trade": TradeEvent,
            "TradeETH": TradeETHEvent,
            "Profile": ProfileEvent,
            "Summary": SummaryEvent,
            "Greeks": GreeksEvent,
            "TheoPrice": TheoreticalPriceEvent,
            "Underlying": UnderlyingEvent,
            "Series": SeriesEvent,
            "Candle": CandleEvent,
            "TimeAndSale": TimeAndSaleEvent,
            "OptionSale": OptionSaleEvent,
            "Order": OrderEvent,
            "SpreadOrder": SpreadOrderEvent,
            "AnalyticOrder": AnalyticOrderEvent,
            "Configuration": ConfigurationEvent,
            "Message": MessageEvent,
        }

        event_fields: dict[str, list[str]] = {}

        for event_type, event_class in event_classes.items():
            # Always include base fields
            fields = ["eventType", "eventSymbol", "eventTime"]

            # Get all properties from the event class (excluding private and base methods)
            for attr_name in dir(event_class):
                # Skip private attributes, dunders, and methods from MarketEvent base class
                if attr_name.startswith("_") or attr_name in (
                    "event_type",
                    "event_symbol",
                    "event_time",
                    "get",
                    "to_dict",
                ):
                    continue

                attr = getattr(event_class, attr_name)
                # Check if it's a property
                if isinstance(attr, property):
                    # Convert snake_case to camelCase for API
                    camel_case_name = self._snake_to_camel(attr_name)
                    if camel_case_name not in fields:
                        fields.append(camel_case_name)

            event_fields[event_type] = fields

        return event_fields

    @staticmethod
    def _snake_to_camel(snake_str: str) -> str:
        """
        Convert snake_case to camelCase.

        Args:
            snake_str: String in snake_case format.

        Returns:
            String in camelCase format.

        Example:
            >>> FeedChannel._snake_to_camel("bid_price")
            'bidPrice'
            >>> FeedChannel._snake_to_camel("event_symbol")
            'eventSymbol'
        """
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    async def __aenter__(self):
        """Context manager entry."""
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()
