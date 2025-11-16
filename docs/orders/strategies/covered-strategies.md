# Covered Strategies

Covered strategies involve owning (or having cash to cover) the underlying stock
and selling options against that position to generate income.

## Covered Call

**Market Outlook**: Neutral to slightly bullish

**Risk Profile**: Undefined downside risk (owning stock), capped upside

### Strategy Overview

Own 100 shares of stock and sell 1 call option contract against it. Generate
income from the call premium while maintaining stock ownership.

- **Requirement**: Own 100 shares per contract
- **Sell**: Out-of-the-money call
- **Income**: Call premium received
- **Max Profit**: Strike price - stock cost + premium
- **Max Loss**: Stock price falls to zero (offset by premium received)
- **Breakeven**: Stock purchase price - premium received

### When to Use

- Own stock and expect it to trade sideways or rise modestly
- Want to generate income on existing holdings
- Willing to sell stock at the strike price
- Comfortable with capped upside
- In a neutral to slightly bullish market environment

### Code Example

```python
from datetime import date
from tastypy.orders.templates import covered_call

# You own 100 shares of AAPL at $148
# Sell a covered call at $155 for income
order = covered_call(
    underlying="AAPL",
    strike=155.0,        # Willing to sell at $155
    expiration=date(2025, 12, 19),
    quantity=1,          # 1 contract = 100 shares
    limit_price=2.50     # Collect min $2.50/share = $250
)
```

### Example P&L Scenarios

Assume you own AAPL at $148, sell 155 call for $2.50:

| AAPL Price at Expiration | Stock P&L | Option P&L | Total P&L | Notes                                 |
| ------------------------ | --------- | ---------- | --------- | ------------------------------------- |
| $140                     | -$800     | +$250      | -$550     | Option profit cushions stock loss     |
| $145.50                  | -$250     | +$250      | $0        | Breakeven point                       |
| $148                     | $0        | +$250      | +$250     | Keep stock + premium                  |
| $155                     | +$700     | +$250      | +$950     | Max profit - stock called away        |
| $160                     | +$1,200   | -$250      | +$950     | Stock called away, missed $500 upside |

### Greeks Profile

- **Delta**: Long stock (1.0) minus short call delta (e.g., -0.30) = net 0.70
  delta
- **Theta**: Positive (benefit from time decay of short call)
- **Vega**: Negative (benefit from falling volatility in call)
- **Gamma**: Negative (from short call)

### Strike Selection

**Conservative (Higher probability of keeping stock)**:

- Sell calls 10-20% OTM
- Lower premium collected
- Higher chance of expiring worthless
- Example: Stock at $150, sell $165 call

**Moderate**:

- Sell calls 5-10% OTM
- Balanced premium and probability
- Example: Stock at $150, sell $155-160 call

**Aggressive (Higher income, higher assignment risk)**:

- Sell at-the-money or slightly OTM calls
- Maximum premium collected
- High chance of assignment
- Example: Stock at $150, sell $150-152 call

### Management Strategies

**If stock stays below strike** (Ideal):

- Let option expire worthless
- Keep premium and stock
- Sell another call for next month

**If stock approaches strike**:

- Let stock get called away and keep max profit
- Roll up and out: Buy back the call, sell a higher strike in later month
- Close the call, keep the stock

**If stock drops significantly**:

- Let call expire worthless, keep premium as income
- Consider selling another call at lower strike
- Or exit stock position if outlook has changed

**Rolling Technique**:

```python
# Buy back the Dec 155 call
# Sell Jan 160 call for additional credit
# Continue generating income while giving stock more room to run
```

---

## Covered Put (Cash-Secured Put)

**Market Outlook**: Neutral to slightly bearish, or want to own stock at lower
price

**Risk Profile**: Undefined downside risk, defined upside (premium only)

### Strategy Overview

Sell a put option with cash set aside to purchase the stock if assigned.
Generate income while potentially buying stock at a discount.

- **Requirement**: Cash = strike × 100 × quantity
- **Sell**: Out-of-the-money put
- **Income**: Put premium received
- **Max Profit**: Premium received (if stock stays above strike)
- **Max Loss**: Strike price - premium (if stock goes to zero)
- **Breakeven**: Strike price - premium

### When to Use

- Want to buy stock but think it might drop first
- Willing to buy stock at the strike price
- Want to generate income while waiting to buy
- Neutral to slightly bearish short-term outlook
- Have cash sitting idle and want to put it to work

### Code Example

```python
from datetime import date
from tastypy.orders.templates import covered_put

# Want to buy AAPL if it drops to $145
# AAPL currently at $150
order = covered_put(
    underlying="AAPL",
    strike=145.0,        # Willing to buy at $145
    expiration=date(2025, 12, 19),
    quantity=1,          # Need $14,500 cash
    limit_price=2.00     # Collect min $2.00/share = $200
)
```

### Example P&L Scenarios

