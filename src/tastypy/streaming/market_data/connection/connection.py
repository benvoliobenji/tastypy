"""WebSocket connection management for DXLink protocol."""

import asyncio
import json
import logging
from typing import Any, Callable

import websockets
from websockets.asyncio.client import ClientConnection

from ..enums import MessageType
from ..messages import (
    AuthMessage,
    KeepaliveMessage,
    Message,
    SetupMessage,
    parse_message,
)

logger = logging.getLogger(__name__)


class DXLinkConnection:
    """
    Manages WebSocket connection to DXLink server.

    Handles connection setup, authentication, keepalive, and message routing.
    """

    def __init__(
        self,
        websocket_url: str,
        auth_token: str,
        keepalive_timeout: int = 60,
    ) -> None:
        """
        Initialize a DXLink connection.

        Args:
            websocket_url: The WebSocket URL for DXLink.
            auth_token: The API quote token for authentication.
            keepalive_timeout: Keepalive timeout in seconds (default: 60).
        """
        self.websocket_url = websocket_url
        self.auth_token = auth_token
        self.keepalive_timeout = keepalive_timeout

        self._websocket: ClientConnection | None = None
        self._is_connected = False
        self._is_authenticated = False
        self._keepalive_task: asyncio.Task[None] | None = None
        self._receive_task: asyncio.Task[None] | None = None
        self._message_handlers: dict[MessageType, list[Callable[[Message], None]]] = {}

    @property
    def is_connected(self) -> bool:
        """Check if the connection is established."""
        return self._is_connected

    @property
    def is_authenticated(self) -> bool:
        """Check if the connection is authenticated."""
        return self._is_authenticated

    async def connect(self) -> None:
        """
        Establish WebSocket connection and authenticate.

        This performs the full connection sequence:
        1. Connect to WebSocket
        2. Send SETUP message
        3. Authenticate with token
        4. Start keepalive and message receiving tasks
        """
        try:
            # Connect to WebSocket
            logger.info(f"Connecting to {self.websocket_url}")
            self._websocket = await websockets.connect(self.websocket_url)
            self._is_connected = True
            logger.info("WebSocket connected")

            # Send SETUP message
            setup_msg = SetupMessage(
                keepalive_timeout=self.keepalive_timeout,
                accept_keepalive_timeout=self.keepalive_timeout,
            )
            await self.send_message(setup_msg)
            logger.info("SETUP message sent")

            # Wait for server SETUP response
            response = await self._receive_raw_message()
            if response and response.get("type") == "SETUP":
                logger.info("Received SETUP response from server")

            # Check if auth is required
            auth_state_msg = await self._receive_raw_message()
            if (
                auth_state_msg
                and auth_state_msg.get("type") == "AUTH_STATE"
                and auth_state_msg.get("state") == "UNAUTHORIZED"
            ):
                logger.info("Authentication required, sending AUTH message")
                # Send AUTH message
                auth_msg = AuthMessage(self.auth_token)
                await self.send_message(auth_msg)

                # Wait for AUTH_STATE response
                auth_response = await self._receive_raw_message()
                if (
                    auth_response
                    and auth_response.get("type") == "AUTH_STATE"
                    and auth_response.get("state") == "AUTHORIZED"
                ):
                    self._is_authenticated = True
                    logger.info(
                        f"Authenticated as user {auth_response.get('userId', 'unknown')}"
                    )
                else:
                    raise RuntimeError("Authentication failed")
            else:
                # No auth required
                self._is_authenticated = True
                logger.info("No authentication required")

            # Start background tasks
            self._keepalive_task = asyncio.create_task(self._keepalive_loop())
            self._receive_task = asyncio.create_task(self._receive_loop())

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            await self.disconnect()
            raise

    async def disconnect(self) -> None:
        """Disconnect from the WebSocket server and clean up."""
        logger.info("Disconnecting...")
        self._is_connected = False
        self._is_authenticated = False

        # Cancel background tasks
        if self._keepalive_task:
            self._keepalive_task.cancel()
            try:
                await self._keepalive_task
            except asyncio.CancelledError:
                pass

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        # Close WebSocket
        if self._websocket:
            await self._websocket.close()
            self._websocket = None

        logger.info("Disconnected")

    async def send_message(self, message: Message) -> None:
        """
        Send a message to the DXLink server.

        Args:
            message: The message to send.

        Raises:
            RuntimeError: If not connected.
        """
        if not self._websocket or not self._is_connected:
            raise RuntimeError("Not connected to WebSocket")

        data = json.dumps(message.to_dict())
        await self._websocket.send(data)
        logger.debug(f"Sent: {data}")

    async def _receive_raw_message(self) -> dict[str, Any] | None:
        """
        Receive a raw message from the WebSocket.

        Returns:
            The parsed JSON message or None if connection closed.
        """
        if not self._websocket:
            return None

        try:
            data = await self._websocket.recv()
            message = json.loads(data)
            logger.debug(f"Received: {data}")
            return message
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection closed")
            self._is_connected = False
            return None
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            return None

    async def _receive_loop(self) -> None:
        """Background task to continuously receive and route messages."""
        while self._is_connected:
            try:
                raw_msg = await self._receive_raw_message()
                if not raw_msg:
                    break

                # Parse and route message
                message = parse_message(raw_msg)
                await self._route_message(message)

            except Exception as e:
                logger.error(f"Error in receive loop: {e}")
                break

    async def _route_message(self, message: Message) -> None:
        """
        Route a received message to registered handlers.

        Args:
            message: The message to route.
        """
        handlers = self._message_handlers.get(message.type, [])
        for handler in handlers:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"Error in message handler: {e}")

    def register_handler(
        self, message_type: MessageType, handler: Callable[[Message], None]
    ) -> None:
        """
        Register a handler for a specific message type.

        Args:
            message_type: The type of message to handle.
            handler: The callback function to handle the message.
        """
        if message_type not in self._message_handlers:
            self._message_handlers[message_type] = []
        self._message_handlers[message_type].append(handler)

    def unregister_handler(
        self, message_type: MessageType, handler: Callable[[Message], None]
    ) -> None:
        """
        Unregister a handler for a specific message type.

        Args:
            message_type: The type of message.
            handler: The handler to remove.
        """
        if message_type in self._message_handlers:
            try:
                self._message_handlers[message_type].remove(handler)
            except ValueError:
                pass

    async def _keepalive_loop(self) -> None:
        """Background task to send keepalive messages."""
        # Send keepalive at half the timeout interval
        interval = self.keepalive_timeout / 2

        while self._is_connected:
            try:
                await asyncio.sleep(interval)
                if self._is_connected:
                    keepalive_msg = KeepaliveMessage()
                    await self.send_message(keepalive_msg)
                    logger.debug("Sent keepalive")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error sending keepalive: {e}")

    async def __aenter__(self):
        """Context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.disconnect()
