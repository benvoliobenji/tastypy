# Vertical Spreads

Vertical spreads are two-leg option strategies where you buy one option and sell
another option of the same type (both calls or both puts) with the same
expiration but different strike prices.

## Bull Call Spread

**Market Outlook**: Moderately bullish

**Risk Profile**: Defined risk, defined reward

### Strategy Overview

A bull call spread profits from moderate upward price movement. You buy a call
at a lower strike and sell a call at a higher strike, both with the same
expiration.

- **Buy**: Lower strike call
- **Sell**: Higher strike call
- **Net Cost**: Debit (you pay to enter)
- **Max Profit**: Width of strikes - net debit paid
- **Max Loss**: Net debit paid
- **Breakeven**: Long strike + net debit

### When to Use

- You expect moderate upward price movement
- You want to reduce the cost of buying a long call
- Volatility is high and you want to offset some of the premium cost
- You have a specific price target in mind (at or below short strike)

### Code Example

```python
from datetime import date
from tastypy.orders.templates import bull_call_spread

# AAPL is at $148, expecting rise to $155
order = bull_call_spread(
    underlying="AAPL",
    long_strike=150.0,   # Buy the 150 call
    short_strike=155.0,  # Sell the 155 call
    expiration=date(2025, 12, 19), # December 19, 2025
    quantity=1,          # 1 spread
    limit_price=2.50     # Pay max $2.50 debit
)
```

### Example P&L Scenarios

Assume AAPL at $148, buy 150/155 bull call spread for $2.50:

| AAPL Price at Expiration | P&L   | Notes                                    |
| ------------------------ | ----- | ---------------------------------------- |
| $145                     | -$250 | Max loss (both options expire worthless) |
| $150                     | -$250 | Breakeven at $152.50                     |
| $152.50                  | $0    | Breakeven point                          |
| $155                     | +$250 | Max profit (5-point spread - $2.50 cost) |
| $160                     | +$250 | Max profit (capped at short strike)      |

### Greeks Profile

- **Delta**: Positive, increases as price rises toward strikes
- **Theta**: Slightly negative initially, becomes positive near short strike
- **Vega**: Slightly positive initially, becomes negative near expiration
- **Gamma**: Positive between strikes, peaks at mid-point

### Management Tips

- **Take profits**: Consider closing at 50% of max profit
- **Adjust**: If stock moves against you, consider rolling to a later date
- **Early exit**: If stock blows past short strike early, consider taking
  profits
- **Avoid assignment**: If short call goes ITM near expiration, close or roll to
  avoid assignment

---

## Bear Call Spread

**Market Outlook**: Moderately bearish to neutral

**Risk Profile**: Defined risk, defined reward

### Strategy Overview

A bear call spread profits when the underlying stays below the short strike. You
sell a call at a lower strike and buy a call at a higher strike for protection.

- **Sell**: Lower strike call
- **Buy**: Higher strike call (protection)
- **Net Credit**: Credit (you receive premium)
- **Max Profit**: Net credit received
- **Max Loss**: Width of strikes - net credit
- **Breakeven**: Short strike + net credit

### When to Use

- You expect the stock to stay flat or decline
- You want to profit from time decay
- Implied volatility is high and you want to sell premium
- You believe the stock won't reach the short strike

### Code Example

```python
from datetime import date
from tastypy.orders.templates import bear_call_spread

# AAPL is at $148, expecting it to stay below $155
order = bear_call_spread(
    underlying="AAPL",
    short_strike=155.0,  # Sell the 155 call
    long_strike=160.0,   # Buy the 160 call (protection)
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=1.50     # Receive min $1.50 credit
)
```

### Example P&L Scenarios

Assume AAPL at $148, sell 155/160 bear call spread for $1.50 credit:

| AAPL Price at Expiration | P&L   | Notes                                      |
| ------------------------ | ----- | ------------------------------------------ |
| $150                     | +$150 | Max profit (both options expire worthless) |
| $155                     | +$150 | Max profit (short strike not breached)     |
| $156.50                  | $0    | Breakeven point                            |
| $160                     | -$350 | Max loss (5-point spread - $1.50 credit)   |
| $165                     | -$350 | Max loss (capped by long call protection)  |

### Greeks Profile

- **Delta**: Negative, becomes more negative as price rises
- **Theta**: Positive (benefits from time decay)
- **Vega**: Negative (benefits from declining volatility)
- **Gamma**: Negative, peaks at short strike

### Management Tips

- **Take profits early**: Close at 50-75% of max profit to reduce tail risk
- **Roll up/out**: If tested, roll to higher strikes or later expiration for
  additional credit
- **Watch pin risk**: Near expiration, be aware of assignment risk if short call
  is near ATM
- **Don't let winners become losers**: If you've captured 80%+ of credit,
  consider closing

---

## Bull Put Spread

**Market Outlook**: Moderately bullish to neutral

**Risk Profile**: Defined risk, defined reward

### Strategy Overview

A bull put spread profits when the underlying stays above the short strike. You
sell a put at a higher strike and buy a put at a lower strike for protection.

- **Sell**: Higher strike put
- **Buy**: Lower strike put (protection)
- **Net Credit**: Credit (you receive premium)
- **Max Profit**: Net credit received
- **Max Loss**: Width of strikes - net credit
- **Breakeven**: Short strike - net credit

### When to Use

- You're bullish or neutral on the underlying
- You want to profit from time decay and rising prices
- You believe the stock has support at or above the short strike
- Implied volatility is elevated

### Code Example

