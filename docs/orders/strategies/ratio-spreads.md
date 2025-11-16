# Ratio Spreads

Ratio spreads involve buying options at one strike and selling more options at a
different strike, creating an asymmetric position with undefined risk on the
short side.

## Call Ratio Spread

**Market Outlook**: Moderately bullish with limited upside belief

**Risk Profile**: Limited downside risk, unlimited upside risk

### Strategy Overview

Buy calls at a lower strike and sell more calls at a higher strike. Typically
entered for a small credit or debit. Profits if stock rises to the short strike
but has unlimited risk above.

- **Buy**: Lower strike calls (fewer contracts)
- **Sell**: Higher strike calls (more contracts)
- **Net Cost**: Usually credit or small debit
- **Max Profit**: At short strike price
- **Max Loss Downside**: Net debit paid (if entered for debit)
- **Max Loss Upside**: Unlimited (beyond short strike)
- **Breakeven**: Complex - depends on credit/debit and strikes

### When to Use

- Moderately bullish but don't expect price to exceed short strike
- Want to reduce cost or collect credit on bullish play
- Have specific price target in mind
- Advanced traders only - requires active management
- **Not recommended for beginners due to unlimited risk**

### Code Example

```python
from datetime import date
from tastypy.orders.templates import call_ratio_spread

# AAPL at $150, bullish to $155 but not beyond
# Buy 1, sell 2 for net credit
order = call_ratio_spread(
    underlying="AAPL",
    long_strike=150.0,     # Buy 1 call
    short_strike=155.0,    # Sell 2 calls
    expiration=date(2025, 12, 19),
    long_quantity=1,       # Buy 1
    short_quantity=2,      # Sell 2
    limit_price=0.50       # Collect $0.50 credit (or pay debit)
)
```

### Example P&L Scenarios

Assume AAPL at $150, 1×2 call ratio spread (buy 1x 150C, sell 2x 155C) for $0.50
credit:

| AAPL Price at Expiration | P&L            | Notes                                               |
| ------------------------ | -------------- | --------------------------------------------------- |
| $145                     | +$50           | All expire worthless, keep credit                   |
| $150                     | +$50           | Long call ATM, shorts OTM                           |
| $155                     | +$550          | Max profit: Long call $5 ITM + $50 credit           |
| $160                     | +$50           | Long worth $10, shorts worth -$10, net +$50 credit  |
| $165                     | -$450          | Long worth $15, shorts worth -$20, net -$5 + credit |
| $170+                    | Unlimited loss | Extra short call creates increasing losses          |

### Greeks Profile

- **Delta**: Positive initially, becomes negative if price rises too much
- **Theta**: Slightly positive (net short options)
- **Vega**: Slightly negative (net short options)
- **Gamma**: Positive below strikes, becomes very negative above short strike

---

## Put Ratio Spread

**Market Outlook**: Moderately bearish with limited downside belief

**Risk Profile**: Limited upside risk, significant downside risk (stock to zero)

### Strategy Overview

Buy puts at a higher strike and sell more puts at a lower strike. Similar
structure to call ratio but with puts.

- **Buy**: Higher strike puts (fewer contracts)
- **Sell**: Lower strike puts (more contracts)
- **Net Cost**: Usually credit or small debit
- **Max Profit**: At short strike price
- **Max Loss Downside**: Significant (stock to zero × naked puts)
- **Max Loss Upside**: Net debit paid (if entered for debit)
- **Breakeven**: Complex - depends on credit/debit and strikes

### Code Example

```python
from datetime import date
from tastypy.orders.templates import put_ratio_spread

# AAPL at $150, bearish to $145 but not much lower
# Buy 1, sell 2
order = put_ratio_spread(
    underlying="AAPL",
    long_strike=150.0,     # Buy 1 put
    short_strike=145.0,    # Sell 2 puts
    expiration=date(2025, 12, 19),
    long_quantity=1,
    short_quantity=2,
    limit_price=0.50       # Net credit/debit
)
```

### Example P&L Scenarios

Assume AAPL at $150, 1×2 put ratio spread (buy 1x 150P, sell 2x 145P) for $0.50
credit:

| AAPL Price at Expiration | P&L               | Notes                                               |
| ------------------------ | ----------------- | --------------------------------------------------- |
| $160                     | +$50              | All expire worthless, keep credit                   |
| $150                     | +$50              | Long put ATM, shorts OTM                            |
| $145                     | +$550             | Max profit: Long put $5 ITM + $50 credit            |
| $140                     | +$50              | Long worth $10, shorts worth -$10, net +credit      |
| $135                     | -$450             | Long worth $15, shorts worth -$20, net -$5 + credit |
| $130 and lower           | Increasing losses | Extra short put creates increasing losses           |

## Ratio Selection

### Standard 1×2 Ratio

Most common structure:

- Buy 1, sell 2
- Example: Buy 1x 150C, sell 2x 155C

### 2×3 Ratio

Larger position:

- Buy 2, sell 3
- Same risk/reward profile, larger size

