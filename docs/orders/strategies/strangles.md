# Strangles

Strangles are similar to straddles but use different strikes (out-of-the-money
options), making them cheaper but requiring larger moves to profit.

## Long Strangle

**Market Outlook**: Expecting large move in either direction (long volatility)

**Risk Profile**: Defined risk, potentially unlimited reward

### Strategy Overview

Buy an out-of-the-money put and an out-of-the-money call. Cheaper alternative to
long straddle but requires a larger move to profit.

- **Buy**: OTM put (below current price)
- **Buy**: OTM call (above current price)
- **Net Cost**: Debit (total premium paid)
- **Max Loss**: Total premium paid
- **Max Profit**: Unlimited (stock to zero on downside, unlimited on upside)
- **Breakeven**: Two points - put strike - premium, call strike + premium

### When to Use

- Expecting large move but want lower cost than straddle
- Before earnings or major events
- When IV is relatively low
- Uncertain of direction but confident in volatility
- Want defined risk with unlimited profit potential

### Code Example

```python
from datetime import date
from tastypy.orders.templates import long_strangle

# AAPL at $150, expecting big move
# Use strangle instead of straddle for lower cost
order = long_strangle(
    underlying="AAPL",
    put_strike=145.0,    # OTM put
    call_strike=155.0,   # OTM call
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=6.00     # Pay max $6.00 (vs $10 for straddle)
)
```

### Example P&L Scenarios

Assume AAPL at $150, buy 145/155 strangle for $6.00:

| AAPL Price at Expiration | P&L   | Notes                                               |
| ------------------------ | ----- | --------------------------------------------------- |
| $130                     | +$900 | Put worth $15, call worthless: $15 - $6 = $9 profit |
| $139                     | $0    | Lower breakeven: Put worth $6, call worthless       |
| $145                     | -$600 | Put ATM, call worthless - max loss                  |
| $150                     | -$600 | Both OTM - max loss                                 |
| $155                     | -$600 | Call ATM, put worthless - max loss                  |
| $161                     | $0    | Upper breakeven: Call worth $6, put worthless       |
| $170                     | +$900 | Call worth $15, put worthless: $15 - $6 = $9 profit |

### Greeks Profile

- **Delta**: Near zero (offsetting deltas)
- **Theta**: Negative (time decay on both legs)
- **Vega**: Positive (benefits from volatility increase)
- **Gamma**: Positive (accelerates in direction of move)

### Strike Selection

**Narrow Strangle** (More expensive, easier to profit):

- Strikes close to ATM (e.g., 2-5% OTM each side)
- Higher cost, lower breakevens
- Example: Stock at $150, use 147/153 strangle

**Wide Strangle** (Cheaper, harder to profit):

- Strikes farther OTM (e.g., 10-15% OTM each side)
- Lower cost, higher breakevens
- Example: Stock at $150, use 135/165 strangle

**Balanced Approach**:

- Use same delta for both strikes (e.g., 30 delta put and 30 delta call)
- Example: Stock at $150, use 145/155 (both ~5 points out)

---

## Short Strangle

**Market Outlook**: Expecting minimal movement (short volatility)

**Risk Profile**: Undefined risk in both directions, defined reward

### Strategy Overview

Sell an out-of-the-money put and an out-of-the-money call. Profits from time
decay when the stock stays within the range. **UNLIMITED RISK - Use with extreme
caution.**

- **Sell**: OTM put
- **Sell**: OTM call
- **Net Credit**: Credit (total premium received)
- **Max Profit**: Total premium received
- **Max Loss**: Unlimited (stock to zero on downside, unlimited on upside)
- **Breakeven**: Two points - put strike - premium, call strike + premium

### When to Use

- **HIGH RISK STRATEGY - Consider iron condors instead**
- Expecting range-bound movement
- Implied volatility is very high
- After large move, expecting consolidation
- Have substantial capital and risk tolerance
- Plan to actively manage position

### Code Example

```python
from datetime import date
from tastypy.orders.templates import short_strangle

# AAPL at $150, expecting minimal movement
# WARNING: Unlimited risk!
order = short_strangle(
    underlying="AAPL",
    put_strike=140.0,    # Sell OTM put
    call_strike=160.0,   # Sell OTM call
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=4.00     # Collect min $4.00 credit
)
```

### Example P&L Scenarios

Assume AAPL at $150, sell 140/160 strangle for $4.00:

| AAPL Price at Expiration | P&L            | Notes                                     |
| ------------------------ | -------------- | ----------------------------------------- |
| $130                     | -$600          | Put worth $10, less $4 credit = -$6 loss  |
| $136                     | $0             | Lower breakeven                           |
| $140-160                 | +$400          | Max profit zone - both expire worthless   |
| $164                     | $0             | Upper breakeven                           |
| $170                     | -$600          | Call worth $10, less $4 credit = -$6 loss |
| $180+                    | Unlimited loss | Losses continue to grow                   |

### Greeks Profile

- **Delta**: Near zero initially
- **Theta**: Positive (collecting time decay)
- **Vega**: Negative (hurt by volatility increase)
- **Gamma**: Negative (accelerating losses if tested)

### Management - CRITICAL

**Active management required:**

- **Close at 50% profit**: Standard profit target
- **Use stop losses**: Exit at 2x credit received
- **Roll when tested**: Roll strike out further or to next expiration
- **Close before catalysts**: Exit before earnings or major news
- **Consider alternatives**: Iron condor provides same exposure with defined
  risk
