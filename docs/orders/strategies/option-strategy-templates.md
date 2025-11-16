# Option Strategy Templates

## Overview

TastyPy provides easy-to-use template functions for common option strategies.
These templates are designed to be beginner-friendly while using proper trader
terminology. Each template returns an `OrderBuilder` that can be further
customized before placing with the TastyTrade API.

## Quick Start

```python
from datetime import date
from tastypy.orders.templates import bull_call_spread

# Create a bull call spread
order = bull_call_spread(
    underlying="AAPL",
    long_strike=150.0,
    short_strike=155.0,
    expiration=date(2025, 12, 19),  # Dec 19, 2025
    quantity=1,
    limit_price=2.50
)

# Place the order (assumes you have a session and orders module set up)
response = orders.place_order(order)
```

## Available Strategies

### Vertical Spreads

- [Bull Call Spread](vertical-spreads.md#bull-call-spread) - Bullish debit
  spread
- [Bear Call Spread](vertical-spreads.md#bear-call-spread) - Bearish credit
  spread
- [Bull Put Spread](vertical-spreads.md#bull-put-spread) - Bullish credit spread
- [Bear Put Spread](vertical-spreads.md#bear-put-spread) - Bearish debit spread

### Multi-Leg Strategies

- [Iron Condor](iron-condor.md) - Neutral range-bound credit spread
- [Call Butterfly](butterfly-spreads.md#call-butterfly) - Neutral debit spread
- [Put Butterfly](butterfly-spreads.md#put-butterfly) - Neutral debit spread

### Time-Based Strategies

- [Call Calendar Spread](calendar-spreads.md#call-calendar-spread) - Time decay
  strategy
- [Put Calendar Spread](calendar-spreads.md#put-calendar-spread) - Time decay
  strategy

### Income Strategies

- [Covered Call](covered-strategies.md#covered-call) - Generate income on long
  stock
- [Covered Put](covered-strategies.md#covered-put) - Cash-secured put

### Advanced Strategies

- [Call Ratio Spread](ratio-spreads.md#call-ratio-spread) - Asymmetric call
  spread
- [Put Ratio Spread](ratio-spreads.md#put-ratio-spread) - Asymmetric put spread

### Volatility Strategies

- [Long Straddle](straddles.md#long-straddle) - Long volatility
- [Short Straddle](straddles.md#short-straddle) - Short volatility
- [Long Strangle](strangles.md#long-strangle) - Long volatility, wider range
- [Short Strangle](strangles.md#short-strangle) - Short volatility, wider range

### Specialty Strategies

- [Jade Lizard](jade-lizard.md) - Bullish credit spread with no upside risk

## Understanding Option Symbols

All templates use the OCC (Options Clearing Corporation) format for option
symbols:

```text
AAPL  251219C00150000
└─┬─┘ └──┬─┘│└───┬───┘
  │      │  │    └─ Strike price ($150.00 with 3 decimals = 00150000)
  │      │  └────── Option type (C = Call, P = Put)
  │      └───────── Expiration date (YYMMDD format: Dec 19, 2025)
  └──────────────── Symbol padded to 6 characters
```

### Expiration Date Format

Templates accept expiration dates in multiple formats for maximum flexibility:

**Using date objects (recommended):**

```python
from datetime import date, timedelta

# Specific date
expiration = date(2025, 12, 19)

# Relative date (e.g., 30 days from now)
expiration = date.today() + timedelta(days=30)
```

**Using datetime objects:**

```python
from datetime import datetime

expiration = datetime(2025, 12, 19, 16, 0, 0)  # Time component is ignored
```

**Using YYMMDD strings (backward compatible):**

```python
expiration = "251219"  # December 19, 2025
```

**Examples:**

- December 19, 2025 → `date(2025, 12, 19)` or `"251219"`
- January 16, 2026 → `date(2026, 1, 16)` or `"260116"`
- March 21, 2025 → `date(2025, 3, 21)` or `"250321"`

## Common Parameters

Most templates share these common parameters:

| Parameter     | Type                      | Description                             |
| ------------- | ------------------------- | --------------------------------------- |
| `underlying`  | `str`                     | Stock symbol (e.g., `"AAPL"`)           |
| `strike`      | `float`                   | Strike price (e.g., `150.0`)            |
| `expiration`  | `date \| datetime \| str` | Expiration date (date object or YYMMDD) |
| `quantity`    | `int`                     | Number of contracts (default: 1)        |
| `limit_price` | `float \| None`           | Limit price for the order (optional)    |

## Risk Considerations

### Defined Risk Strategies

- Vertical spreads (bull/bear call/put spreads)
- Iron condor
- Butterfly spreads
- Calendar spreads
- Long straddle/strangle

### Undefined Risk Strategies (Use with Caution!)

- Short straddle
- Short strangle
- Ratio spreads (partial undefined risk)
- Naked covered calls/puts

### Capital Requirements

- **Covered strategies**: Require stock ownership or cash reserves
  - Covered call: 100 shares per contract
  - Cash-secured put: Cash = strike × 100 × quantity
- **Spreads**: Margin = width of spread × 100 × quantity
- **Iron condor**: Margin = width of wider spread × 100 × quantity

## Order Execution

### Limit vs Market Orders

```python
from datetime import date

# With limit price (recommended for multi-leg strategies)
order = bull_call_spread("AAPL", 150.0, 155.0, date(2025, 12, 19), 1, limit_price=2.50)

# Market order (omit limit_price)
order = bull_call_spread("AAPL", 150.0, 155.0, date(2025, 12, 19), 1)
```

**Best Practice**: Always use limit orders for multi-leg strategies to avoid
poor fills.

### Time-in-Force

All templates default to **Day orders** (order expires at market close). To
change:

```python
from datetime import date

order = bull_call_spread("AAPL", 150.0, 155.0, date(2025, 12, 19), 1, 2.50)
order.gtc()  # Good-til-canceled
# or
order.day()  # Day order (default)
```

## Next Steps

- Explore specific strategies in the linked documentation pages
- Learn about [risk management best practices](risk-management.md)
- Understand [position sizing and Greeks](position-sizing.md)
- Read about [choosing the right strategy](strategy-selection.md)
