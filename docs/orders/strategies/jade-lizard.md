# Jade Lizard

**Market Outlook**: Bullish to neutral

**Risk Profile**: Undefined downside risk, no upside risk (when credit > call
spread width)

## Strategy Overview

A jade lizard combines a naked short put with a bear call spread. It's designed
so that the credit received exceeds the width of the call spread, creating a
position with no upside risk.

### Structure

- **Sell**: Out-of-the-money put (lower strike)
- **Sell**: Out-of-the-money call (middle strike)
- **Buy**: Further out-of-the-money call (highest strike) - protection

**Net Credit**: Credit (premium received)

**Max Profit**: Total credit received (if stock stays between put and short
call)

**Max Loss Downside**: Put strike - credit received (if stock goes to zero)

**Max Loss Upside**: None (if credit > call spread width)

**Breakeven**: Put strike - credit received

## Key Feature: No Upside Risk

When structured correctly (credit ≥ call spread width), there is **no upside
risk**:

- Credit received: $6.00
- Call spread width: 160 - 155 = $5.00
- Even if stock rallies above 160, max loss on call spread ($5.00) is covered by
  credit ($6.00)

## When to Use

- Bullish outlook but want premium collection
- Don't believe stock will drop to put strike
- Want income without upside risk
- High implied volatility environment
- Technical support at put strike level
- More bullish than iron condor but want downside income

## Code Example

```python
from datetime import date
from tastypy.orders.templates import jade_lizard

# AAPL at $150, bullish with support at $140
# Sell jade lizard for credit > call spread width
order = jade_lizard(
    underlying="AAPL",
    put_strike=140.0,        # Sell put
    call_short_strike=155.0, # Sell call (bear call spread part)
    call_long_strike=160.0,  # Buy call (protection)
    expiration=date(2025, 12, 19),
    quantity=1,
    limit_price=6.00         # Collect min $6.00 ($5 call width + $1)
)
```

## Example P&L Scenarios

Assume AAPL at $150, jade lizard 140P/155C/160C for $6.00 credit:

| AAPL Price at Expiration | P&L     | Notes                                                    |
| ------------------------ | ------- | -------------------------------------------------------- |
| $120                     | -$1,400 | Put assigned at $140, stock worth $120, less $6 credit   |
| $134                     | $0      | Breakeven: $140 put - $6 credit                          |
| $140-155                 | +$600   | Max profit zone - all expire worthless                   |
| $160                     | +$100   | Call spread at max loss ($5), offset by $6 credit        |
| $170+                    | +$100   | Call spread maxes at -$5, but have $6 credit = $1 profit |

### Key Insight

Unlike most credit spreads, jade lizard has **asymmetric risk**:

- Downside: Significant risk (like naked put)
- Upside: No risk (when credit > call spread width)

This makes it ideal for bullish traders who want income but don't want to cap
gains.

## Greeks Profile

- **Delta**: Positive (bullish position)
- **Theta**: Positive (benefits from time decay)
- **Vega**: Negative (benefits from declining volatility)
- **Gamma**: Negative at put strike, negative at call strikes

## Strike Selection

### Critical Rule: Credit > Call Spread Width

**Example calculations**:

**Good Jade Lizard**:

- Sell 140 put: $3.00
- Sell 155 call: $2.50
- Buy 160 call: -$1.00
- **Total credit**: $4.50
- **Call spread width**: $5.00
- **Result**: Small upside risk ($0.50)

**Perfect Jade Lizard**:

- Sell 140 put: $4.00
- Sell 155 call: $3.00
- Buy 160 call: -$1.00
- **Total credit**: $6.00
- **Call spread width**: $5.00
- **Result**: No upside risk, $1.00 profit even at highest prices

### Strike Placement Guidelines

**Put Strike**:

- 10-20% below current price
- At strong technical support
- Around 20-30 delta
- Example: Stock at $150, use $135-145 put

**Call Short Strike**:

- 5-10% above current price
- Around 30 delta
- Example: Stock at $150, use $155-160 short call

**Call Long Strike**:

- 5-10 points above short call
- Adjust based on credit needed
- Example: If short call at $155, long call at $160-165

## Jade Lizard vs Iron Condor

| Aspect        | Jade Lizard                | Iron Condor   |
| ------------- | -------------------------- | ------------- |
| Upside Risk   | None (if structured right) | Defined       |
| Downside Risk | Undefined (like naked put) | Defined       |
| Bias          | Bullish                    | Neutral       |
| Credit        | Larger                     | Smaller       |
| Margin        | Higher (naked put)         | Lower         |
| Best For      | Bullish income             | Neutral range |

## Management Strategies

### If Stock Stays in Range (Ideal)

- Let all options expire worthless
- Keep full credit
- **Or** close at 50-75% of max profit to reduce risk

### If Stock Drops Toward Put Strike

**Action options**:

1. **Roll put down and out**: Lower strike, later expiration, collect credit
2. **Close entire position**: If approaching 50% max loss
3. **Close put, keep call spread**: Reduce risk exposure
4. **Convert to covered put**: If assigned, own stock, sell calls

**Example roll**:

```python
# Stock dropped from $150 to $142, put at $140 is threatened
# Close current position
# Open new jade lizard: 135P/155C/160C for next month
# Collect additional credit, give more room
```