Assume AAPL at $150, sell 145 put for $2.00:

| AAPL Price at Expiration | Outcome     | P&L     | Notes                                            |
| ------------------------ | ----------- | ------- | ------------------------------------------------ |
| $155                     | Put expires | +$200   | Keep premium, no assignment                      |
| $150                     | Put expires | +$200   | Stock didn't drop, keep premium                  |
| $145                     | Assigned    | +$200   | Buy stock at $145, effective cost $143           |
| $143                     | Assigned    | $0      | Breakeven: $145 - $2 premium                     |
| $140                     | Assigned    | -$300   | Own stock at $145, now worth $140, net $143 cost |
| $130                     | Assigned    | -$1,300 | Own stock at $145, now worth $130, net $143 cost |

### Greeks Profile

- **Delta**: Negative (short put delta, e.g., -0.30)
- **Theta**: Positive (benefit from time decay)
- **Vega**: Negative (benefit from falling volatility)
- **Gamma**: Negative

### Strike Selection

**Conservative (Lower assignment probability)**:

- Sell puts 10-20% OTM
- Lower premium
- Want to collect income, not get assigned
- Example: Stock at $150, sell $130-135 put

**Moderate (Balanced approach)**:

- Sell puts 5-10% OTM
- Decent premium, moderate assignment risk
- Example: Stock at $150, sell $140-145 put

**Aggressive (Want to own stock)**:

- Sell at-the-money puts
- Maximum premium
- High probability of assignment
- Essentially buying stock at discount via premium collected
- Example: Stock at $150, sell $150 put

### Management Strategies

**If stock stays above strike** (Ideal for income):

- Let put expire worthless
- Keep premium
- Sell another put for next month

**If stock drops toward strike**:

- Let assignment happen if you want to own stock
- Roll down and out: Buy back put, sell lower strike in later month (collect
  credit)
- Close the put to avoid assignment

**If assigned**:

- Now you own stock at the strike price (minus premium collected)
- Can start selling covered calls for additional income ("wheel strategy")
- Or hold stock if bullish

**The Wheel Strategy**:

1. Sell cash-secured put
2. If assigned, own stock
3. Sell covered call on stock
4. If called away, back to step 1
5. Generate income at each step

---

## Covered Strategy Comparison

| Aspect      | Covered Call               | Cash-Secured Put            |
| ----------- | -------------------------- | --------------------------- |
| Requirement | Own 100 shares             | Cash = strike × 100         |
| Direction   | Neutral to bullish         | Neutral to bearish          |
| Goal        | Income on stock            | Income or stock acquisition |
| Assignment  | Stock called away          | Stock put to you            |
| Risk        | Stock drops                | Stock drops                 |
| Max Profit  | Limited (strike + premium) | Premium only                |

## Common Mistakes

1. **Selling calls on stock you don't want to lose**: Only sell calls if willing
   to part with stock at strike
2. **Wrong strike selection**: Don't sell ITM options unless intentionally
   planning assignment
3. **Ignoring earnings**: Calls/puts can get assigned early before earnings
4. **Not rolling**: Missing opportunities to extend the trade and collect more
   premium
5. **Overleveraging**: Don't sell more puts than you have cash to cover
6. **Ignoring dividends**: Ex-dividend dates can trigger early assignment
7. **Tax implications**: Short-term vs long-term capital gains if stock is
   called away

## Tax Considerations

### Covered Calls

- If assigned: Gain/loss calculated from original stock purchase price to
  strike + premium
- If held < 1 year: Short-term capital gains (ordinary income rates)
- If held > 1 year: Long-term capital gains (lower rates)
- **Caution**: Selling ITM calls can reset holding period

### Cash-Secured Puts

- If expires worthless: Premium is short-term capital gain
- If assigned: Premium reduces cost basis of stock

**Consult a tax professional for your specific situation.**

## Best Practices

### Timing

- **30-45 days to expiration**: Sweet spot for time decay
- **Weekly options**: More frequent income, more management required
- **Monthly options**: Less management, larger premium per trade

### Premium Targets

- **Covered calls**: Aim for 1-3% of stock price per month
- **Cash-secured puts**: Aim for 1-2% of strike price per month

### Rolling Decisions

- **Roll out**: Same strike, later expiration (collect more time premium)
- **Roll up**: Higher strike, same or later expiration (covered calls)
- **Roll down**: Lower strike, same or later expiration (cash-secured puts)
- **Always collect a credit**: Don't roll for a debit

## Related Strategies

- [Vertical Spreads](vertical-spreads.md) - Don't require stock ownership
- [Collar Strategy](https://www.investopedia.com/terms/c/collar.asp) - Covered
  call + protective put
- [Poor Man's Covered Call](https://www.investopedia.com/terms/p/pmcc.asp) - Use
  LEAPS instead of stock
- [The Wheel Strategy](https://www.reddit.com/r/thetagang/) - Systematic covered
  call/put rotation