### Custom Ratios

- **1×3**: More aggressive, higher credit, more risk
- **2×4**: Equivalent to 1×2 but bigger position
- **Covered ratio**: Own stock + sell more calls than you own

## Strike Selection

### Call Ratio Spread

**Conservative**:

- Short strike at your price target
- 5-10 point spread between strikes
- Example: Stock $150, buy 150C, sell 160C (giving room for movement)

**Aggressive**:

- Tighter strikes for more credit
- Less room for upside before unlimited risk
- Example: Stock $150, buy 150C, sell 153C

### Put Ratio Spread

**Conservative**:

- Short strike at strong support level
- Wider spread gives more room
- Example: Stock $150, buy 150P, sell 140P

**Aggressive**:

- Tighter strikes
- More credit but less margin for error
- Example: Stock $150, buy 150P, sell 148P

## Management Strategies

### If Price Approaches/Exceeds Short Strike

**Critical**: This is when unlimited risk begins!

**Options**:

1. **Close entire position**: Lock in profit/loss
2. **Buy back naked options**: Convert to defined risk spread
3. **Roll short strikes higher/lower**: Extend the profit zone
4. **Add long options**: Create butterfly or other defined risk structure

### If Price Stays in Profit Zone

- Consider closing at 50% of max profit
- Don't get greedy - max profit is at specific price
- Time decay works in your favor

### Before Expiration

- **Never hold to expiration if near/above short strike**
- Assignment risk on naked options
- Close 1-2 weeks before expiration

## Risk Management - CRITICAL

### Position Sizing

**Key principle**: Size as if you're short the naked options, because you are!

**Example**: 1×2 call ratio = 1 naked short call + 1 debit spread

- Margin requirement reflects the naked call
- Risk is unlimited above short strike

**Recommended**: Risk no more than 1-2% of account on potential loss

### Stop Losses

**Define exit points before entry**:

- If stock moves beyond X% past short strike → close
- If unrealized loss reaches 2-3× credit received → close
- If approaching max acceptable loss → close immediately

### Why Most Traders Should Avoid Ratio Spreads

1. **Unlimited risk**: One big move can cause severe losses
2. **Complex management**: Requires constant monitoring
3. **Margin intensive**: Naked options require substantial margin
4. **Better alternatives exist**: Vertical spreads provide similar exposure with
   defined risk
5. **Psychological difficulty**: Hard to manage the unlimited risk aspect

## When Ratio Spreads Work

**Ideal conditions**:

- Strong conviction price won't exceed short strike
- High implied volatility (collect more premium)
- Clear technical resistance (calls) or support (puts)
- Near-term catalyst that will resolve uncertainty
- Experience managing undefined risk positions

**Avoid when**:

- Low conviction on price target
- Trending market (risk of runaway move)
- Low volatility (insufficient credit)
- Earnings or major catalyst ahead
- Beginner/intermediate trader

## Better Alternatives

### Instead of Call Ratio Spread

**Bull call spread**:

- Defined risk
- Similar profit if stock reaches target
- Less margin required
- Example: Instead of 1×2 150/155 ratio, use 1×1 150/155 spread

**Call calendar spread**:

- Profit from time decay
- Less directional risk
- Defined risk

### Instead of Put Ratio Spread

**Bear put spread**:

- Defined risk
- Similar profit if stock reaches target
- Simpler management

**Put calendar spread**:

- Time decay focus
- Defined risk

## Real-World Example

### Call Ratio Spread - Earnings Play

```python
# STOCK at $100, earnings tomorrow
# Bullish to $105 but unlikely to exceed $110
# Sell ratio spread to collect credit

call_ratio_spread("STOCK", 100.0, 105.0, "251219", 1, 2, 0.75)

# Max profit at $105: $575
# Risk: Unlimited above $110
# Plan: Close immediately after earnings
```

**Better Alternative**:

```python
# Use defined risk bull call spread instead
bull_call_spread("STOCK", 100.0, 105.0, "251219", 1, 2.50)

# Max profit: $250
# Max loss: $250
# No unlimited risk
```

## Related Strategies

- [Vertical Spreads](vertical-spreads.md) - Defined risk alternatives
- [Calendar Spreads](calendar-spreads.md) - Time-based alternatives
- [Butterfly Spreads](butterfly-spreads.md) - Similar profit profile with
  defined risk

## Summary

**Call Ratio Spread**: Bullish strategy with unlimited upside risk. Profits if
stock rises to short strike but loses if it rises too much.

**Put Ratio Spread**: Bearish strategy with significant downside risk. Profits
if stock falls to short strike but loses if it falls too much.

**Key Takeaway**: Ratio spreads are advanced strategies with undefined risk that
require active management and are not suitable for most traders. The unlimited
risk aspect makes them dangerous, and defined-risk alternatives (vertical
spreads, butterflies) usually provide better risk/reward profiles for most
market conditions.

**Recommendation**: Unless you're an experienced trader with a very specific
market view and risk management plan, use vertical spreads instead of ratio
spreads.
