# Straddles

Straddles are volatility strategies that involve buying or selling both a call
and a put at the same strike and expiration.

## Long Straddle

**Market Outlook**: Expecting large move in either direction (long volatility)

**Risk Profile**: Defined risk, potentially unlimited reward

### Strategy Overview

Buy both a call and a put at the same strike (usually ATM). Profits from large
price movements in either direction.

- **Buy**: ATM call
- **Buy**: ATM put
- **Net Cost**: Debit (total premium paid)
- **Max Loss**: Total premium paid
- **Max Profit**: Unlimited (stock to zero on downside, unlimited on upside)
- **Breakeven**: Two points - strike ± total premium

### When to Use

- Expecting a large move but unsure of direction
- Before major catalyst (earnings, FDA approval, merger news)
- When implied volatility is low relative to expected move
- Volatility expected to increase significantly
- Binary events with large potential outcomes

### Code Example

```python
from datetime import date
from tastypy.orders.templates import long_straddle

# AAPL at $150, earnings tomorrow, expecting big move
order = long_straddle(
    underlying="AAPL",
    strike=150.0,        # At-the-money
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=10.00    # Pay max $10.00 total
)
```

### Example P&L Scenarios

Assume AAPL at $150, buy 150 straddle for $10.00:

| AAPL Price at Expiration | P&L     | Notes                                                 |
| ------------------------ | ------- | ----------------------------------------------------- |
| $130                     | +$1,000 | Put worth $20, call worthless: $20 - $10 = $10 profit |
| $140                     | $0      | Lower breakeven: Put worth $10, call worthless        |
| $150                     | -$1,000 | Max loss - both options ATM/worthless                 |
| $160                     | $0      | Upper breakeven: Call worth $10, put worthless        |
| $170                     | +$1,000 | Call worth $20, put worthless: $20 - $10 = $10 profit |

### Greeks Profile

- **Delta**: Near zero (call delta and put delta offset)
- **Theta**: Highly negative (paying time decay on both sides)
- **Vega**: Highly positive (major benefit from volatility increase)
- **Gamma**: Highly positive (large gains from directional acceleration)

### Management Tips

- **Exit before expiration**: Volatility collapse can hurt even if directionally
  correct
- **Take profits on volatility spike**: Don't wait for max movement
- **Size appropriately**: Can lose 100% of premium paid
- **Best timing**: Enter when IV is low, exit when IV spikes or price moves
  significantly
- **Earnings plays**: Often exit immediately after announcement regardless of
  profit

---

## Short Straddle

**Market Outlook**: Expecting minimal movement (short volatility)

**Risk Profile**: Undefined risk in both directions, defined reward

### Strategy Overview

Sell both a call and a put at the same strike (usually ATM). Profits from time
decay when the stock stays close to the strike.

- **Sell**: ATM call
- **Sell**: ATM put
- **Net Credit**: Credit (total premium received)
- **Max Profit**: Total premium received
- **Max Loss**: Unlimited (stock to zero on downside, unlimited on upside)
- **Breakeven**: Two points - strike ± total premium

### When to Use

- **HIGH RISK STRATEGY - Use with extreme caution**
- Expecting very little price movement
- After big move, expecting consolidation
- When implied volatility is extremely high
- Have the capital and risk tolerance for potential assignment
- Plan to actively manage the position

### Code Example

```python
from datetime import date
from tastypy.orders.templates import short_straddle

# AAPL at $150, expecting no movement
# WARNING: Unlimited risk!
order = short_straddle(
    underlying="AAPL",
    strike=150.0,
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=10.00    # Collect min $10.00 credit
)
```

### Example P&L Scenarios

Assume AAPL at $150, sell 150 straddle for $10.00:

| AAPL Price at Expiration | P&L            | Notes                                               |
| ------------------------ | -------------- | --------------------------------------------------- |
| $130                     | -$1,000        | Put assigned, $20 loss - $10 credit = -$10 loss     |
| $140                     | $0             | Lower breakeven: Put worth $10, eats entire credit  |
| $150                     | +$1,000        | Max profit - both expire worthless                  |
| $160                     | $0             | Upper breakeven: Call worth $10, eats entire credit |
| $170                     | -$1,000        | Call assigned, $20 loss - $10 credit = -$10 loss    |
| $180+                    | Unlimited loss | Losses continue to grow                             |

