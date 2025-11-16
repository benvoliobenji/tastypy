# Calendar Spreads

Calendar spreads (also called time spreads or horizontal spreads) profit from
the difference in time decay between two options at the same strike but
different expirations.

## Call Calendar Spread

**Market Outlook**: Neutral to slightly bullish

**Risk Profile**: Defined risk, potentially undefined reward

### Strategy Overview

Sell a near-term call and buy a longer-term call at the same strike. Profits
from time decay of the short-term option while maintaining long-term exposure.

- **Sell**: Near-term call
- **Buy**: Far-term call (same strike)
- **Net Cost**: Debit (pay to enter)
- **Max Loss**: Net debit paid (if far option expires worthless)
- **Max Profit**: Varies (achieved when near option expires with stock at
  strike)
- **Breakeven**: Complex - depends on remaining value of long option

### When to Use

- Neutral to slightly bullish outlook
- Expecting low volatility in near term, potential movement later
- High implied volatility in near-term options
- After earnings pass (front month IV elevated)
- Want to own longer-term option at reduced cost

### Code Example

```python
from datetime import date
from tastypy.orders.templates import call_calendar_spread

# AAPL at $150, sell Dec calls, buy Jan calls
order = call_calendar_spread(
    underlying="AAPL",
    strike=150.0,            # Same strike for both
    near_expiration=date(2025, 12, 19), # December 2025
    far_expiration=date(2026, 1, 16),  # January 2026
    quantity=1,
    limit_price=2.50         # Pay max $2.50 debit
)
```

### Example P&L at Near Expiration

Assume AAPL at $150, sell Dec 150 call, buy Jan 150 call for $2.50:

| AAPL Price at Dec Expiration | Approximate P&L | Notes                                           |
| ---------------------------- | --------------- | ----------------------------------------------- |
| $140                         | -$100 to -$150  | Both OTM, long option has some value left       |
| $150                         | +$200 to +$300  | Optimal - short expires, long retains max value |
| $160                         | -$100 to +$100  | Both ITM, spread compresses                     |

**Note**: P&L at near expiration depends heavily on implied volatility and
remaining time value of the long option.

### Greeks Profile

- **Delta**: Small positive delta if stock is near strike
- **Theta**: Positive in near term (short option decays faster)
- **Vega**: Positive (benefits from IV increase in longer-term option)
- **Gamma**: Complex - depends on which option dominates

---

## Put Calendar Spread

**Market Outlook**: Neutral to slightly bearish

**Risk Profile**: Defined risk, potentially undefined reward

### Strategy Overview

Identical structure to call calendar but using puts. Sell near-term put, buy
far-term put at same strike.

### Code Example

```python
from datetime import date
from tastypy.orders.templates import put_calendar_spread

# AAPL at $150, expecting support at $150
order = put_calendar_spread(
    underlying="AAPL",
    strike=150.0,
    near_expiration=date(2025, 12, 19),
    far_expiration=date(2026, 1, 16),
    quantity=1,
    limit_price=2.50
)
```

## Strike Selection

### At-the-Money (ATM)

- **Most common**: Strike at current stock price
- **Pros**: Maximum time decay differential
- **Cons**: Requires price to stay very close to strike

### Out-of-the-Money (OTM)

- **Directional bias**: Call calendars above, put calendars below current price
- **Pros**: Lower cost, directional exposure
- **Cons**: Less time decay advantage

### In-the-Money (ITM)

- **Rare**: Usually not optimal
- **Use case**: Want intrinsic value protection

## Management Strategies

### At Near Expiration

**If stock is at strike** (Ideal):

1. Let short option expire worthless
2. Keep long option - now a simple long call/put
3. Option 1: Sell the long option for profit
4. Option 2: Sell another near-term option (roll into new calendar)

**If stock moved away from strike**:

- Close entire spread
- Usually results in small loss to small profit
- Don't let it become a max loss

### Rolling Calendars

**Convert to "diagonal"**:

- After near option expires, sell new near-term option at different strike
- Follow the stock's movement
- Continue collecting time decay

**Example**:

1. Start: Dec 150/Jan 150 calendar, AAPL at $150
2. Dec expires, AAPL now at $155
3. Sell Jan 155 call (now you have Jan 150/Jan 155 long call vertical)
4. Or sell Feb 155 call (now you have Jan 150/Feb 155 diagonal)

## Advanced Techniques

### Double Calendar (Iron Calendar)

Combine call calendar and put calendar:

- Sell near-term strangle
- Buy far-term strangle
- Profits from time decay on both sides
- Wider profit zone than single calendar

### Calendar Spread as Earnings Play

**Pre-earnings**:

- Near-term option has inflated IV
- After earnings, IV crushes in near-term
- Far-term less affected
- Calendar spread widens = profit

**Setup**: 1-2 weeks before earnings, exit right after earnings announcement

## Risks and Considerations

### Assignment Risk

- If short option goes ITM near expiration, can be assigned early
- You'll be short stock but still own long call
- Usually best to close or roll before this happens

### Volatility Risk

- Calendar spreads are vega positive
- Need IV to stay elevated or increase
- If IV collapses across all expirations, can lose

### Time Decay Timing

- Sweet spot: 30-60 days to near expiration, 60-120+ days to far expiration
- Too short: Not enough time decay differential
- Too long: Pay too much premium upfront

### Liquidity

- Two-leg spread requires decent liquidity
- Use limit orders
- Wider bid-ask spreads can eat into profits

## Calendar vs Diagonal

| Aspect      | Calendar | Diagonal             |
| ----------- | -------- | -------------------- |
| Strikes     | Same     | Different            |
| Directional | Minimal  | More directional     |
| Time Decay  | Maximum  | Moderate             |
| Cost        | Moderate | Varies               |
| Best For    | Neutral  | Slightly directional |

**Diagonal Spreads**: Use different strikes and different expirations. Adds
directional bias to the time decay play.

## Common Mistakes

1. **Wrong expiration spread**: Need enough time difference (30+ days minimum)
2. **Ignoring volatility**: Need stable or rising IV for success
3. **Holding too long**: Should close or roll at/before near expiration
4. **Wrong strike**: ATM calendars need stock to stay very close to strike
5. **Poor entry timing**: Best when near-term IV is elevated
6. **Not rolling**: Missing opportunity to continue the trade after near
   expiration

## When Calendar Spreads Work Best

**Ideal Conditions**:

- Stock trading in a range
- Near-term IV elevated vs far-term
- Before/after earnings (near-term IV spike)
- No major catalysts in far-term period
- High liquidity in both expirations

**Avoid**:

- Strong trending markets
- Low volatility across all expirations
- When near and far IV are similar
- Poor liquidity in either expiration

## Related Strategies

- [Vertical Spreads](vertical-spreads.md) - Uses same expiration, different
  strikes
- [Butterfly Spreads](butterfly-spreads.md) - Another neutral strategy
- [Iron Condor](iron-condor.md) - Wider profit zone, credit spread
- [Covered Strategies](covered-strategies.md) - Alternative income strategies