```python
from datetime import date
from tastypy.orders.templates import bull_put_spread

# AAPL is at $148, expecting support at $145
order = bull_put_spread(
    underlying="AAPL",
    short_strike=145.0,  # Sell the 145 put
    long_strike=140.0,   # Buy the 140 put (protection)
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=1.25     # Receive min $1.25 credit
)
```

### Example P&L Scenarios

Assume AAPL at $148, sell 145/140 bull put spread for $1.25 credit:

| AAPL Price at Expiration | P&L   | Notes                                      |
| ------------------------ | ----- | ------------------------------------------ |
| $140                     | -$375 | Max loss (5-point spread - $1.25 credit)   |
| $143.75                  | $0    | Breakeven point                            |
| $145                     | +$125 | Max profit begins                          |
| $150                     | +$125 | Max profit (both options expire worthless) |

### Greeks Profile

- **Delta**: Positive, decreases as price falls
- **Theta**: Positive (benefits from time decay)
- **Vega**: Negative (benefits from declining volatility)
- **Gamma**: Negative at short strike

### Management Tips

- **Close early**: Take profits at 50-75% of max profit
- **Roll down/out**: If tested, roll to lower strikes or later date for
  additional credit
- **Watch support levels**: Technical analysis can help identify good short
  strike placement
- **Avoid earnings**: Unless specifically targeting IV crush, avoid holding
  through earnings

---

## Bear Put Spread

**Market Outlook**: Moderately bearish

**Risk Profile**: Defined risk, defined reward

### Strategy Overview

A bear put spread profits from moderate downward price movement. You buy a put
at a higher strike and sell a put at a lower strike to reduce cost.

- **Buy**: Higher strike put
- **Sell**: Lower strike put
- **Net Cost**: Debit (you pay to enter)
- **Max Profit**: Width of strikes - net debit paid
- **Max Loss**: Net debit paid
- **Breakeven**: Long strike - net debit

### When to Use

- You expect moderate downward price movement
- You want to reduce the cost of buying a long put
- You have a specific downside target (at or above short strike)
- Volatility is high and outright puts are expensive

### Code Example

```python
from datetime import date
from tastypy.orders.templates import bear_put_spread

# AAPL is at $148, expecting decline to $140
order = bear_put_spread(
    underlying="AAPL",
    long_strike=150.0,   # Buy the 150 put
    short_strike=145.0,  # Sell the 145 put
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=2.00     # Pay max $2.00 debit
)
```

### Example P&L Scenarios

Assume AAPL at $148, buy 150/145 bear put spread for $2.00:

| AAPL Price at Expiration | P&L   | Notes                                        |
| ------------------------ | ----- | -------------------------------------------- |
| $155                     | -$200 | Max loss (both options expire worthless)     |
| $150                     | -$200 | Long put ATM but no intrinsic value gain yet |
| $148                     | -$200 | Breakeven at $148                            |
| $145                     | +$300 | Max profit (5-point spread - $2.00 cost)     |
| $140                     | +$300 | Max profit (capped at short strike)          |

### Greeks Profile

- **Delta**: Negative, becomes more negative as price falls
- **Theta**: Slightly negative, becomes positive if both options go deep ITM
- **Vega**: Slightly positive, benefits from rising volatility
- **Gamma**: Positive between strikes

### Management Tips

- **Take profits**: Close at 50% of max profit to reduce risk
- **Don't hold to expiration**: Time decay accelerates, manage 1-2 weeks before
  expiry
- **Watch for reversals**: If stock bounces, consider cutting losses early
- **Roll to extend**: If thesis unchanged but need more time, roll to later
  expiration

---

## Vertical Spread Comparison

| Strategy  | Outlook | Type   | Max Profit | Max Loss | Best Conditions           |
| --------- | ------- | ------ | ---------- | -------- | ------------------------- |
| Bull Call | Bullish | Debit  | Limited    | Limited  | Moderate rise expected    |
| Bear Call | Bearish | Credit | Limited    | Limited  | Stay below short strike   |
| Bull Put  | Bullish | Credit | Limited    | Limited  | Stay above short strike   |
| Bear Put  | Bearish | Debit  | Limited    | Limited  | Moderate decline expected |

## Strike Selection Guidelines

### Width Selection

- **Narrow spreads** (2-3 points): Lower cost, lower profit, higher probability
- **Standard spreads** (5 points): Balanced risk/reward
- **Wide spreads** (10+ points): Higher cost/credit, lower probability

### Strike Placement

**Debit Spreads (Bull Call, Bear Put)**:

- **Conservative**: Long strike at or slightly OTM, short strike 5-10 points
  further out
- **Aggressive**: Long strike ATM, short strike closer (3-5 points)

**Credit Spreads (Bull Put, Bear Call)**:

- **Conservative**: Short strike 1-2 standard deviations OTM
- **Moderate**: Short strike around 70-80% probability OTM
- **Aggressive**: Short strike around 30-50 delta

## Common Mistakes to Avoid

1. **Holding to expiration**: Close early to avoid pin risk and maximize
   probability-adjusted returns
2. **Poor strike selection**: Don't sell strikes you believe will be tested
3. **Ignoring assignment risk**: Short options ITM near expiration can be
   assigned
4. **Fighting the trend**: Don't keep rolling against a strong directional move
5. **Over-trading**: Quality setups are better than quantity
6. **Ignoring earnings**: IV crush can work for or against you depending on the
   spread
7. **Not using limit orders**: Always use limit orders for spreads to avoid poor
   fills

## Related Strategies

- [Iron Condor](iron-condor.md) - Combines bull put and bear call spreads
- [Butterfly Spreads](butterfly-spreads.md) - Uses three strikes instead of two
- [Calendar Spreads](calendar-spreads.md) - Uses different expirations instead
  of strikes
