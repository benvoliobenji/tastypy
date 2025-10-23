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
