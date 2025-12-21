"""Asynchronous account data streamer for TastyTrade."""

import logging
from typing import Callable

from ....session import Session
from ..connection.connection import AccountConnection
from ..events import (
    AccountEvent,
    AccountEventType,
    parse_account_event,
)

logger = logging.getLogger(__name__)


class AsyncAccountStreamer:
    """
    Async streamer for real-time account updates from TastyTrade.

    This class provides real-time notifications for:
    - Order status changes (filled, cancelled, routed, etc.)
    - Account balance updates
    - Position changes
    - Quote alert triggers
    - Public watchlist updates

    Use this if your application is already using asyncio.

    Example:
        >>> import asyncio
        >>> from tastypy import Session
        >>> from tastypy.streaming import AsyncAccountStreamer, AccountEventType
        >>>
        >>> async def main():
        ...     session = Session(client_secret="...", refresh_token="...")
        ...     async with AsyncAccountStreamer(session) as streamer:
        ...
        ...         def on_order(event):
        ...             print(f"Order {event.order_id}: {event.status}")
        ...
        ...         streamer.subscribe(AccountEventType.ORDER, on_order)
        ...         await streamer.subscribe_accounts(["5WT00000"])
        ...
        ...         # Keep streaming for 60 seconds
        ...         await asyncio.sleep(60)
        >>>
        >>> asyncio.run(main())
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the async account streamer.

        Args:
            session: An authenticated TastyTrade session.
        """
        self._session = session
        self._connection: AccountConnection | None = None
        self._is_connected = False
        self._subscriptions: dict[
            AccountEventType, list[Callable[[AccountEvent], None]]
        ] = {
            AccountEventType.ORDER: [],
            AccountEventType.BALANCE: [],
            AccountEventType.POSITION: [],
            AccountEventType.QUOTE_ALERT: [],
            AccountEventType.PUBLIC_WATCHLISTS: [],
            AccountEventType.COMPLEX_ORDER: [],
        }

    @property
    def is_connected(self) -> bool:
        """Check if the streamer is connected."""
        return self._is_connected

    @property
    def session_id(self) -> str:
        """Get the WebSocket session ID from the server."""
        if self._connection:
            return self._connection.session_id
        return ""

    async def connect(self) -> None:
        """
        Connect to the TastyTrade Account Streamer.

        Raises:
            RuntimeError: If already connected.
        """
        if self._is_connected:
            raise RuntimeError("Already connected")

        # Ensure session has valid token
        if not self._session.is_logged_in():
            self._session.refresh()

        # Determine WebSocket URL based on environment
        if self._session.is_sandbox():
            websocket_url = "wss://streamer.cert.tastyworks.com"
        else:
            websocket_url = "wss://streamer.tastyworks.com"

        logger.info(f"Creating account streamer connection to {websocket_url}")
        self._connection = AccountConnection(
            websocket_url=websocket_url,
            access_token=self._session.access_token,
            heartbeat_interval=10.0,  # Send heartbeat every 10 seconds
        )

        # Register event handler
        self._connection.register_message_handler(self._handle_message)

        await self._connection.connect()
        self._is_connected = True
        logger.info("Connected to account streamer")

    async def disconnect(self) -> None:
        """Disconnect from the account streamer."""
        if not self._is_connected:
            return

        logger.info("Disconnecting from account streamer")

        if self._connection:
            await self._connection.disconnect()
            self._connection = None

        self._is_connected = False
        logger.info("Disconnected from account streamer")

    def _handle_message(self, message: dict) -> None:
        """
        Handle incoming messages from the account streamer.

        Args:
            message: Raw message dictionary.
        """
        try:
            # Parse the event
            event = parse_account_event(message)
            event_type = event.event_type

            # Call registered handlers for this event type
            if event_type and event_type in self._subscriptions:
                for callback in self._subscriptions[event_type]:
                    try:
                        callback(event)
                    except Exception as e:
                        logger.error(f"Error in {event_type.value} callback: {e}")

        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def subscribe_accounts(self, account_numbers: list[str]) -> None:
        """
        Subscribe to updates for specific accounts.

        This subscribes to orders, balances, and positions for the given accounts.

        Args:
            account_numbers: List of account numbers to monitor.

        Raises:
            RuntimeError: If not connected.
        """
        if not self._is_connected or not self._connection:
            raise RuntimeError("Not connected. Call connect() first.")

        await self._connection.subscribe_accounts(account_numbers)

    async def subscribe_quote_alerts(self) -> None:
        """
        Subscribe to quote alert trigger notifications.

        Raises:
            RuntimeError: If not connected.
        """
        if not self._is_connected or not self._connection:
            raise RuntimeError("Not connected. Call connect() first.")

        await self._connection.subscribe_quote_alerts()

    async def subscribe_public_watchlists(self) -> None:
        """
        Subscribe to public watchlist updates.

        Raises:
            RuntimeError: If not connected.
        """
        if not self._is_connected or not self._connection:
            raise RuntimeError("Not connected. Call connect() first.")

        await self._connection.subscribe_public_watchlists()

    def subscribe(
        self,
        event_type: AccountEventType,
        callback: Callable[[AccountEvent], None],
    ) -> None:
        """
        Subscribe to account events of a specific type.

        Args:
            event_type: The type of event to subscribe to (ORDER, BALANCE, POSITION, QUOTE_ALERT).
            callback: Function to call when events of this type are received.

        Example:
            >>> def handle_order(event):
            ...     print(f"Order: {event.order_id} - {event.status}")
            >>> streamer.subscribe(AccountEventType.ORDER, handle_order)
        """
        if event_type not in self._subscriptions:
            logger.warning(f"Unknown event type: {event_type}")
            return

        if callback in self._subscriptions[event_type]:
            logger.warning(
                f"Already subscribed to {event_type.value} with this callback"
            )
            return

        self._subscriptions[event_type].append(callback)
        logger.info(f"Subscribed to {event_type.value} events")

    def unsubscribe(
        self,
        event_type: AccountEventType,
        callback: Callable[[AccountEvent], None],
    ) -> None:
        """
        Unsubscribe from account events of a specific type.

        Args:
            event_type: The type of event to unsubscribe from.
            callback: The callback function to remove.
        """
        if event_type not in self._subscriptions:
            logger.warning(f"Unknown event type: {event_type}")
            return

        if callback not in self._subscriptions[event_type]:
            logger.warning(f"Not subscribed to {event_type.value} with this callback")
            return

        self._subscriptions[event_type].remove(callback)
        logger.info(f"Unsubscribed from {event_type.value} events")

    async def __aenter__(self):
        """Context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.disconnect()
