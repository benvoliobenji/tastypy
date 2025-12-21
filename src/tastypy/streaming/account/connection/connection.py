"""WebSocket connection management for TastyTrade Account Streamer."""

import asyncio
import json
import logging
from typing import Any, Callable

import websockets
from websockets.asyncio.client import ClientConnection

logger = logging.getLogger(__name__)


class AccountConnection:
    """
    Manages WebSocket connection to TastyTrade Account Streamer.
    """

    def __init__(
        self,
        websocket_url: str,
        access_token: str,
        heartbeat_interval: float = 10.0,
    ) -> None:
        """
        Initialize an Account Streamer connection.

        Args:
            websocket_url: WebSocket URL for account streamer.
            access_token: OAuth2 access token (Bearer token).
            heartbeat_interval: Interval between heartbeats in seconds (default: 10s).
        """
        self.websocket_url = websocket_url
        self.access_token = access_token
        self.heartbeat_interval = heartbeat_interval

        self._websocket: ClientConnection | None = None
        self._is_connected = False
        self._heartbeat_task: asyncio.Task[None] | None = None
        self._receive_task: asyncio.Task[None] | None = None
        self._message_handlers: list[Callable[[dict[str, Any]], None]] = []
        self._request_id_counter = 0
        self._web_socket_session_id: str = ""

    @property
    def is_connected(self) -> bool:
        """Check if the connection is established."""
        return self._is_connected

    @property
    def session_id(self) -> str:
        """Get the WebSocket session ID from the server."""
        return self._web_socket_session_id

    def _next_request_id(self) -> int:
        """Generate next request ID for tracking messages."""
        self._request_id_counter += 1
        return self._request_id_counter

    async def connect(self) -> None:
        """
        Establish WebSocket connection to account streamer.

        This opens the WebSocket and prepares for subscriptions.
        Note: You must call subscribe() methods after connecting to receive event data.
        """
        try:
            logger.info(f"Connecting to {self.websocket_url}")
            self._websocket = await websockets.connect(
                self.websocket_url,
                max_size=2**23,  # 8MB max message size
            )
            self._is_connected = True
            logger.info("Account streamer WebSocket connected")

            # Start message receiving task
            self._receive_task = asyncio.create_task(self._receive_messages())

            # Start heartbeat task
            self._heartbeat_task = asyncio.create_task(self._send_heartbeats())

            logger.info("Account streamer connection established")

        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            self._is_connected = False
            raise

    async def disconnect(self) -> None:
        """Close the WebSocket connection and cleanup tasks."""
        if not self._is_connected:
            return

        logger.info("Disconnecting from account streamer")

        # Cancel tasks
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        # Close websocket
        if self._websocket:
            await self._websocket.close()
            self._websocket = None

        self._is_connected = False
        self._web_socket_session_id = ""
        logger.info("Disconnected from account streamer")

    async def send_message(self, message: dict[str, Any]) -> None:
        """
        Send a JSON message to the account streamer.

        Args:
            message: Dictionary to send as JSON.
        """
        if not self._websocket or not self._is_connected:
            raise RuntimeError("Not connected")

        # Add auth token to all messages
        message["auth-token"] = f"Bearer {self.access_token}"

        # Add request-id if not present
        if "request-id" not in message:
            message["request-id"] = self._next_request_id()

        json_str = json.dumps(message)
        logger.debug(f"Sending: {json_str}")
        await self._websocket.send(json_str)

    async def _send_heartbeats(self) -> None:
        """Send periodic heartbeat messages to keep connection alive."""
        while self._is_connected:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                await self.send_message({"action": "heartbeat"})
                logger.debug("Heartbeat sent")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")

    async def _receive_messages(self) -> None:
        """Receive and dispatch messages from the WebSocket."""
        if not self._websocket:
            return

        try:
            async for message_str in self._websocket:
                try:
                    message = json.loads(message_str)
                    logger.debug(f"Received: {message}")

                    # Store session ID from responses
                    if "web-socket-session-id" in message:
                        self._web_socket_session_id = message["web-socket-session-id"]

                    # Handle status responses (heartbeat, connect, etc.)
                    if message.get("status") == "ok":
                        action = message.get("action")
                        logger.debug(f"Action '{action}' acknowledged")
                        continue

                    # Dispatch data messages to handlers
                    if "type" in message and "data" in message:
                        for handler in self._message_handlers:
                            try:
                                handler(message)
                            except Exception as e:
                                logger.error(f"Handler error: {e}")

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

        except asyncio.CancelledError:
            logger.debug("Message receiving cancelled")
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
            self._is_connected = False
        except Exception as e:
            logger.error(f"Error in receive loop: {e}")
            self._is_connected = False

    def register_message_handler(
        self, handler: Callable[[dict[str, Any]], None]
    ) -> None:
        """
        Register a callback for incoming messages.

        Args:
            handler: Function to call with each message dict.
        """
        self._message_handlers.append(handler)

    def unregister_message_handler(
        self, handler: Callable[[dict[str, Any]], None]
    ) -> None:
        """
        Unregister a message handler.

        Args:
            handler: The handler function to remove.
        """
        if handler in self._message_handlers:
            self._message_handlers.remove(handler)

    async def subscribe_accounts(self, account_numbers: list[str]) -> None:
        """
        Subscribe to all updates for the specified accounts.

        This subscribes to: orders, balances, and positions.

        Args:
            account_numbers: List of account numbers to monitor.
        """
        await self.send_message({"action": "connect", "value": account_numbers})
        logger.info(f"Subscribed to accounts: {account_numbers}")

    async def subscribe_public_watchlists(self) -> None:
        """Subscribe to public watchlist updates."""
        await self.send_message({"action": "public-watchlists-subscribe"})
        logger.info("Subscribed to public watchlists")

    async def subscribe_quote_alerts(self) -> None:
        """Subscribe to quote alert trigger notifications."""
        await self.send_message({"action": "quote-alerts-subscribe"})
        logger.info("Subscribed to quote alerts")

    async def __aenter__(self):
        """Context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.disconnect()
