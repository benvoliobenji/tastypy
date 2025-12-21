"""Types of services available in DXLink."""

from enum import Enum


class ServiceType(str, Enum):
    """Types of services available in DXLink."""

    FEED = "FEED"
    DOM = "DOM"
