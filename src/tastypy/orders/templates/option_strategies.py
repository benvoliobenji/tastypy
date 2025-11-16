"""Easy-to-use templates for common option strategies.

This module provides simple template functions that construct complex option orders
using trader-friendly terminology. Each template returns an OrderBuilder that can be
further customized before placing.

Example:
    >>> from datetime import date
    >>> from tastypy.orders.templates import bull_call_spread
    >>> order = bull_call_spread(
    ...     underlying="AAPL",
    ...     long_strike=150.0,
    ...     short_strike=155.0,
    ...     expiration=date(2025, 12, 19),
    ...     quantity=1,
    ...     limit_price=2.50
    ... )
    >>> response = orders.place_order(order)
"""

import datetime

from ..common.order_builder import OrderBuilder, OrderLegBuilder


def _format_expiration(expiration: datetime.date | datetime.datetime | str) -> str:
    """
    Convert expiration date to YYMMDD format string.

    Args:
        expiration: Either a date/datetime object or a YYMMDD format string

    Returns:
        Expiration date in YYMMDD format (e.g., "251219" for Dec 19, 2025)

    Example:
        >>> from datetime import date
        >>> _format_expiration(date(2025, 12, 19))
        '251219'
        >>> _format_expiration("251219")
        '251219'
    """
    if isinstance(expiration, str):
        # Already in YYMMDD format, return as-is
        return expiration
    elif isinstance(expiration, (datetime.date, datetime.datetime)):
        # Convert date/datetime to YYMMDD format
        return expiration.strftime("%y%m%d")
    else:
        raise TypeError(
            f"expiration must be a date, datetime, or YYMMDD string, got {type(expiration)}"
        )


def _build_option_symbol(
    underlying: str,
    expiration: datetime.date | datetime.datetime | str,
    option_type: str,
    strike: float,
) -> str:
    """
    Build an OCC option symbol.

    Args:
        underlying: The underlying stock symbol (e.g., "AAPL")
        expiration: Expiration date as date/datetime object or YYMMDD string
        option_type: "C" for call or "P" for put
        strike: Strike price (e.g., 150.0)

    Returns:
        OCC formatted option symbol (e.g., "AAPL  251219C00150000")
    """
    # OCC format: SYMBOL(6 chars) YYMMDD C/P Strike(8 chars with 3 decimal places)
    expiration_str = _format_expiration(expiration)
    padded_symbol = underlying.ljust(6)
    strike_str = f"{int(strike * 1000):08d}"
    return f"{padded_symbol}{expiration_str}{option_type}{strike_str}"


# ============================================================================
# VERTICAL SPREADS
# ============================================================================


