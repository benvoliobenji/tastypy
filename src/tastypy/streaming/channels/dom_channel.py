"""DOM channel for streaming order book data."""

import asyncio
import logging
from typing import Any, Callable

from ..enums import (
    DomDataFormat,
    MessageType,
    ServiceType,
)
from ..messages import (
    ChannelCancelMessage,
    ChannelOpenedMessage,
    ChannelRequestMessage,
    DomConfigMessage,
    DomSetupMessage,
    DomSnapshotMessage,
    Message,
)

logger = logging.getLogger(__name__)


class DomChannel:
    """
    Manages a DOM service channel for streaming order book data.

    A DOM (Depth of Market) channel provides Level 2 order book data,
    showing multiple price levels and order sizes on both bid and ask sides.
    """

    def __init__(
        self,
        channel_id: int,
        connection: Any,  # DXLinkConnection type
        symbol: str,
        sources: list[str] | None = None,
    ) -> None:
        """
        Initialize a DOM channel.

        Args:
            channel_id: The channel ID (must be > 0).
            connection: The DXLink connection to use.
            symbol: The symbol to stream order book for.
            sources: Market data sources (e.g., ["ntv"]). None for default.
        """
        if channel_id <= 0:
            raise ValueError("Channel ID must be greater than 0")

        self.channel_id = channel_id
        self.connection = connection
        self.symbol = symbol
        self.sources = sources or ["ntv"]

        self._is_open = False
        self._is_configured = False
        self._snapshot_handlers: list[Callable[[DomSnapshotMessage], None]] = []

        # Register message handlers
        self.connection.register_handler(
            MessageType.CHANNEL_OPENED, self._handle_channel_opened
        )
        self.connection.register_handler(
            MessageType.CHANNEL_CLOSED, self._handle_channel_closed
        )
        self.connection.register_handler(
            MessageType.DOM_CONFIG, self._handle_dom_config
        )
        self.connection.register_handler(
            MessageType.DOM_SNAPSHOT, self._handle_dom_snapshot
        )

    @property
    def is_open(self) -> bool:
        """Check if the channel is open."""
        return self._is_open

    @property
    def is_configured(self) -> bool:
        """Check if the channel is configured."""
        return self._is_configured

    async def open(
        self,
        aggregation_period: float = 0.1,
        depth_limit: int = 10,
        data_format: DomDataFormat = DomDataFormat.FULL,
        order_fields: list[str] | None = None,
    ) -> None:
        """
        Open the DOM channel and configure it.

        Args:
            aggregation_period: Update frequency in seconds (default: 0.1 = 100ms).
            depth_limit: Number of price levels to receive (default: 10).
            data_format: Data format (FULL or COMPACT, default: FULL).
            order_fields: Fields to include in each order (default: ["price", "size"]).
        """
        if self._is_open:
            logger.warning(f"DOM channel {self.channel_id} is already open")
            return

        logger.info(f"Opening DOM channel {self.channel_id} for {self.symbol}")

        # Request channel
        request = ChannelRequestMessage(
            self.channel_id,
            ServiceType.DOM,
            {"symbol": self.symbol, "sources": self.sources},
        )
        await self.connection.send_message(request)

        # Wait for channel to be opened (with timeout)
        max_wait = 10  # seconds
        wait_interval = 0.1
        elapsed = 0.0
        while not self._is_open and elapsed < max_wait:
            await asyncio.sleep(wait_interval)
            elapsed += wait_interval

        if not self._is_open:
            raise TimeoutError(
                f"DOM channel {self.channel_id} failed to open within {max_wait}s"
            )

        # Configure DOM service
        setup = DomSetupMessage(
            self.channel_id,
            accept_aggregation_period=aggregation_period,
            accept_depth_limit=depth_limit,
            accept_data_format=data_format,
            accept_order_fields=order_fields or ["price", "size"],
        )
        await self.connection.send_message(setup)

    async def close(self) -> None:
        """Close the DOM channel."""
        if not self._is_open:
            logger.warning(f"DOM channel {self.channel_id} is not open")
            return

        logger.info(f"Closing DOM channel {self.channel_id}")

        # Send cancel message
        cancel = ChannelCancelMessage(self.channel_id)
        await self.connection.send_message(cancel)

        self._is_open = False
        self._is_configured = False

        # Unregister handlers
        self.connection.unregister_handler(
            MessageType.CHANNEL_OPENED, self._handle_channel_opened
        )
        self.connection.unregister_handler(
            MessageType.CHANNEL_CLOSED, self._handle_channel_closed
        )
        self.connection.unregister_handler(
            MessageType.DOM_CONFIG, self._handle_dom_config
        )
        self.connection.unregister_handler(
            MessageType.DOM_SNAPSHOT, self._handle_dom_snapshot
        )

    def register_snapshot_handler(
        self, handler: Callable[[DomSnapshotMessage], None]
    ) -> None:
        """
        Register a handler for DOM snapshot messages.

        Args:
            handler: Callback function that receives DomSnapshotMessage objects.
        """
        self._snapshot_handlers.append(handler)

    def unregister_snapshot_handler(
        self, handler: Callable[[DomSnapshotMessage], None]
    ) -> None:
        """
        Unregister a snapshot handler.

        Args:
            handler: The handler to remove.
        """
        if handler in self._snapshot_handlers:
            self._snapshot_handlers.remove(handler)

    def _handle_channel_opened(self, message: Message) -> None:
        """Handle CHANNEL_OPENED message."""
        if not isinstance(message, ChannelOpenedMessage):
            return
        if message.channel != self.channel_id:
            return

        self._is_open = True
        logger.info(f"DOM channel {self.channel_id} opened for {self.symbol}")

    def _handle_channel_closed(self, message: Message) -> None:
        """Handle CHANNEL_CLOSED message."""
        if message.channel != self.channel_id:
            return

        self._is_open = False
        self._is_configured = False
        logger.info(f"DOM channel {self.channel_id} closed")

    def _handle_dom_config(self, message: Message) -> None:
        """Handle DOM_CONFIG message."""
        if not isinstance(message, DomConfigMessage):
            return
        if message.channel != self.channel_id:
            return

        self._is_configured = True
        logger.info(
            f"DOM channel {self.channel_id} configured: "
            f"format={message.data_format.value}, "
            f"depth_limit={message.depth_limit}, "
            f"fields={message.order_fields}"
        )

    def _handle_dom_snapshot(self, message: Message) -> None:
        """Handle DOM_SNAPSHOT message."""
        if not isinstance(message, DomSnapshotMessage):
            return
        if message.channel != self.channel_id:
            return

        # Call all registered handlers
        for handler in self._snapshot_handlers:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"Error in DOM snapshot handler: {e}")

    async def __aenter__(self):
        """Context manager entry."""
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()
