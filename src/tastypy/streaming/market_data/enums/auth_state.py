"""Authentication states in the DXLink protocol."""

from enum import Enum


class AuthState(str, Enum):
    """Authentication states in the DXLink protocol."""

    AUTHORIZED = "AUTHORIZED"
    UNAUTHORIZED = "UNAUTHORIZED"