### Greeks Profile

- **Delta**: Near zero initially (offsetting deltas)
- **Theta**: Highly positive (collecting time decay on both sides)
- **Vega**: Highly negative (hurt by volatility increase)
- **Gamma**: Highly negative (accelerating losses if price moves)

### Management Tips - CRITICAL

**This strategy requires active management:**

- **Never hold to expiration unmanaged**: Huge assignment risk
- **Close at 50% profit**: Don't be greedy, take profits early
- **Use stop losses**: Exit if loss reaches 1-2x the credit received
- **Watch for catalysts**: Close before earnings or major news
- **Consider defined risk alternatives**: Iron condors, iron butterflies
- **Have enough capital**: Need significant margin and ability to handle
  assignment
- **Adjust when tested**: Roll strikes, close one side, convert to spread

---

## Straddle Comparison

| Aspect     | Long Straddle         | Short Straddle         |
| ---------- | --------------------- | ---------------------- |
| Cost       | High (debit)          | None (credit received) |
| Direction  | Neutral               | Neutral                |
| Volatility | Want increase         | Want decrease          |
| Risk       | Defined (premium)     | Undefined (unlimited)  |
| Best Use   | Before known catalyst | High IV consolidation  |
| Time Decay | Enemy                 | Friend                 |
| Management | Moderate              | Critical/Active        |

## Strike Selection

### Long Straddle

**At-the-Money (Most Common)**:

- Maximum gamma and vega exposure
- Most expensive but most responsive to movement
- Best when expecting very large move

**Slightly OTM**:

- Cheaper alternative (becomes a strangle - see [Strangles](strangles.md))
- Need larger move to profit
- Lower cost = lower breakevens

### Short Straddle

**At-the-Money (Standard)**:

- Maximum premium collected
- Highest probability of being tested
- Requires precise price prediction

**Note**: Most traders prefer iron condors or iron butterflies over naked short
straddles for defined risk.

## Common Mistakes

1. **Long straddles**: Overpaying when IV is already elevated
2. **Short straddles**: Underestimating risk, not having management plan
3. **Both**: Holding through expiration without management
4. **Both**: Wrong position sizing relative to account
5. **Long**: Not taking profits after volatility spike
6. **Short**: Not closing before known catalysts
7. **Short**: Letting small losses become large losses

## Alternatives to Consider

### Instead of Long Straddle

- **Long Strangle**: Cheaper, need larger move (see [Strangles](strangles.md))
- **Calendar Straddle**: Sell near-term, buy far-term for lower cost
- **Risk Reversal**: Long call + short put (or vice versa) for directional bias

### Instead of Short Straddle

- **Iron Butterfly**: Same structure but with defined risk wings
- **Iron Condor**: Wider profit zone, defined risk
- **Credit Spreads**: Directional defined-risk alternative

## Real-World Applications

### Long Straddle - Earnings Play

```python
# Stock at $100, earnings in 2 days
# IV is 40%, expecting 15% move
long_straddle("STOCK", 100.0, "251219", 1, 8.00)
# If stock moves to $115 or $85, profit ~$700
# Exit immediately after announcement
```

### Short Straddle - Post-Earnings IV Crush

```python
# Stock at $100, IV drops from 80% to 30% post-earnings
# Enter SHORT straddle to capture IV collapse
# ONLY if stock likely to consolidate
# Close within 1-2 weeks at 25-50% profit
```

## Related Strategies

- [Strangles](strangles.md) - Similar but using different strikes
- [Iron Butterfly](iron-condor.md) - Short straddle with defined risk wings
- [Calendar Spreads](calendar-spreads.md) - Time-based volatility play
- [Butterfly Spreads](butterfly-spreads.md) - Debit alternative to short
  straddle

## Summary

**Long Straddle**: Best for binary events or expected large moves. High cost,
requires significant movement to profit. Most traders lose money on long
straddles by overpaying for volatility.

**Short Straddle**: High-risk, high-maintenance strategy for experienced traders
only. Unlimited risk makes it unsuitable for most traders. Iron butterflies and
iron condors provide similar exposure with defined risk and are generally
preferred.

**Key Takeaway**: Most option traders should avoid short straddles and use them
only in very specific circumstances with strict management rules and adequate
capital.