- **Watch margin**: Undefined risk strategies tie up significant margin

---

## Strangle vs Straddle Comparison

| Aspect        | Long Strangle    | Long Straddle    |
| ------------- | ---------------- | ---------------- |
| Cost          | Lower            | Higher           |
| Breakevens    | Wider apart      | Closer together  |
| Move Required | Larger           | Smaller          |
| Max Profit    | Same (unlimited) | Same (unlimited) |
| Risk          | Same (premium)   | Same (premium)   |
| Best For      | Cost-conscious   | Maximum gamma    |

| Aspect      | Short Strangle       | Short Straddle          |
| ----------- | -------------------- | ----------------------- |
| Premium     | Lower                | Higher                  |
| Profit Zone | Wider                | Narrower                |
| Risk        | Unlimited            | Unlimited               |
| Management  | Easier (wider zone)  | Harder (tight zone)     |
| Preferred?  | No - use iron condor | No - use iron butterfly |

## Strike Selection Guidelines

### Long Strangle

**For earnings/events**:

- Use expected move to determine strikes
- Example: Expected ±10% move, use strikes 10-15% out

**For volatility plays**:

- Use technical levels (support/resistance)
- Balance cost vs probability

**Delta-based selection**:

- 25-30 delta options are common
- Example: Stock $150, sell 25 delta put (~$140) and 25 delta call (~$160)

### Short Strangle

**Conservative** (Lower premium, safer):

- 10-15 delta options (85-90% probability OTM)
- Example: Stock $150, sell 10 delta put (~$135) and 10 delta call (~$165)

**Aggressive** (Higher premium, riskier):

- 30 delta options (70% probability OTM)
- Example: Stock $150, sell 30 delta put (~$145) and 30 delta call (~$155)

**Most Important**: Use strikes you believe won't be tested!

## Common Mistakes

1. **Long strangle**: Overpaying for volatility that doesn't materialize
2. **Short strangle**: Underestimating risk, treating it like a safe income
   strategy
3. **Both**: Poor strike selection relative to expected move
4. **Both**: Not managing positions actively
5. **Long**: Holding too long and losing to time decay
6. **Short**: Not having management plan for tested positions
7. **Short**: Using position size that's too large for account

## Why Iron Condor is Better Than Short Strangle

**Short Strangle Problems**:

- Unlimited risk
- Larger margin requirement
- One big move can wipe out months of profits
- Psychological stress

**Iron Condor Benefits**:

- Defined max loss
- Lower margin requirement
- Can size larger for same risk
- Sleep better at night

**Exception**: Short strangle only if you:

- Have substantial capital
- Plan to roll/adjust aggressively
- Understand and accept the risks
- Want slightly higher premium than iron condor

## Management Strategies

### Long Strangle

**Take profits**:

- After big volatility spike (even if directionally flat)
- At 50-100% profit on underlying move
- Immediately after catalyst event

**Cut losses**:

- If IV collapses and position at 50%+ loss
- If catalyst passes without expected move

### Short Strangle

**Untested position**:

- Close at 50% of max profit
- Roll to next expiration to extend time

**Tested position (price near strike)**:

- Roll tested side out further OTM
- Roll entire position to next expiration
- Close position if approaching 50% max loss
- Convert to iron condor by buying wings

**Both sides tested** (price whipsawing):

- Usually best to close and take the loss
- Don't let it become a max loss situation

## Real-World Example

### Long Strangle - Earnings Play

```python
# STOCK at $100, earnings tomorrow
# Expected move: ±12%
# IV: 60%

long_strangle("STOCK", 88.0, 112.0, "251219", 1, 5.00)

# Breakevens: $83 and $117
# If stock moves to $115 or $85, profit ~$200-$700
# Exit immediately after earnings announcement
```

### Short Strangle - High IV Environment

```python
# STOCK at $100 after major news
# IV: 80% (extremely elevated)
# Technical range: $90-$110

short_strangle("STOCK", 90.0, 110.0, "260116", 1, 8.00)

# Profit zone: $82-$118
# Max profit: $800
# RISK: Unlimited below $82 or above $118
# Management: Close at $400 profit or $1,600 loss
```

**Better Alternative**:

```python
# Iron condor with defined risk
iron_condor("STOCK", 80.0, 90.0, 110.0, 120.0, "260116", 1, 6.00)

# Max profit: $600
# Max loss: $400
# Same profit zone but risk is defined
```

## Related Strategies

- [Straddles](straddles.md) - Same strikes instead of different strikes
- [Iron Condor](iron-condor.md) - Short strangle with defined risk wings
  (RECOMMENDED)
- [Vertical Spreads](vertical-spreads.md) - Directional defined-risk
  alternatives
- [Butterfly Spreads](butterfly-spreads.md) - Debit alternative with tighter
  profit zone

## Summary

**Long Strangle**: Cost-effective volatility play for expected large moves.
Lower cost than straddle but requires bigger move. Best for earnings and
event-driven trades.

**Short Strangle**: High-risk strategy that most traders should avoid. Iron
condors provide similar profit potential with defined risk. Only use short
strangles if you:

- Fully understand unlimited risk
- Have substantial capital reserves
- Will manage positions actively
- Accept that one big loss can erase many winners

**Recommendation**: For short premium strategies, use iron condors instead of
short strangles for peace of mind and better risk management.