def bull_call_spread(
    underlying: str,
    long_strike: float,
    short_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Bull Call Spread (debit spread).

    A bullish strategy that profits from moderate upward price movement.
    Buy a lower strike call and sell a higher strike call.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        long_strike: Strike price of the call to buy (lower strike)
        short_strike: Strike price of the call to sell (higher strike)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of spreads (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Buy AAPL 150/155 bull call spread for $2.50
        >>> order = bull_call_spread("AAPL", 150.0, 155.0, date(2025, 12, 19), 1, 2.50)
    """
    long_call_symbol = _build_option_symbol(underlying, expiration, "C", long_strike)
    short_call_symbol = _build_option_symbol(underlying, expiration, "C", short_strike)

    long_leg = (
        OrderLegBuilder()
        .equity_option(long_call_symbol)
        .quantity(quantity)
        .buy_to_open()
    )
    short_leg = (
        OrderLegBuilder()
        .equity_option(short_call_symbol)
        .quantity(quantity)
        .sell_to_open()
    )

    order = OrderBuilder().add_leg(long_leg).add_leg(short_leg).day().debit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def bear_call_spread(
    underlying: str,
    short_strike: float,
    long_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Bear Call Spread (credit spread).

    A bearish/neutral strategy that profits if the underlying stays below the short strike.
    Sell a lower strike call and buy a higher strike call.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        short_strike: Strike price of the call to sell (lower strike)
        long_strike: Strike price of the call to buy (higher strike)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of spreads (default: 1)
        limit_price: Minimum credit to receive (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Sell AAPL 155/160 bear call spread for $1.50 credit
        >>> order = bear_call_spread("AAPL", 155.0, 160.0, date(2025, 12, 19), 1, 1.50)
    """
    short_call_symbol = _build_option_symbol(underlying, expiration, "C", short_strike)
    long_call_symbol = _build_option_symbol(underlying, expiration, "C", long_strike)

    short_leg = (
        OrderLegBuilder()
        .equity_option(short_call_symbol)
        .quantity(quantity)
        .sell_to_open()
    )
    long_leg = (
        OrderLegBuilder()
        .equity_option(long_call_symbol)
        .quantity(quantity)
        .buy_to_open()
    )

    order = OrderBuilder().add_leg(short_leg).add_leg(long_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def bull_put_spread(
    underlying: str,
    short_strike: float,
    long_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Bull Put Spread (credit spread).

    A bullish/neutral strategy that profits if the underlying stays above the short strike.
    Sell a higher strike put and buy a lower strike put.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        short_strike: Strike price of the put to sell (higher strike)
        long_strike: Strike price of the put to buy (lower strike)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of spreads (default: 1)
        limit_price: Minimum credit to receive (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Sell AAPL 145/140 bull put spread for $1.25 credit
        >>> order = bull_put_spread("AAPL", 145.0, 140.0, date(2025, 12, 19), 1, 1.25)
    """
    short_put_symbol = _build_option_symbol(underlying, expiration, "P", short_strike)
    long_put_symbol = _build_option_symbol(underlying, expiration, "P", long_strike)

    short_leg = (
        OrderLegBuilder()
        .equity_option(short_put_symbol)
        .quantity(quantity)
        .sell_to_open()
    )
    long_leg = (
        OrderLegBuilder()
        .equity_option(long_put_symbol)
        .quantity(quantity)
        .buy_to_open()
    )

    order = OrderBuilder().add_leg(short_leg).add_leg(long_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def bear_put_spread(
    underlying: str,
    long_strike: float,
    short_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Bear Put Spread (debit spread).

    A bearish strategy that profits from moderate downward price movement.
    Buy a higher strike put and sell a lower strike put.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        long_strike: Strike price of the put to buy (higher strike)
        short_strike: Strike price of the put to sell (lower strike)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of spreads (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Buy AAPL 150/145 bear put spread for $2.00
        >>> order = bear_put_spread("AAPL", 150.0, 145.0, date(2025, 12, 19), 1, 2.00)
    """
    long_put_symbol = _build_option_symbol(underlying, expiration, "P", long_strike)
    short_put_symbol = _build_option_symbol(underlying, expiration, "P", short_strike)

    long_leg = (
        OrderLegBuilder()
        .equity_option(long_put_symbol)
        .quantity(quantity)
        .buy_to_open()
    )
    short_leg = (
        OrderLegBuilder()
        .equity_option(short_put_symbol)
        .quantity(quantity)
        .sell_to_open()
    )

    order = OrderBuilder().add_leg(long_leg).add_leg(short_leg).day().debit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# IRON CONDOR
# ============================================================================


def iron_condor(
    underlying: str,
    put_long_strike: float,
    put_short_strike: float,
    call_short_strike: float,
    call_long_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create an Iron Condor (credit spread).

    A neutral strategy that profits when the underlying stays within a range.
    Combines a bull put spread and a bear call spread.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        put_long_strike: Long put strike (lowest strike)
        put_short_strike: Short put strike (lower middle strike)
        call_short_strike: Short call strike (upper middle strike)
        call_long_strike: Long call strike (highest strike)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of iron condors (default: 1)
        limit_price: Minimum credit to receive (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL iron condor: 140/145/155/160 for $2.00 credit
        >>> order = iron_condor("AAPL", 140.0, 145.0, 155.0, 160.0, date(2025, 12, 19), 1, 2.00)
    """
    # Bull put spread (lower strikes)
    long_put_symbol = _build_option_symbol(underlying, expiration, "P", put_long_strike)
    short_put_symbol = _build_option_symbol(
        underlying, expiration, "P", put_short_strike
    )

    # Bear call spread (upper strikes)
    short_call_symbol = _build_option_symbol(
        underlying, expiration, "C", call_short_strike
    )
    long_call_symbol = _build_option_symbol(
        underlying, expiration, "C", call_long_strike
    )

    # Build legs
    long_put_leg = (
        OrderLegBuilder()
        .equity_option(long_put_symbol)
        .quantity(quantity)
        .buy_to_open()
    )
    short_put_leg = (
        OrderLegBuilder()
        .equity_option(short_put_symbol)
        .quantity(quantity)
        .sell_to_open()
    )
    short_call_leg = (
        OrderLegBuilder()
        .equity_option(short_call_symbol)
        .quantity(quantity)
        .sell_to_open()
    )
    long_call_leg = (
        OrderLegBuilder()
        .equity_option(long_call_symbol)
        .quantity(quantity)
        .buy_to_open()
    )

    order = (
        OrderBuilder()
        .add_leg(long_put_leg)
        .add_leg(short_put_leg)
        .add_leg(short_call_leg)
        .add_leg(long_call_leg)
        .day()
        .credit()
    )

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# BUTTERFLY SPREAD
# ============================================================================


def call_butterfly(
    underlying: str,
    lower_strike: float,
    middle_strike: float,
    upper_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Call Butterfly Spread (debit spread).

    A neutral strategy that profits when the underlying stays near the middle strike.
    Buy 1 lower call, sell 2 middle calls, buy 1 upper call.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        lower_strike: Lowest strike price (buy 1)
        middle_strike: Middle strike price (sell 2)
        upper_strike: Highest strike price (buy 1)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of butterflies (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL 145/150/155 call butterfly for $1.00
        >>> order = call_butterfly("AAPL", 145.0, 150.0, 155.0, date(2025, 12, 19), 1, 1.00)
    """
    lower_call_symbol = _build_option_symbol(underlying, expiration, "C", lower_strike)
    middle_call_symbol = _build_option_symbol(
        underlying, expiration, "C", middle_strike
    )
    upper_call_symbol = _build_option_symbol(underlying, expiration, "C", upper_strike)

    lower_leg = (
        OrderLegBuilder()
        .equity_option(lower_call_symbol)
        .quantity(quantity)
        .buy_to_open()
    )
    middle_leg = (
        OrderLegBuilder()
        .equity_option(middle_call_symbol)
        .quantity(quantity * 2)
        .sell_to_open()
    )
    upper_leg = (
        OrderLegBuilder()
        .equity_option(upper_call_symbol)
        .quantity(quantity)
        .buy_to_open()
    )

    order = (
        OrderBuilder()
        .add_leg(lower_leg)
        .add_leg(middle_leg)
        .add_leg(upper_leg)
        .day()
        .debit()
    )

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def put_butterfly(
    underlying: str,
    lower_strike: float,
    middle_strike: float,
    upper_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Put Butterfly Spread (debit spread).

    A neutral strategy that profits when the underlying stays near the middle strike.
    Buy 1 lower put, sell 2 middle puts, buy 1 upper put.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        lower_strike: Lowest strike price (buy 1)
        middle_strike: Middle strike price (sell 2)
        upper_strike: Highest strike price (buy 1)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of butterflies (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL 145/150/155 put butterfly for $1.00
        >>> order = put_butterfly("AAPL", 145.0, 150.0, 155.0, date(2025, 12, 19), 1, 1.00)
    """
    lower_put_symbol = _build_option_symbol(underlying, expiration, "P", lower_strike)
    middle_put_symbol = _build_option_symbol(underlying, expiration, "P", middle_strike)
    upper_put_symbol = _build_option_symbol(underlying, expiration, "P", upper_strike)

    lower_leg = (
        OrderLegBuilder()
        .equity_option(lower_put_symbol)
        .quantity(quantity)
        .buy_to_open()
    )
    middle_leg = (
        OrderLegBuilder()
        .equity_option(middle_put_symbol)
        .quantity(quantity * 2)
        .sell_to_open()
    )
    upper_leg = (
        OrderLegBuilder()
        .equity_option(upper_put_symbol)
        .quantity(quantity)
        .buy_to_open()
    )

    order = (
        OrderBuilder()
        .add_leg(lower_leg)
        .add_leg(middle_leg)
        .add_leg(upper_leg)
        .day()
        .debit()
    )

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# CALENDAR SPREAD
# ============================================================================


def call_calendar_spread(
    underlying: str,
    strike: float,
    near_expiration: datetime.date | datetime.datetime | str,
    far_expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Call Calendar Spread (debit spread).

    A neutral strategy that profits from time decay.
    Sell a near-term call and buy a longer-term call at the same strike.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        strike: Strike price for both options
        near_expiration: Near-term expiration as date/datetime object or YYMMDD string
        far_expiration: Far-term expiration as date/datetime object or YYMMDD string
        quantity: Number of spreads (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL 150 call calendar: sell Dec, buy Jan for $2.50
        >>> order = call_calendar_spread("AAPL", 150.0, date(2025, 12, 19), date(2026, 1, 16), 1, 2.50)
    """
    near_call_symbol = _build_option_symbol(underlying, near_expiration, "C", strike)
    far_call_symbol = _build_option_symbol(underlying, far_expiration, "C", strike)

    near_leg = (
        OrderLegBuilder()
        .equity_option(near_call_symbol)
        .quantity(quantity)
        .sell_to_open()
    )
    far_leg = (
        OrderLegBuilder()
        .equity_option(far_call_symbol)
        .quantity(quantity)
        .buy_to_open()
    )

    order = OrderBuilder().add_leg(near_leg).add_leg(far_leg).day().debit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def put_calendar_spread(
    underlying: str,
    strike: float,
    near_expiration: datetime.date | datetime.datetime | str,
    far_expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Put Calendar Spread (debit spread).

    A neutral strategy that profits from time decay.
    Sell a near-term put and buy a longer-term put at the same strike.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        strike: Strike price for both options
        near_expiration: Near-term expiration as date/datetime object or YYMMDD string
        far_expiration: Far-term expiration as date/datetime object or YYMMDD string
        quantity: Number of spreads (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL 150 put calendar: sell Dec, buy Jan for $2.50
        >>> order = put_calendar_spread("AAPL", 150.0, date(2025, 12, 19), date(2026, 1, 16), 1, 2.50)
    """
    near_put_symbol = _build_option_symbol(underlying, near_expiration, "P", strike)
    far_put_symbol = _build_option_symbol(underlying, far_expiration, "P", strike)

    near_leg = (
        OrderLegBuilder()
        .equity_option(near_put_symbol)
        .quantity(quantity)
        .sell_to_open()
    )
    far_leg = (
        OrderLegBuilder().equity_option(far_put_symbol).quantity(quantity).buy_to_open()
    )

    order = OrderBuilder().add_leg(near_leg).add_leg(far_leg).day().debit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# COVERED STRATEGIES
# ============================================================================


def covered_call(
    underlying: str,
    strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Covered Call.

    Requires owning 100 shares per contract. Sell calls against existing long stock.
    This template only creates the short call order - assumes stock is already owned.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        strike: Strike price of the call to sell
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of contracts (default: 1, requires 100 shares per contract)
        limit_price: Minimum credit per contract (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Sell covered call on 100 shares of AAPL at $155 for $2.50
        >>> order = covered_call("AAPL", 155.0, date(2025, 12, 19), 1, 2.50)
    """
    call_symbol = _build_option_symbol(underlying, expiration, "C", strike)

    call_leg = (
        OrderLegBuilder().equity_option(call_symbol).quantity(quantity).sell_to_open()
    )

    order = OrderBuilder().add_leg(call_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def covered_put(
    underlying: str,
    strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Covered Put (Cash-Secured Put).

    Sell puts with cash reserved to buy the stock if assigned.
    This template only creates the short put order - assumes sufficient cash.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        strike: Strike price of the put to sell
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of contracts (default: 1, requires cash for 100 shares per contract)
        limit_price: Minimum credit per contract (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Sell cash-secured put on AAPL at $145 for $2.00
        >>> order = covered_put("AAPL", 145.0, date(2025, 12, 19), 1, 2.00)
    """
    put_symbol = _build_option_symbol(underlying, expiration, "P", strike)

    put_leg = (
        OrderLegBuilder().equity_option(put_symbol).quantity(quantity).sell_to_open()
    )

    order = OrderBuilder().add_leg(put_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# RATIO SPREAD
# ============================================================================


def call_ratio_spread(
    underlying: str,
    long_strike: float,
    short_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    long_quantity: int = 1,
    short_quantity: int = 2,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Call Ratio Spread.

    Buy calls at a lower strike and sell more calls at a higher strike.
    Typically done for a credit or small debit. Unlimited risk above short strike.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        long_strike: Strike price of calls to buy (lower)
        short_strike: Strike price of calls to sell (higher)
        expiration: Expiration date as date/datetime object or YYMMDD string
        long_quantity: Number of long calls (default: 1)
        short_quantity: Number of short calls (default: 2)
        limit_price: Net credit/debit limit (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL 150/155 call ratio spread: buy 1, sell 2
        >>> order = call_ratio_spread("AAPL", 150.0, 155.0, date(2025, 12, 19), 1, 2, 0.50)
    """
    long_call_symbol = _build_option_symbol(underlying, expiration, "C", long_strike)
    short_call_symbol = _build_option_symbol(underlying, expiration, "C", short_strike)

    long_leg = (
        OrderLegBuilder()
        .equity_option(long_call_symbol)
        .quantity(long_quantity)
        .buy_to_open()
    )
    short_leg = (
        OrderLegBuilder()
        .equity_option(short_call_symbol)
        .quantity(short_quantity)
        .sell_to_open()
    )

    # Ratio spreads can be credit or debit depending on strikes and quantities
    # Default to credit if receiving money
    order = OrderBuilder().add_leg(long_leg).add_leg(short_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def put_ratio_spread(
    underlying: str,
    long_strike: float,
    short_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    long_quantity: int = 1,
    short_quantity: int = 2,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Put Ratio Spread.

    Buy puts at a higher strike and sell more puts at a lower strike.
    Typically done for a credit or small debit. Significant risk below short strike.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        long_strike: Strike price of puts to buy (higher)
        short_strike: Strike price of puts to sell (lower)
        expiration: Expiration date as date/datetime object or YYMMDD string
        long_quantity: Number of long puts (default: 1)
        short_quantity: Number of short puts (default: 2)
        limit_price: Net credit/debit limit (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL 150/145 put ratio spread: buy 1, sell 2
        >>> order = put_ratio_spread("AAPL", 150.0, 145.0, date(2025, 12, 19), 1, 2, 0.50)
    """
    long_put_symbol = _build_option_symbol(underlying, expiration, "P", long_strike)
    short_put_symbol = _build_option_symbol(underlying, expiration, "P", short_strike)

    long_leg = (
        OrderLegBuilder()
        .equity_option(long_put_symbol)
        .quantity(long_quantity)
        .buy_to_open()
    )
    short_leg = (
        OrderLegBuilder()
        .equity_option(short_put_symbol)
        .quantity(short_quantity)
        .sell_to_open()
    )

    # Ratio spreads can be credit or debit depending on strikes and quantities
    order = OrderBuilder().add_leg(long_leg).add_leg(short_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# STRADDLE
# ============================================================================


def long_straddle(
    underlying: str,
    strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Long Straddle (debit spread).

    Buy both a call and a put at the same strike. Profits from large moves in either direction.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        strike: Strike price for both call and put
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of straddles (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Buy AAPL 150 straddle for $10.00
        >>> order = long_straddle("AAPL", 150.0, date(2025, 12, 19), 1, 10.00)
    """
    call_symbol = _build_option_symbol(underlying, expiration, "C", strike)
    put_symbol = _build_option_symbol(underlying, expiration, "P", strike)

    call_leg = (
        OrderLegBuilder().equity_option(call_symbol).quantity(quantity).buy_to_open()
    )
    put_leg = (
        OrderLegBuilder().equity_option(put_symbol).quantity(quantity).buy_to_open()
    )

    order = OrderBuilder().add_leg(call_leg).add_leg(put_leg).day().debit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def short_straddle(
    underlying: str,
    strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Short Straddle (credit spread).

    Sell both a call and a put at the same strike. Profits when underlying stays near strike.
    Unlimited risk - use with caution!

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        strike: Strike price for both call and put
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of straddles (default: 1)
        limit_price: Minimum credit to receive (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Sell AAPL 150 straddle for $10.00 credit
        >>> order = short_straddle("AAPL", 150.0, date(2025, 12, 19), 1, 10.00)
    """
    call_symbol = _build_option_symbol(underlying, expiration, "C", strike)
    put_symbol = _build_option_symbol(underlying, expiration, "P", strike)

    call_leg = (
        OrderLegBuilder().equity_option(call_symbol).quantity(quantity).sell_to_open()
    )
    put_leg = (
        OrderLegBuilder().equity_option(put_symbol).quantity(quantity).sell_to_open()
    )

    order = OrderBuilder().add_leg(call_leg).add_leg(put_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# STRANGLE
# ============================================================================


def long_strangle(
    underlying: str,
    put_strike: float,
    call_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Long Strangle (debit spread).

    Buy an out-of-the-money put and an out-of-the-money call.
    Profits from large moves in either direction, cheaper than straddle.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        put_strike: Strike price of the put to buy (lower)
        call_strike: Strike price of the call to buy (higher)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of strangles (default: 1)
        limit_price: Maximum debit to pay (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Buy AAPL 145/155 strangle for $6.00
        >>> order = long_strangle("AAPL", 145.0, 155.0, date(2025, 12, 19), 1, 6.00)
    """
    put_symbol = _build_option_symbol(underlying, expiration, "P", put_strike)
    call_symbol = _build_option_symbol(underlying, expiration, "C", call_strike)

    put_leg = (
        OrderLegBuilder().equity_option(put_symbol).quantity(quantity).buy_to_open()
    )
    call_leg = (
        OrderLegBuilder().equity_option(call_symbol).quantity(quantity).buy_to_open()
    )

    order = OrderBuilder().add_leg(put_leg).add_leg(call_leg).day().debit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


def short_strangle(
    underlying: str,
    put_strike: float,
    call_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Short Strangle (credit spread).

    Sell an out-of-the-money put and an out-of-the-money call.
    Profits when underlying stays between strikes. Unlimited risk - use with caution!

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        put_strike: Strike price of the put to sell (lower)
        call_strike: Strike price of the call to sell (higher)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of strangles (default: 1)
        limit_price: Minimum credit to receive (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # Sell AAPL 145/155 strangle for $6.00 credit
        >>> order = short_strangle("AAPL", 145.0, 155.0, date(2025, 12, 19), 1, 6.00)
    """
    put_symbol = _build_option_symbol(underlying, expiration, "P", put_strike)
    call_symbol = _build_option_symbol(underlying, expiration, "C", call_strike)

    put_leg = (
        OrderLegBuilder().equity_option(put_symbol).quantity(quantity).sell_to_open()
    )
    call_leg = (
        OrderLegBuilder().equity_option(call_symbol).quantity(quantity).sell_to_open()
    )

    order = OrderBuilder().add_leg(put_leg).add_leg(call_leg).day().credit()

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order


# ============================================================================
# JADE LIZARD
# ============================================================================


def jade_lizard(
    underlying: str,
    put_strike: float,
    call_short_strike: float,
    call_long_strike: float,
    expiration: datetime.date | datetime.datetime | str,
    quantity: int = 1,
    limit_price: float | None = None,
) -> OrderBuilder:
    """
    Create a Jade Lizard (credit spread).

    A bullish/neutral strategy combining a short put and a bear call spread.
    Sell a put and sell a call vertical spread. Credit received should exceed
    the width of the call spread for no upside risk.

    Args:
        underlying: Stock symbol (e.g., "AAPL")
        put_strike: Strike price of the put to sell
        call_short_strike: Strike price of the call to sell (lower)
        call_long_strike: Strike price of the call to buy (higher)
        expiration: Expiration date as date/datetime object or YYMMDD string
        quantity: Number of jade lizards (default: 1)
        limit_price: Minimum credit to receive (optional)

    Returns:
        OrderBuilder ready to place

    Example:
        >>> from datetime import date
        >>> # AAPL jade lizard: sell 140 put, sell 155/160 call spread for $6.00
        >>> order = jade_lizard("AAPL", 140.0, 155.0, 160.0, date(2025, 12, 19), 1, 6.00)
    """
    put_symbol = _build_option_symbol(underlying, expiration, "P", put_strike)
    short_call_symbol = _build_option_symbol(
        underlying, expiration, "C", call_short_strike
    )
    long_call_symbol = _build_option_symbol(
        underlying, expiration, "C", call_long_strike
    )

    put_leg = (
        OrderLegBuilder().equity_option(put_symbol).quantity(quantity).sell_to_open()
    )
    short_call_leg = (
        OrderLegBuilder()
        .equity_option(short_call_symbol)
        .quantity(quantity)
        .sell_to_open()
    )
    long_call_leg = (
        OrderLegBuilder()
        .equity_option(long_call_symbol)
        .quantity(quantity)
        .buy_to_open()
    )

    order = (
        OrderBuilder()
        .add_leg(put_leg)
        .add_leg(short_call_leg)
        .add_leg(long_call_leg)
        .day()
        .credit()
    )

    if limit_price is not None:
        order.limit(limit_price)
    else:
        order.market()

    return order
