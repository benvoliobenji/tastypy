"""Asynchronous market data streamer using DXLink protocol."""

import logging
from typing import Callable

from tastypy.api_quote_tokens import QuoteStreamerTokenAuthResult
from tastypy.session import Session
from ..channels import DomChannel, FeedChannel
from ..connection import DXLinkConnection
from ..enums import DomDataFormat, EventType, FeedContract
from ..events import MarketEvent
from ..messages import DomSnapshotMessage

logger = logging.getLogger(__name__)


class AsyncMarketDataStreamer:
    """
    Async version of MarketDataStreamer for use in async applications.

    This class provides the same functionality as MarketDataStreamer but
    uses async/await instead of threading. Use this if your application
    is already using asyncio.

    Example:
        >>> import asyncio
        >>> from tastypy import Session
        >>> from tastypy.streaming import AsyncMarketDataStreamer, EventType
        >>>
        >>> async def main():
        ...     session = Session(client_secret="...", refresh_token="...")
        ...     streamer = AsyncMarketDataStreamer(session)
        ...
        ...     def on_quote(event):
        ...         print(f"{event.event_symbol}: Bid={event.bid_price}")
        ...
        ...     await streamer.connect()
        ...     await streamer.subscribe("AAPL", EventType.QUOTE, on_quote)
        ...
        ...     # Keep streaming for 60 seconds
        ...     await asyncio.sleep(60)
        ...
        ...     await streamer.disconnect()
        >>>
        >>> asyncio.run(main())
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the async market data streamer.

        Args:
            session: An authenticated TastyTrade session.
        """
        self._session = session
        self._connection: DXLinkConnection | None = None
        self._feed_channel: FeedChannel | None = None  # Single shared FEED channel
        self._dom_channels: dict[int, DomChannel] = {}
        self._next_channel_id = 1
        self._is_connected = False

    @property
    def is_connected(self) -> bool:
        """Check if the streamer is connected."""
        return self._is_connected

    async def connect(self) -> None:
        """
        Connect to the DXLink WebSocket server.

        Raises:
            RuntimeError: If already connected.
        """
        if self._is_connected:
            raise RuntimeError("Already connected")

        logger.info("Fetching API quote token")
        token_auth = QuoteStreamerTokenAuthResult(self._session)
        token_auth.sync()

        logger.info("Creating DXLink connection")
        self._connection = DXLinkConnection(token_auth.dxlink_url, token_auth.token)

        await self._connection.connect()
        self._is_connected = True
        logger.info("Connected and authenticated")

    async def disconnect(self) -> None:
        """Disconnect from the DXLink server."""
        if not self._is_connected:
            return

        logger.info("Disconnecting")

        # Close shared FEED channel
        if self._feed_channel:
            await self._feed_channel.close()
            self._feed_channel = None

        # Close all DOM channels
        for dom_channel in self._dom_channels.values():
            await dom_channel.close()

        self._dom_channels.clear()

        # Disconnect
        if self._connection:
            await self._connection.disconnect()
            self._connection = None

        self._is_connected = False
        logger.info("Disconnected")

    async def subscribe(
        self,
        symbol: str,
        event_type: EventType,
        callback: Callable[[MarketEvent], None],
        from_time: int | None = None,
        contract: FeedContract = FeedContract.AUTO,
    ) -> None:
        """
        Subscribe to market events for a symbol.

        Args:
            symbol: The symbol to subscribe to.
            event_type: The type of event.
            callback: Function to call when events are received.
            from_time: For time-series events, the start time in epoch milliseconds.
            contract: The feed contract type.
        """
        if not self._is_connected or not self._connection:
            raise RuntimeError("Not connected. Call connect() first.")

        logger.info(f"Subscribing to {event_type.value} for {symbol}")

        # Create or reuse the single shared FEED channel
        if self._feed_channel is None:
            channel_id = self._next_channel_id
            self._next_channel_id += 1

            logger.debug(f"Creating shared FEED channel {channel_id}")
            self._feed_channel = FeedChannel(channel_id, self._connection, contract)
            await self._feed_channel.open()
            logger.debug(f"Shared FEED channel {channel_id} opened")

        # Register callback
        def event_handler(event: MarketEvent) -> None:
            if event.event_symbol == symbol and event.event_type == event_type.value:
                callback(event)

        self._feed_channel.register_event_handler(event_handler)

        # Subscribe on the shared channel
        await self._feed_channel.subscribe(symbol, event_type, from_time)
        logger.info(f"Successfully subscribed to {event_type.value} for {symbol}")

    async def unsubscribe(self, symbol: str, event_type: EventType) -> None:
        """
        Unsubscribe from market events for a symbol.

        Args:
            symbol: The symbol to unsubscribe from.
            event_type: The type of event.
        """
        if self._feed_channel:
            await self._feed_channel.unsubscribe(symbol, event_type)

    async def subscribe_dom(
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

        Args:
            symbol: The symbol to subscribe to (e.g., "AAPL").
            callback: Function to call when DOM snapshots are received.
            sources: Market data sources (e.g., ["ntv"]). None for default.
            aggregation_period: Update frequency in seconds (default: 0.1 = 100ms).
            depth_limit: Number of price levels to receive (default: 10).
            data_format: Data format (FULL or COMPACT, default: FULL).
            order_fields: Fields to include in orders (default: ["price", "size"]).

        Example:
            >>> async def handle_order_book(snapshot):
            ...     print(f"Bids: {snapshot.bids}")
            ...     print(f"Asks: {snapshot.asks}")
            >>> await streamer.subscribe_dom("AAPL", handle_order_book, depth_limit=5)
        """
        if not self._is_connected or not self._connection:
            raise RuntimeError("Not connected. Call connect() first.")

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

    async def unsubscribe_dom(self, symbol: str) -> None:
        """
        Unsubscribe from DOM order book data for a symbol.

        Args:
            symbol: The symbol to unsubscribe from.
        """
        # Find and close the DOM channel for this symbol
        for channel_id, dom_channel in list(self._dom_channels.items()):
            if dom_channel.symbol == symbol:
                await dom_channel.close()
                del self._dom_channels[channel_id]
                break

    async def __aenter__(self):
        """Context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.disconnect()
