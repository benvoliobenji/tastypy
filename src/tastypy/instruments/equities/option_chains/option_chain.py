"""
Helper functions for fetching equity option chains.

These functions provide convenient access to option chain data in different formats.
"""

import datetime
from collections import defaultdict
from ..options.equity_option import EquityOption
from ....session import Session
from ....errors import translate_error_code


def get_option_chain(
    session: Session, symbol: str
) -> dict[datetime.date, list[EquityOption]]:
    """
    Returns a mapping of expiration date to a list of option objects
    representing the options chain for the given symbol.

    In the case that there are two expiries on the same day (e.g. SPXW and SPX AM
    options), both will be returned in the same list. If you just want one expiry,
    you'll need to filter the list yourself, or use NestedOptionChain instead.

    Args:
        session: The session to use for the request
        symbol: The symbol to get the option chain for (e.g., 'AAPL', 'SPY')

    Returns:
        A dictionary mapping expiration dates to lists of EquityOption objects
    """
    # URL encode forward slashes for symbols like indexes
    symbol = symbol.replace("/", "%2F")

    response = session._client.get(f"/option-chains/{symbol}")

    if response.status_code == 200:
        data = response.json()
        chain: dict[datetime.date, list[EquityOption]] = defaultdict(list)

        for item in data.get("data", {}).get("items", []):
            option = EquityOption(item)
            if option.expiration_date:
                chain[option.expiration_date].append(option)

        return dict(chain)
    else:
        error_code = response.status_code
        error_message = response.json().get("error", {}).get("message", "")
        raise translate_error_code(error_code, error_message)
