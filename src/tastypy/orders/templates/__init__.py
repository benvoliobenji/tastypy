"""Easy-to-use templates for common option trading strategies.

This module provides simple, trader-friendly functions to construct complex
option orders. All templates use standard option terminology (calls vs puts,
long vs short) and return OrderBuilder instances that can be further customized.

Available Strategy Templates:
    Vertical Spreads:
        - bull_call_spread: Buy lower call, sell higher call (debit)
        - bear_call_spread: Sell lower call, buy higher call (credit)
        - bull_put_spread: Sell higher put, buy lower put (credit)
        - bear_put_spread: Buy higher put, sell lower put (debit)

    Iron Condor:
        - iron_condor: Bull put spread + bear call spread (credit)

    Butterfly Spreads:
        - call_butterfly: Buy 1, sell 2, buy 1 calls (debit)
        - put_butterfly: Buy 1, sell 2, buy 1 puts (debit)

    Calendar Spreads:
        - call_calendar_spread: Sell near call, buy far call (debit)
        - put_calendar_spread: Sell near put, buy far put (debit)

    Covered Strategies:
        - covered_call: Sell call against long stock (credit)
        - covered_put: Sell put with cash secured (credit)

    Ratio Spreads:
        - call_ratio_spread: Buy calls, sell more calls (credit/debit)
        - put_ratio_spread: Buy puts, sell more puts (credit/debit)

    Straddles:
        - long_straddle: Buy call and put at same strike (debit)
        - short_straddle: Sell call and put at same strike (credit)

    Strangles:
        - long_strangle: Buy OTM put and call (debit)
        - short_strangle: Sell OTM put and call (credit)

    Jade Lizard:
        - jade_lizard: Short put + bear call spread (credit)

Example:
    >>> from tastypy.orders.templates import bull_call_spread
    >>> from tastypy.orders import Orders
    >>>
    >>> # Create a bull call spread order
    >>> order = bull_call_spread(
    ...     underlying="AAPL",
    ...     long_strike=150.0,
    ...     short_strike=155.0,
    ...     expiration="251219",
    ...     quantity=1,
    ...     limit_price=2.50
    ... )
    >>>
    >>> # Place the order
    >>> orders = Orders(session, account_number)
    >>> response = orders.place_order(order)
"""

from .option_strategies import (
    bear_call_spread,
    bear_put_spread,
    bull_call_spread,
    bull_put_spread,
    call_butterfly,
    call_calendar_spread,
    call_ratio_spread,
    covered_call,
    covered_put,
    iron_condor,
    jade_lizard,
    long_straddle,
    long_strangle,
    put_butterfly,
    put_calendar_spread,
    put_ratio_spread,
    short_straddle,
    short_strangle,
)

__all__ = [
    # Vertical Spreads
    "bull_call_spread",
    "bear_call_spread",
    "bull_put_spread",
    "bear_put_spread",
    # Iron Condor
    "iron_condor",
    # Butterfly Spreads
    "call_butterfly",
    "put_butterfly",
    # Calendar Spreads
    "call_calendar_spread",
    "put_calendar_spread",
    # Covered Strategies
    "covered_call",
    "covered_put",
    # Ratio Spreads
    "call_ratio_spread",
    "put_ratio_spread",
    # Straddles
    "long_straddle",
    "short_straddle",
    # Strangles
    "long_strangle",
    "short_strangle",
    # Jade Lizard
    "jade_lizard",
]
