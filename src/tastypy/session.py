"""OAuth2 session management for TastyTrade API."""

import datetime
import importlib.metadata
from typing import Any

import httpx

from .errors import translate_error_code


class Session:
    """
    OAuth2-based session for TastyTrade API authentication.

    This class handles OAuth2 authentication using client secret and refresh token.
    Access tokens are automatically refreshed when they expire (every 15 minutes).

    For personal use:
        Follow the steps in the OAuth2 Quick Start Guide to obtain your
        client secret and refresh token.

    For trusted partners:
        Follow the authorization code flow documented in TastyTrade's official OAuth2 guide.

    Example:
        >>> # Basic usage with OAuth2
        >>> session = Session(
        ...     client_secret="your_client_secret",
        ...     refresh_token="your_refresh_token"
        ... )
        >>> # Access token is automatically generated on first API call
        >>> accounts = session.client.get("/customers/me/accounts")

        >>> # Manual refresh if needed (automatic in most cases)
        >>> session.refresh()
    """

    _oauth_token_url = "/oauth/token"
    _version: str = importlib.metadata.version("tastypy")
    _headers: dict[str, str] = {"User-Agent": f"tastypy/{_version}"}

    def __init__(
        self,
        client_secret: str,
        refresh_token: str,
        base_url: str = "https://api.tastyworks.com",
    ) -> None:
        """
        Initialize an OAuth2 session.

        Args:
            client_secret: Your OAuth application's client secret.
            refresh_token: Long-lived refresh token from your OAuth grant.
            base_url: API base URL (prod or sandbox). Defaults to production.
        """
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._base_url = base_url
        self._access_token: str = ""
        self._token_expiration: datetime.datetime | None = None
        self._client: httpx.Client | None = None

    def _request_access_token(self) -> dict[str, Any]:
        """
        Request a new access token from the OAuth endpoint.

        Returns:
            Dictionary containing access_token and expires_in.

        Raises:
            Various exceptions via translate_error_code for failed requests.
        """
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "client_secret": self._client_secret,
        }

        response = httpx.post(
            f"{self._base_url}{self._oauth_token_url}",
            json=payload,
            headers=self._headers,
        )

        if response.status_code == 200:
            return response.json()
        else:
            error_message = (
                response.json().get("error", {}).get("message", response.text)
            )
            raise translate_error_code(response.status_code, error_message)

    def refresh(self) -> None:
        """
        Refresh the access token using the refresh token.

        This method is automatically called when needed, but can be manually
        invoked if desired. Access tokens last 15 minutes.

        Raises:
            Various exceptions via translate_error_code for failed requests.
        """
        token_data = self._request_access_token()

        self._access_token = token_data.get("access_token", "")
        expires_in = token_data.get("expires_in", 900)  # Default 15 minutes

        # Calculate expiration time (with 30 second buffer for safety)
        # Use UTC to avoid timezone issues when refreshing
        self._token_expiration = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(seconds=expires_in - 30)

        # Update or create the HTTP client with new access token
        auth_headers = {"Authorization": f"Bearer {self._access_token}"}
        auth_headers.update(self._headers)

        if self._client is not None:
            self._client.close()

        self._client = httpx.Client(base_url=self._base_url, headers=auth_headers)

    def is_logged_in(self) -> bool:
        """
        Check if the session has a valid access token.

        This checks if an access token exists and has not expired.

        Returns:
            True if access token is valid, False otherwise.
        """
        if not self._access_token or self._token_expiration is None:
            return False

        return datetime.datetime.now(datetime.timezone.utc) < self._token_expiration

    @property
    def client(self) -> httpx.Client:
        """
        Get the authenticated HTTP client.

        Automatically refreshes the access token if expired or not yet obtained.

        Returns:
            Configured httpx.Client with authentication headers.
        """
        if not self.is_logged_in():
            self.refresh()

        if self._client is None:
            self.refresh()

        return self._client  # type: ignore

    def is_sandbox(self) -> bool:
        """
        Check if the session is connected to the sandbox environment.

        Returns:
            True if using sandbox, False if using production.
        """
        return "cert.tastyworks" in self._base_url

    def close(self) -> None:
        """Close the HTTP client and clean up resources."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes the session."""
        self.close()

    def __del__(self):
        """Cleanup when object is garbage collected."""
        self.close()
