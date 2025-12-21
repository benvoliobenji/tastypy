"""Format of data in DOM_SNAPSHOT messages."""

from enum import Enum


class DomDataFormat(str, Enum):
    """Format of data in DOM_SNAPSHOT messages."""

    FULL = "FULL"
    COMPACT = "COMPACT"
