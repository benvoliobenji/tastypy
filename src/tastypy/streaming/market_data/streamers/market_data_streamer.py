"""Synchronous market data streamer for TastyTrade."""

import asyncio
import logging
import threading
from typing import Callable, TypedDict

from ....api_quote_tokens import QuoteStreamerTokenAuthResult
from ....session import Session
from ..channels import DomChannel, FeedChannel
from ..connection import DXLinkConnection
from ..enums import DomDataFormat, EventType, FeedContract
from ..events import MarketEvent
from ..messages import DomSnapshotMessage

logger = logging.getLogger(__name__)


class SubscriptionInfo(TypedDict):
    """Information for a FEED subscription."""

    callback: Callable[[MarketEvent], None]
    from_time: int | None
    contract: FeedContract


class MarketDataStreamer:
    """
    High-level interface for streaming market data from TastyTrade.

    This class provides an easy-to-use interface for streaming real-time
    market data. It handles connection management, authentication, and
    runs in a background thread to avoid blocking your application.

    Example:
        >>> from tastypy import Session
        >>> from tastypy.streaming import MarketDataStreamer, EventType
        >>>
        >>> # Create session and streamer
        >>> session = Session(client_secret="...", refresh_token="...")
        >>> streamer = MarketDataStreamer(session)
        >>>
        >>> # Define event handler
        >>> def on_quote(event):
        ...     print(f"{event.event_symbol}: Bid={event.bid_price}, Ask={event.ask_price}")
        >>>
        >>> # Subscribe and start streaming
        >>> streamer.subscribe("AAPL", EventType.QUOTE, on_quote)
        >>> streamer.start()
        >>>
        >>> # ... do other work while streaming in background ...
        >>>
        >>> # Stop streaming
        >>> streamer.stop()
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the market data streamer.

        Args:
            session: An authenticated TastyTrade session.
        """
        self._session = session
        self._connection: DXLinkConnection | None = None
        self._feed_channel: FeedChannel | None = None  # Single shared FEED channel
        self._dom_channels: dict[int, DomChannel] = {}
        self._next_channel_id = 1
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._is_running = False
        self._subscriptions: dict[tuple[str, EventType], SubscriptionInfo] = {}
        self._dom_subscriptions: dict[
            str, tuple[int, Callable[[DomSnapshotMessage], None]]
        ] = {}

    @property
    def is_running(self) -> bool:
        """Check if the streamer is currently running."""
        return self._is_running

    def subscribe(
        self,
        symbol: str,
        event_type: EventType,
        callback: Callable[[MarketEvent], None],
        from_time: int | None = None,
        contract: FeedContract = FeedContract.AUTO,
    ) -> None:
        """
        Subscribe to market events for a symbol.

        This method can be called before or after starting the streamer.
        The subscription will be activated when the streamer is running.

        Args:
            symbol: The symbol to subscribe to (e.g., "AAPL", "SPY", "AAPL{=5m}" for candles).
            event_type: The type of event (Quote, Trade, Candle, Greeks, etc.).
            callback: Function to call when events are received.
            from_time: For time-series events (Candle), the start time in epoch milliseconds.
            contract: The feed contract type (default: AUTO).

        Example:
            >>> def handle_quote(event):
            ...     print(f"Quote: {event.event_symbol} @ {event.bid_price}/{event.ask_price}")
            >>> streamer.subscribe("AAPL", EventType.QUOTE, handle_quote)
        """
        key = (symbol, event_type)
        if key in self._subscriptions:
            logger.warning(f"Already subscribed to {event_type.value} for {symbol}")
            return

        # Store subscription for later activation with all parameters
        self._subscriptions[key] = {
            "callback": callback,
            "from_time": from_time,
            "contract": contract,
        }

        # If already running, activate subscription immediately
        if self._is_running and self._loop:
            asyncio.run_coroutine_threadsafe(
                self._activate_subscription(
                    symbol, event_type, callback, from_time, contract
                ),
                self._loop,
            )

    def unsubscribe(self, symbol: str, event_type: EventType) -> None:
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

        # Remove subscription
        self._subscriptions.pop(key)

        # If running, deactivate subscription on the shared channel
        if self._is_running and self._loop and self._feed_channel:
            if (symbol, event_type) in self._feed_channel._subscriptions:
                asyncio.run_coroutine_threadsafe(
                    self._deactivate_subscription(0, symbol, event_type),
                    self._loop,
                )

    def subscribe_dom(
        self,
        symbol: str,
        callback: Callable[[DomSnapshotMessage], None],
        sources: list[str] | None = None,
        aggregation_period: float = 0.1,
        depth_limit: int = 10,
        data_format: DomDataFormat = DomDataFormat.FULL,
        order_fields: list[str] | None = None,
    ) -> None:
        """
        Subscribe to Depth of Market (Level 2) order book data for a symbol.

        This creates a DOM channel that provides continuous snapshots of the
        order book with multiple price levels on both bid and ask sides.

        Args:
            symbol: The symbol to subscribe to (e.g., "AAPL").
            callback: Function to call when DOM snapshots are received.
            sources: Market data sources (e.g., ["ntv"]). None for default.
            aggregation_period: Update frequency in seconds (default: 0.1 = 100ms).
            depth_limit: Number of price levels to receive (default: 10).
            data_format: Data format (FULL or COMPACT, default: FULL).
            order_fields: Fields to include in orders (default: ["price", "size"]).

        Example:
            >>> def handle_order_book(snapshot):
            ...     print(f"Bids: {snapshot.bids}")
            ...     print(f"Asks: {snapshot.asks}")
            >>> streamer.subscribe_dom("AAPL", handle_order_book, depth_limit=5)
        """
        if symbol in self._dom_subscriptions:
            logger.warning(f"Already subscribed to DOM for {symbol}")
            return

        # Store subscription for later activation
        self._dom_subscriptions[symbol] = (
            self._next_channel_id,
            callback,
        )

        # If already running, activate subscription immediately
        if self._is_running and self._loop:
            asyncio.run_coroutine_threadsafe(
                self._activate_dom_subscription(
                    symbol,
                    callback,
                    sources,
                    aggregation_period,
                    depth_limit,
                    data_format,
                    order_fields,
                ),
                self._loop,
            )

    def unsubscribe_dom(self, symbol: str) -> None:
        """
        Unsubscribe from DOM order book data for a symbol.

        Args:
            symbol: The symbol to unsubscribe from.
        """
        if symbol not in self._dom_subscriptions:
            logger.warning(f"Not subscribed to DOM for {symbol}")
            return

        channel_id, _ = self._dom_subscriptions.pop(symbol)

        # If running, deactivate subscription
        if self._is_running and self._loop:
            asyncio.run_coroutine_threadsafe(
                self._deactivate_dom_subscription(channel_id),
                self._loop,
            )

    def start(self) -> None:
        """
        Start the market data streamer.

        This starts a background thread that manages the WebSocket connection
        and streams market data. The thread will continue running until
        stop() is called.

        Raises:
            RuntimeError: If the streamer is already running.
        """
        if self._is_running:
            raise RuntimeError("Streamer is already running")

        logger.info("Starting market data streamer")
        self._is_running = True
        self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the market data streamer.

        This will close all channels, disconnect from the WebSocket,
        and stop the background thread.
        """
        if not self._is_running:
            logger.warning("Streamer is not running")
            return

        logger.info("Stopping market data streamer")
        self._is_running = False

        # Schedule cleanup and stop in the event loop
        if self._loop and self._loop.is_running():
            try:
                # Create a future to signal when cleanup is done
                cleanup_future = asyncio.run_coroutine_threadsafe(
                    self._cleanup(), self._loop
                )
                # Wait for cleanup to complete (with timeout)
                cleanup_future.result(timeout=5.0)
            except TimeoutError:
                logger.warning("Cleanup timed out after 5 seconds")
            except Exception as e:
                # Ignore "Event loop stopped" errors - this is expected during shutdown
                if "Event loop stopped" not in str(e):
                    logger.error(f"Error during cleanup: {e}")
            finally:
                # Now stop the loop
                if self._loop.is_running():
                    self._loop.call_soon_threadsafe(self._loop.stop)

        # Wait for thread to finish
        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None

        self._loop = None
        logger.info("Market data streamer stopped")

    def wait(self) -> None:
        """
        Wait for the streamer thread to finish.

        This is useful for keeping your main program running while
        the streamer operates in the background.
        """
        if self._thread and self._thread.is_alive():
            self._thread.join()

    def _run_event_loop(self) -> None:
        """Run the asyncio event loop in the background thread."""
        try:
            # Create new event loop for this thread
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            # Run the main streaming logic
            self._loop.run_until_complete(self._streaming_main())

        except asyncio.CancelledError:
            # Normal shutdown - cleanup was called
            logger.debug("Event loop cancelled during shutdown")
        except Exception as e:
            # Only log if it's not a shutdown-related error
            if "Event loop stopped" not in str(e) and not self._is_running:
                logger.debug(f"Event loop stopped during shutdown: {e}")
            elif self._is_running:
                logger.error(f"Error in streaming event loop: {e}")
        finally:
            if self._loop and not self._loop.is_closed():
                self._loop.close()

    async def _streaming_main(self) -> None:
        """Main streaming logic that runs in the event loop."""
        try:
            # Get API quote token
            logger.info("Fetching API quote token")
            token_auth = QuoteStreamerTokenAuthResult(self._session)
            token_auth.sync()

            # Create connection
            logger.info("Creating DXLink connection")
            self._connection = DXLinkConnection(token_auth.dxlink_url, token_auth.token)

            # Connect and authenticate
            await self._connection.connect()
            logger.info("Connected and authenticated")

            # Activate all pending FEED subscriptions
            for (symbol, event_type), sub_info in self._subscriptions.items():
                await self._activate_subscription(
                    symbol,
                    event_type,
                    sub_info["callback"],
                    sub_info.get("from_time"),
                    sub_info.get("contract", FeedContract.AUTO),
                )

            # Activate all pending DOM subscriptions
            for symbol, (_, callback) in self._dom_subscriptions.items():
                await self._activate_dom_subscription(symbol, callback)

            # Keep running until stopped
            while self._is_running:
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error in streaming main: {e}")
        finally:
            # Clean up
            await self._cleanup()

    async def _activate_subscription(
        self,
        symbol: str,
        event_type: EventType,
        callback: Callable[[MarketEvent], None],
        from_time: int | None = None,
        contract: FeedContract = FeedContract.AUTO,
    ) -> None:
        """
        Activate a subscription on a channel.

        Args:
            symbol: The symbol to subscribe to.
            event_type: The type of event.
            callback: The callback function.
            from_time: Optional start time for time-series events.
            contract: The feed contract type.
        """
        if not self._connection:
            return

        # Create or reuse the single shared FEED channel
        if self._feed_channel is None:
            channel_id = self._next_channel_id
            self._next_channel_id += 1

            self._feed_channel = FeedChannel(channel_id, self._connection, contract)
            await self._feed_channel.open()

        # Register callback
        def event_handler(event: MarketEvent) -> None:
            if event.event_symbol == symbol and event.event_type == event_type.value:
                callback(event)

        self._feed_channel.register_event_handler(event_handler)

        # Subscribe on the shared channel
        await self._feed_channel.subscribe(symbol, event_type, from_time)

    async def _deactivate_subscription(
        self, channel_id: int, symbol: str, event_type: EventType
    ) -> None:
        """
        Deactivate a subscription on a channel.

        Args:
            channel_id: The channel ID (unused, kept for compatibility).
            symbol: The symbol to unsubscribe from.
            event_type: The type of event.
        """
        if self._feed_channel:
            await self._feed_channel.unsubscribe(symbol, event_type)

    async def _activate_dom_subscription(
        self,
        symbol: str,
        callback: Callable[[DomSnapshotMessage], None],
        sources: list[str] | None = None,
        aggregation_period: float = 0.1,
        depth_limit: int = 10,
        data_format: DomDataFormat = DomDataFormat.FULL,
        order_fields: list[str] | None = None,
    ) -> None:
        """
        Activate a DOM subscription.

        Args:
            symbol: The symbol to subscribe to.
            callback: The callback function.
            sources: Market data sources.
            aggregation_period: Update frequency in seconds.
            depth_limit: Number of price levels.
            data_format: Data format (FULL or COMPACT).
            order_fields: Fields to include in orders.
        """
        if not self._connection:
            return

        # Create DOM channel
        channel_id = self._next_channel_id
        dom_channel = DomChannel(channel_id, self._connection, symbol, sources)
        self._dom_channels[channel_id] = dom_channel

        # Register callback
        dom_channel.register_snapshot_handler(callback)

        # Open and configure channel
        await dom_channel.open(
            aggregation_period=aggregation_period,
            depth_limit=depth_limit,
            data_format=data_format,
            order_fields=order_fields,
        )

        self._next_channel_id += 1

    async def _deactivate_dom_subscription(self, channel_id: int) -> None:
        """
        Deactivate a DOM subscription.

        Args:
            channel_id: The channel ID.
        """
        if channel_id not in self._dom_channels:
            return

        dom_channel = self._dom_channels.pop(channel_id)
        await dom_channel.close()

    async def _cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up resources")

        # Close shared FEED channel
        if self._feed_channel:
            try:
                await self._feed_channel.close()
            except Exception as e:
                logger.error(f"Error closing FEED channel: {e}")
            self._feed_channel = None

        # Close all DOM channels
        for dom_channel in self._dom_channels.values():
            try:
                await dom_channel.close()
            except Exception as e:
                logger.error(f"Error closing DOM channel: {e}")

        self._dom_channels.clear()

        # Disconnect
        if self._connection:
            try:
                await self._connection.disconnect()
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
            self._connection = None
            self._connection = None

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
