import datetime


def format_datetime_with_local(dt: datetime.datetime | None) -> tuple[str, str]:
    """
    Format a datetime as both UTC and local timezone.

    Args:
        dt: Datetime to format.

    Returns:
        Tuple of (utc_string, local_string).
    """
    if dt is None:
        return ("", "")

    utc_str = dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    # Convert to local timezone
    local_dt = dt.astimezone()
    local_str = local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    return (utc_str, local_str)
