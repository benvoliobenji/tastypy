# Iron Condor

**Market Outlook**: Neutral (expecting low volatility and range-bound movement)

**Risk Profile**: Defined risk, defined reward

## Strategy Overview

An iron condor is a neutral, credit-based strategy that combines a bull put
spread and a bear call spread on the same underlying with the same expiration.
It profits when the underlying stays within a defined range between the short
strikes.

### Structure

- **Sell**: Out-of-the-money put (lower middle strike)
- **Buy**: Further out-of-the-money put (lowest strike) - protection
- **Sell**: Out-of-the-money call (upper middle strike)
- **Buy**: Further out-of-the-money call (highest strike) - protection

**Net Credit**: Credit (you receive premium)

**Max Profit**: Net credit received (achieved if stock stays between short
strikes)

**Max Loss**: Width of wider spread - net credit

**Breakeven Points**:

- Lower: Short put strike - net credit
- Upper: Short call strike + net credit

## Visual Representation

```
            Short Call
               │
    Long Put   │   Short Put      Long Call
       │       │       │              │
    ───┴───────┴───────┴──────────────┴───
     140     145     155            160

       └─────Bull Put Spread─────┘
               └─────Bear Call Spread─────┘
```

## When to Use

- You expect the underlying to trade in a range
- Implied volatility is elevated (selling premium)
- After a big move, expecting consolidation
- Around technical support/resistance levels
- Low volatility environment where big moves are unlikely
- You want to profit from time decay on both sides

## Code Example

```python
from datetime import date
from tastypy.orders.templates import iron_condor

# AAPL is at $150, expecting it to stay between $145-$155
order = iron_condor(
    underlying="AAPL",
    put_long_strike=140.0,   # Buy 140 put (lowest)
    put_short_strike=145.0,  # Sell 145 put (lower middle)
    call_short_strike=155.0, # Sell 155 call (upper middle)
    call_long_strike=160.0,  # Buy 160 call (highest)
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=2.00         # Receive min $2.00 credit
)
```

## Example P&L Scenarios

Assume AAPL at $150, sell iron condor 140/145/155/160 for $2.00 credit:

| AAPL Price at Expiration | P&L   | Notes                                               |
| ------------------------ | ----- | --------------------------------------------------- |
| $135                     | -$300 | Max loss on put side (5-point width - $2.00 credit) |
| $140                     | -$300 | Max loss at long put strike                         |
| $143                     | $0    | Lower breakeven point                               |
| $145                     | +$200 | Short put strike - full profit zone begins          |
| $150                     | +$200 | Max profit (between short strikes)                  |
| $155                     | +$200 | Short call strike - full profit zone ends           |
| $157                     | $0    | Upper breakeven point                               |
| $160                     | -$300 | Max loss at long call strike                        |
| $165                     | -$300 | Max loss on call side                               |

## Greeks Profile

- **Delta**: Near zero when centered, directional exposure increases as price
  moves toward short strikes
- **Theta**: Positive (benefits greatly from time decay - this is a theta
  strategy)
- **Vega**: Negative (benefits from declining volatility)
- **Gamma**: Negative (loses value as price accelerates in either direction)

## Strike Selection Guidelines

### Standard Iron Condor

Most traders use **equidistant strikes**:

- Width: 5-point wings are common
- Short strikes: Typically 1 standard deviation out (~16% probability ITM each
  side)
- **Example**: 140/145/155/160 → 5-point wings, 10-point wide profit zone

### Aggressive vs Conservative

**Conservative (Higher probability, lower credit)**:

- Place short strikes around 10-15 delta (85-90% OTM probability)
- Wider profit zone
- Lower premium collected
- **Example**: 135/140/160/165 (wider spread)

**Aggressive (Lower probability, higher credit)**:

- Place short strikes around 30 delta (70% OTM probability)
- Narrower profit zone
- Higher premium collected
- **Example**: 143/145/155/157 (tighter spread)

### Asymmetric Iron Condors

You can bias the iron condor toward your market outlook:

**Slightly Bullish**:

- Wider put spread, narrower call spread
- More credit from put side
- **Example**: 135/145/155/160 (10-point put width, 5-point call width)

**Slightly Bearish**:

- Narrower put spread, wider call spread
- More credit from call side
- **Example**: 140/145/155/165 (5-point put width, 10-point call width)

## Management Strategies

### 1. Take Profits Early

**When to close**:

- At 50% of max profit (common target)
- At 25% of max profit if near expiration
- When you've captured 75%+ of the credit

**Why**: Reduces tail risk and frees up capital for new trades

### 2. Manage Winners

If the stock stays in the profit zone with 2-3 weeks to expiration:

- Close for 50-60% profit
- Roll to next expiration for additional credit
- Close one side if untested and far OTM

### 3. Manage Losers

**If one side is tested**:

**21+ days to expiration**:

- Roll entire iron condor to later expiration
- Roll tested side to further OTM strikes
- Close untested side to reduce risk
- Convert to iron butterfly or broken wing butterfly

**7-14 days to expiration**:

- Close the entire position if >50% of max loss
- Consider rolling tested spread to next expiration
- Take the loss if roll doesn't improve risk/reward

**<7 days to expiration**:

- Usually best to close and take the loss
- Don't let small losses become max losses
- Avoid pin risk and assignment headaches

### 4. Closing One Side

If one side is clearly safe (5+ days out, 90%+ OTM):

- Close the winning side to collect partial profit
- Let the other side expire or manage separately
- Converts position to simple vertical spread

## Risk Management

### Position Sizing

**Conservative approach**:

- Max loss = 1-2% of account
- Example: $50k account → $500-1000 max loss → 1-2 iron condors with 5-point
  wings

**Margin Requirement**:

- Equal to width of wider spread × 100 × quantity
- Example: 5-point wings → $500 margin per iron condor

### Volatility Considerations

**High IV Environment** (Good for Iron Condors):

- Premiums are inflated
- Can collect larger credits
- Higher probability of IV crush working in your favor

**Low IV Environment** (Challenging):

- Premiums are small
- Risk/reward less favorable
- Consider waiting for IV expansion

### Earnings and Events

**Avoid holding through earnings** unless:

- You're specifically playing IV crush
- You've sized position appropriately for the risk
- You're prepared for the potential volatility expansion

**Better approach**:

- Close 1-2 days before earnings
- Enter after earnings when IV contracts
- Use smaller position size if holding through

## Advanced Techniques

### Rolling Techniques

**Roll entire IC out in time**:

- Close current IC
- Open new IC in later expiration at same or adjusted strikes
- Goal: Collect additional credit to offset losses

**Roll tested side**:

- Close tested spread
- Open new spread at further strikes in same or later expiration
- Keeps one side working while managing the other

### Adjustments

**Converting to Iron Butterfly**:

- If stock moves against one side, roll both short strikes to ATM
- Narrows profit zone but increases credit

**Broken Wing Butterfly**:

- Skew the spread so max loss is only on one side
- Can sometimes enter for zero max loss on one side

### Stacking Iron Condors

Open ICs at multiple expirations:

- Weekly ICs for frequent small profits
- Monthly ICs for larger credit, less maintenance
- Diversifies time decay across multiple timeframes

## Common Mistakes to Avoid

1. **Taking max loss**: Close losing positions before max loss is reached
2. **Ignoring adjustments**: Don't be passive, actively manage tested positions
3. **Poor strike selection**: Short strikes too close to current price = higher
   test rate
4. **Over-trading**: Quality setups are key, don't force trades
5. **Wrong IV environment**: Need elevated IV to make the risk/reward worthwhile
6. **Holding to expiration**: Close at 50-75% profit or 50% loss, don't let pin
   risk materialize
7. **Not using limit orders**: Slippage on 4-leg orders can be significant

## When Iron Condors Work Best

**Ideal Conditions**:

- Stock trading in a range for several weeks
- Elevated implied volatility
- 30-45 days to expiration
- No major catalysts (earnings, FDA approval, etc.) on the horizon
- Technical support/resistance levels well-defined

**Avoid**:

- Strong trending markets
- Low volatility environment
- Right before major news events
- When technical breakout/breakdown is likely

## Probability and Expected Value

**Typical Iron Condor**:

- Credit: $2.00 on 5-point wings
- Max Loss: $3.00
- Risk/Reward: $2.00 to make, $3.00 to lose (1.5:1)
- Breakeven probability: Need ~60% win rate to be profitable over time

**Factors affecting probability**:

- Strike selection (delta)
- Time to expiration
- Volatility environment
- Underlying's tendency to trend or range

## Related Strategies

- [Vertical Spreads](vertical-spreads.md) - Building blocks of the iron condor
- [Butterfly Spreads](butterfly-spreads.md) - Similar profit zone but with debit
- [Strangles](strangles.md) - Short strangle has unlimited risk vs IC's defined
  risk
- [Jade Lizard](jade-lizard.md) - Similar to iron condor but with no upside risk

## Summary

The iron condor is a versatile, neutral strategy best suited for range-bound
markets with elevated volatility. While it requires active management and
discipline, it can provide consistent income when used in the right conditions.
Key to success is proper strike selection, early profit-taking, and knowing when
to cut losses.