### If Stock Rises (No Action Needed!)

- This is the beauty of jade lizard
- As long as credit > call spread width, no upside risk
- Can close early for profit or let it expire

### Before Expiration

- Close 1-2 weeks before expiration if near max profit
- Avoid pin risk at put strike
- Don't need to worry about upside

## Risk Management

### Position Sizing

**Key consideration**: The naked put requires substantial margin

**Sizing approach**:

- Margin = Put strike × 100 × quantity
- Example: $140 put = $14,000 margin per contract
- Don't overleverage based on credit received

**Risk per trade**:

- Max loss (stock to zero) = Put strike - credit
- Example: $140 put - $6 credit = $134 max loss per share = $13,400
- Size so max loss = 2-5% of account

### When to Avoid

**Don't use jade lizard if**:

- Strong downtrend in place
- No clear support level for put
- Low implied volatility (insufficient credit)
- Can't collect credit > call spread width
- Uncomfortable with naked put risk
- Insufficient margin for naked put

**Best conditions**:

- Bullish or neutral outlook
- Strong support at put strike
- High implied volatility
- Can structure with no upside risk
- Have margin for naked put
- Want income with upside participation

## Tax and Assignment Considerations

### Early Assignment Risk

**Put side**:

- Can be assigned early if deep ITM
- Results in long stock position at put strike
- Have plan for this scenario

**Call side**:

- Bear call spread can have early assignment
- Less likely if OTM but possible if approaching expiration ITM

### Tax Treatment

- Premium collected is short-term capital gain if expires
- If assigned on put: Reduces cost basis of stock
- If assigned on call spread: Multiple legs, complex treatment

**Consult tax professional for specifics**

## Variations

### Reverse Jade Lizard

**Bearish version**:

- Sell OTM call (higher strike)
- Sell OTM put (middle strike) + Buy OTM put (protection) = bull put spread
- Credit > put spread width = no downside risk
- Bearish bias with income

**When to use**: Bearish but want income without downside risk

### Adjusted Jade Lizard

**Asymmetric call spread**:

- Use wider call spread (10-15 points) to collect more credit
- Gives more cushion for no upside risk
- Example: 140P/155C/170C

## Common Mistakes

1. **Credit < call spread width**: Creates upside risk, defeats the purpose
2. **Put strike too close**: Increases probability of being tested
3. **Ignoring support levels**: Place put at technical support, not random
   strike
4. **Overleveraging**: Naked put requires substantial margin, don't oversize
5. **Not managing tested put**: Have plan before entering trade
6. **Using in downtrend**: Jade lizard is bullish strategy, don't fight trend
7. **Low IV entry**: Need sufficient premium to structure properly

## Real-World Example

### Post-Earnings Jade Lizard

```python
# AAPL at $150 after earnings, IV elevated
# Bullish but want income, support at $140
# Call spread width: $5, aim for $6+ credit

jade_lizard("AAPL", 140.0, 155.0, 160.0, "260116", 1, 6.00)

# Credit received: $6.00
# Call spread width: $5.00
# No upside risk (even if AAPL runs to $200)
# Max profit: $600 (if stays between $140-$155)
# Max loss: $13,400 (if AAPL to zero)
# Breakeven: $134

# Management plan:
# - Close at $300 profit (50%)
# - Roll put if approaches $142
# - Let expire if AAPL stays above $140
```

## Related Strategies

- [Iron Condor](iron-condor.md) - Neutral version with defined risk both sides
- [Bull Put Spread](vertical-spreads.md#bull-put-spread) - Simpler bullish
  credit spread
- [Covered Put](covered-strategies.md#covered-put) - Cash-secured alternative
- [Short Strangle](strangles.md#short-strangle) - Similar structure, unlimited
  risk both sides

## Comparison to Similar Strategies

### vs Short Put

**Jade Lizard advantages**:

- Collects more premium (has call spread too)
- No upside risk if structured correctly

**Short Put advantages**:

- Simpler management
- Less complex structure

### vs Bull Put Spread

**Jade Lizard advantages**:

- Higher credit collected
- No upside risk

**Bull Put Spread advantages**:

- Defined risk both sides
- Lower margin requirement
- Simpler management

### vs Iron Condor

**Jade Lizard advantages**:

- No upside risk
- More bullish bias
- Can participate in upside moves

**Iron Condor advantages**:

- Defined risk both sides
- More neutral strategy
- Lower margin requirement

## Summary

The jade lizard is a sophisticated bullish income strategy that combines a naked
short put with a bear call spread. Its unique advantage is **no upside risk**
when the credit received exceeds the width of the call spread.

**Best for**:

- Experienced traders comfortable with naked put risk
- Bullish outlook with defined support level
- High IV environments where sufficient credit can be collected
- Traders who want income without capping upside

**Key Considerations**:

- Must ensure credit > call spread width
- Requires margin for naked put
- Significant downside risk if put is breached
- Active management needed if tested

**Bottom Line**: The jade lizard is an excellent strategy for bullish traders
who want to collect premium without eliminating upside potential. However, the
undefined downside risk means it requires careful position sizing, strike
selection, and active management. When structured correctly in the right market
conditions, it offers an excellent risk/reward profile for bullish income
trading.
