import datetime


def parse_float(value: float | str | None, default: float = 0.0) -> float:
    """Parse a float value from API response with fallback.

    Args:
        value: Value from API that might be float, str, or None
        default: Default value to return if parsing fails

    Returns:
        Parsed float or default value
    """
    if value is not None:
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    return default


def parse_json_double(value: str | None, default: float = 0.0) -> float:
    """Parse a float value encoded as JSON double string with fallback.

    Handles NaN, Infinity, and -Infinity strings.

    Args:
        value: JSON double string from API or None
        default: Default value to return if parsing fails

    Returns:
        Parsed float or default value
    """
    if value is not None:
        try:
            if value == "NaN":
                return float("nan")
            elif value == "Infinity":
                return float("inf")
            elif value == "-Infinity":
                return float("-inf")
            else:
                return float(value)
        except (ValueError, TypeError):
            return default
    return default


def parse_int(value: int | str | None, default: int = 0) -> int:
    """Parse an integer value from API response with fallback.

    Args:
        value: Value from API that might be int, str, or None
        default: Default value to return if parsing fails

    Returns:
        Parsed int or default value
    """
    if value is not None:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    return default


def parse_datetime(value: str | None) -> datetime.datetime | None:
    """Parse a datetime from ISO 8601 string.

    Args:
        value: ISO 8601 datetime string from API or None

    Returns:
        Parsed datetime or None
    """
    if value:
        try:
            # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
            return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def parse_date(value: str | None) -> datetime.date | None:
    """Parse a date from ISO 8601 date string.

    Args:
        value: ISO 8601 date string from API or None
    Returns:
        Parsed date or None
    """
    if value:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    return None
