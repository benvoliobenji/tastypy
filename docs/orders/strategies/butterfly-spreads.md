# Butterfly Spreads

Butterfly spreads are neutral strategies that profit when the underlying stays
near a specific price (the middle strike) at expiration.

## Call Butterfly

**Market Outlook**: Neutral (expecting minimal movement)

**Risk Profile**: Defined risk, defined reward

### Strategy Overview

A call butterfly uses three strikes with the same expiration. Buy one lower
call, sell two middle calls, buy one upper call. All strikes are equidistant.

- **Buy**: 1 lower strike call
- **Sell**: 2 middle strike calls
- **Buy**: 1 upper strike call
- **Net Cost**: Debit (small premium paid)
- **Max Profit**: Width between strikes - net debit
- **Max Loss**: Net debit paid
- **Breakeven**: Two points - near lower and upper strikes

### When to Use

- Expecting very little movement in the underlying
- Want to profit from time decay in a specific price zone
- Lower cost alternative to iron condor
- When implied volatility is elevated

### Code Example

```python
from datetime import date
from tastypy.orders.templates import call_butterfly

# AAPL at $150, expecting it to stay right around $150
order = call_butterfly(
    underlying="AAPL",
    lower_strike=145.0,   # Buy 1 call
    middle_strike=150.0,  # Sell 2 calls
    upper_strike=155.0,   # Buy 1 call
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=1.00      # Pay max $1.00
)
```

### Example P&L Scenarios

Assume AAPL at $150, buy 145/150/155 call butterfly for $1.00:

| AAPL Price at Expiration | P&L   | Notes                                   |
| ------------------------ | ----- | --------------------------------------- |
| $140                     | -$100 | Max loss (all options expire worthless) |
| $146                     | $0    | Lower breakeven                         |
| $150                     | +$400 | Max profit (exactly at middle strike)   |
| $154                     | $0    | Upper breakeven                         |
| $160                     | -$100 | Max loss (spreads offset)               |

### Greeks Profile

- **Delta**: Near zero initially, changes as price moves away from middle
- **Theta**: Positive when near middle strike (benefits from time decay)
- **Vega**: Negative near middle, positive at wings
- **Gamma**: Negative at middle strike, positive at wings

---

## Put Butterfly

**Market Outlook**: Neutral (expecting minimal movement)

**Risk Profile**: Defined risk, defined reward

### Strategy Overview

Same structure as call butterfly but using puts. Equivalent risk/reward profile.

- **Buy**: 1 lower strike put
- **Sell**: 2 middle strike puts
- **Buy**: 1 upper strike put

### Code Example

```python
from datetime import date
from tastypy.orders.templates import put_butterfly

# AAPL at $150, expecting it to stay around $150
order = put_butterfly(
    underlying="AAPL",
    lower_strike=145.0,   # Buy 1 put
    middle_strike=150.0,  # Sell 2 puts
    upper_strike=155.0,   # Buy 1 put
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=1.00
)
```

## Strike Selection

### Standard Butterfly

- **Equal width**: Most common approach
- **Example**: 145/150/155 (5-point wings)
- **Profit zone**: Narrow, centered at middle strike

### Wider vs Narrower

**Narrow (2-3 point wings)**:

- Lower cost
- Tighter profit zone
- Higher percentage return potential
- More precise price prediction needed

**Wide (10+ point wings)**:

- Higher cost
- Wider profit zone
- Lower percentage return
- More forgiving on price movement

## Management Tips

- **Close at 25-50% profit**: Don't wait for max profit
- **Avoid holding to expiration**: Pin risk at middle strike
- **Best entry**: 30-45 days to expiration
- **Exit if price moves**: If underlying moves significantly away, close to
  preserve capital
- **Adjustments**: Can convert to calendar butterfly or iron butterfly

## Butterfly vs Iron Condor

| Aspect      | Butterfly            | Iron Condor             |
| ----------- | -------------------- | ----------------------- |
| Structure   | 3 strikes, same type | 4 strikes, calls + puts |
| Cost        | Debit (pay)          | Credit (receive)        |
| Profit Zone | Very narrow          | Wider range             |
| Max Profit  | Higher % return      | Lower % return          |
| Breakevens  | 2 points             | 2 points                |
| Best For    | Pin-point accuracy   | Range-bound             |

## Related Strategies

- [Iron Condor](iron-condor.md) - Wider profit zone, credit spread
- [Vertical Spreads](vertical-spreads.md) - Directional alternative
- [Calendar Spreads](calendar-spreads.md) - Time-based alternative
