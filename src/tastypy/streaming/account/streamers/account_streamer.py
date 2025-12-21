"""Synchronous account data streamer for TastyTrade."""

import asyncio
import logging
import threading
from typing import Callable

from ....session import Session
from ..connection.connection import AccountConnection
from ..events import (
    AccountEvent,
    AccountEventType,
    parse_account_event,
)

logger = logging.getLogger(__name__)


class AccountStreamer:
    """
    High-level interface for streaming real-time account data from TastyTrade.

    This class provides real-time notifications for:
    - Order status changes (filled, cancelled, routed, etc.)
    - Account balance updates
    - Position changes
    - Quote alert triggers
    - Public watchlist updates

    The streamer runs in a background thread to avoid blocking your application.

    Example:
        >>> from tastypy import Session
        >>> from tastypy.streaming import AccountStreamer, AccountEventType
        >>>
        >>> # Create session and streamer
        >>> session = Session(client_secret="...", refresh_token="...")
        >>> streamer = AccountStreamer(session)
        >>>
        >>> # Define event handlers
        >>> def on_order(event):
        ...     print(f"Order {event.order_id}: {event.status}")
        >>>
        >>> def on_balance(event):
        ...     print(f"Balance: ${event.net_liquidating_value:.2f}")
        >>>
        >>> # Subscribe to event types
        >>> streamer.subscribe(AccountEventType.ORDER, on_order)
        >>> streamer.subscribe(AccountEventType.BALANCE, on_balance)
        >>>
        >>> # Start streaming
        >>> streamer.start()
        >>> streamer.subscribe_accounts(["5WT00000"])
        >>>
        >>> # ... do other work while streaming in background ...
        >>>
        >>> # Stop streaming
        >>> streamer.stop()
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the account streamer.

        Args:
            session: An authenticated TastyTrade session.
        """
        self._session = session
        self._connection: AccountConnection | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._is_running = False
        # Pre-define some dictionary entries for known event types
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
    def is_running(self) -> bool:
        """Check if the streamer is currently running."""
        return self._is_running

    @property
    def session_id(self) -> str:
        """Get the WebSocket session ID from the server."""
        if self._connection:
            return self._connection.session_id
        return ""

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

    async def _connect_async(self) -> None:
        """Async connection logic."""
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
        logger.info("Connected to account streamer")

    async def _disconnect_async(self) -> None:
        """Async disconnection logic."""
        if self._connection:
            await self._connection.disconnect()
            self._connection = None

    async def _subscribe_accounts_async(self, account_numbers: list[str]) -> None:
        """Async account subscription logic."""
        if self._connection:
            await self._connection.subscribe_accounts(account_numbers)

    async def _subscribe_quote_alerts_async(self) -> None:
        """Async quote alerts subscription logic."""
        if self._connection:
            await self._connection.subscribe_quote_alerts()

    async def _subscribe_public_watchlists_async(self) -> None:
        """Async public watchlists subscription logic."""
        if self._connection:
            await self._connection.subscribe_public_watchlists()

    def _run_event_loop(self) -> None:
        """Run the asyncio event loop in a background thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            # Connect
            self._loop.run_until_complete(self._connect_async())

            # Keep running until stopped
            self._loop.run_forever()

        except Exception as e:
            logger.error(f"Error in event loop: {e}")
        finally:
            # Cleanup
            try:
                self._loop.run_until_complete(self._disconnect_async())
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")

            self._loop.close()
            self._loop = None
            logger.info("Event loop closed")

    def start(self) -> None:
        """
        Start the account data streamer.

        This starts a background thread that manages the WebSocket connection
        and streams account data. The thread will continue running until
        stop() is called.

        Raises:
            RuntimeError: If the streamer is already running.
        """
        if self._is_running:
            raise RuntimeError("Streamer is already running")

        logger.info("Starting account data streamer")
        self._is_running = True
        self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._thread.start()

        # Give the connection time to establish
        import time

        time.sleep(1.0)

    def stop(self) -> None:
        """
        Stop the account data streamer.

        This will disconnect from the WebSocket and stop the background thread.
        """
        if not self._is_running:
            return

        logger.info("Stopping account data streamer")
        self._is_running = False

        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)

        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None

        logger.info("Account data streamer stopped")

    def wait(self, timeout: float | None = None) -> None:
        """
        Wait for the streamer thread to finish.

        This is useful for keeping the main thread alive while streaming.

        Args:
            timeout: Maximum time to wait in seconds (None = wait forever).
        """
        if self._thread:
            self._thread.join(timeout=timeout)

    def subscribe_accounts(self, account_numbers: list[str]) -> None:
        """
        Subscribe to updates for specific accounts.

        This subscribes to orders, balances, and positions for the given accounts.

        Args:
            account_numbers: List of account numbers to monitor.
        """
        if not self._is_running or not self._loop:
            raise RuntimeError("Streamer is not running. Call start() first.")

        asyncio.run_coroutine_threadsafe(
            self._subscribe_accounts_async(account_numbers),
            self._loop,
        )

    def subscribe_quote_alerts(self) -> None:
        """Subscribe to quote alert trigger notifications."""
        if not self._is_running or not self._loop:
            raise RuntimeError("Streamer is not running. Call start() first.")

        asyncio.run_coroutine_threadsafe(
            self._subscribe_quote_alerts_async(),
            self._loop,
        )

    def subscribe_public_watchlists(self) -> None:
        """Subscribe to public watchlist updates."""
        if not self._is_running or not self._loop:
            raise RuntimeError("Streamer is not running. Call start() first.")

        asyncio.run_coroutine_threadsafe(
            self._subscribe_public_watchlists_async(),
            self._loop,
        )

    def subscribe(
        self,
        event_type: AccountEventType,
        callback: Callable[[AccountEvent], None],
    ) -> None:
        """
        Subscribe to account events of a specific type.

        This method can be called before or after starting the streamer.

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

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
