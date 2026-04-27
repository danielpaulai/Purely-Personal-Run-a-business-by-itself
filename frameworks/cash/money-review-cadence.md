# Money Review Cadence · Daily · Weekly · Monthly · Quarterly

> Cash discipline isn't a vibe · it's a calendar. 4 reviews. Different
> depths. Different frequencies. Each catches different problems
> before they're crises.

---

## The 4 reviews

```
DAILY     ·  60 sec  ·  cash position glance
WEEKLY    ·  20 min  ·  forecast + Profit First transfers
MONTHLY   ·  60 min  ·  P&L + unit economics
QUARTERLY ·  3 hrs   ·  full audit + next-quarter plan
```

Skipping any one creates blind spots. Most operators do quarterly
only · then panic at month 2. The daily + weekly catch issues 8
weeks earlier than monthly.

---

## DAILY · 60 SECONDS · cash position glance

Once a day · 60 seconds · before you start work.

**What to check:**
```
[ ] Bank account balances (5 Profit First accounts)
[ ] Stripe today's gross
[ ] Any flagged transactions (failed charges · large expenses)
[ ] Number of paid customers active
```

**Best time:** first thing in the morning · with coffee. Before
email. Before Slack.

**The discipline question:** "Did anything happen yesterday I should
react to today?"

If yes · respond. If no · move on. 60 seconds done.

**Trap:** turning the daily into an obsessive Stripe-refresh.
Don't. 60 seconds maximum. Set a timer if needed.

---

## WEEKLY · 20 MINUTES · forecast + transfers

Once a week · Friday afternoon (best) · before the weekend.

**What to do:**

```
1 · Run /cash-engine for the week's wrap (5 min)
2 · Review the 13-week forecast · update assumptions (5 min)
3 · Check Profit First transfers (10th and 25th cycle)
4 · Reconcile any expense variance from forecast
5 · Note 1-2 specific actions for next week
```

**Outputs:**
- Updated 13-week cash forecast
- Profit First transfers (if it's the 10th or 25th)
- Friday wrap saved to Drive
- Monday's first action queued

**The discipline question:** "Where is cash flow going to be 4-13
weeks from now if I do nothing different?"

The forecast tells you. React early.

---

## MONTHLY · 60 MINUTES · P&L + unit economics

Once a month · last Friday or first Monday of the month.

**What to do:**

```
1 · Pull last month's full P&L (15 min)
   - Revenue · Cost of Goods Sold · Operating Expenses · Profit

2 · Calculate unit economics (15 min)
   - CAC · LTV · LTV/CAC · Gross Margin · Payback
   - See `cash/unit-economics.md`

3 · Review against last 3 months' trend (10 min)
   - What's improving?
   - What's declining?
   - What's the master ratio LTV/CAC trending toward?

4 · Profit First quarterly distribution (if quarter-end)
   - Distribute 50% of PROFIT account to owner
   - 50% stays in PROFIT for war chest

5 · Set next month's targets (15 min)
   - Revenue target
   - One unit-economics improvement
   - One specific cost reduction OR investment

6 · Save dashboard to Drive (5 min)
```

**Outputs:**
- Monthly P&L (saved + filed)
- Unit economics dashboard
- Trend chart (vs last 3 months)
- Next month's targets in BUSINESS-BRAIN.md § Numbers

**The discipline question:** "What's the ONE number I want to move
this month?"

Pick one. Track only that one. Move it.

---

## QUARTERLY · 3 HOURS · full audit + plan

Once a quarter · last Friday of the quarter.

**What to do:**

```
1 · 8-Integrity Audit (30 min)
   - Score Mission, Team, Leader, Product, Legal, Systems, Comms,
     Cash · 0-10 each
   - See `cash/business-integrity-triangle.md`
   - Identify the weakest integrity · plan next quarter's fix

2 · Cashflow Quadrant Review (30 min)
   - What % of last quarter's revenue came from each quadrant?
   - Where do you want to be next quarter?
   - What's the systemization plan to shift weight?
   - See `cash/cashflow-quadrant.md`

3 · Profit First Calibration (30 min)
   - Are the 4 percentages still right?
   - What's the PROFIT account balance vs target?
   - Quarterly distribution to owner (50% of PROFIT)
   - Adjust percentages if needed

4 · Pricing Audit (45 min)
   - Close rate trends
   - Customer feedback on price
   - Competitive positioning
   - Decision: raise prices? Add tiers? Discontinue?
   - See `cash/pricing-frameworks.md`

5 · Forecast Recalibration (45 min)
   - Build the next 13-week forecast from scratch
   - Compare to last quarter's forecast accuracy
   - Identify assumption errors · improve the model
   - See `cash/ninety-day-forecast.md`
```

**Outputs:**
- 8-integrity scorecard (filed · trend over quarters)
- Cashflow quadrant percentages
- Updated Profit First %s
- New pricing decisions
- Fresh 13-week forecast
- Next quarter's 1-3 Rocks
- Quarterly review document saved to Drive

**The discipline question:** "What 1-3 things, if shipped this
quarter, would change the trajectory of the business?"

Those are next quarter's Rocks. Everything else is noise.

---

## The 4-tier review map

```
DAILY      → catches 24-hour issues (failed payments, daily
              activity slumps)
WEEKLY     → catches 4-13 week cash flow issues
MONTHLY    → catches unit-economics drift (CAC creeping up,
              margin compressing)
QUARTERLY  → catches strategic drift (wrong quadrant, wrong
              integrity, wrong product)
```

Each cadence catches a different signal. Skipping a cadence creates
a blind spot.

---

## Calendar setup · install once · runs forever

```
EVERY MORNING (M-F)   ·  09:00  ·  60-sec money check
EVERY FRIDAY          ·  16:00  ·  20-min weekly review
LAST FRIDAY OF MONTH  ·  15:00  ·  60-min monthly review
LAST FRIDAY OF QUARTER ·  09:00  ·  3-hour quarterly review
```

Recurring calendar invites. Title them. Don't skip. Treat them like
client meetings (because YOU are the most important client).

---

## Time investment · the math

```
Daily:      60 sec × 5 days × 4 weeks = 20 min/month
Weekly:     20 min × 4 weeks = 80 min/month
Monthly:    60 min × 1 = 60 min/month
Quarterly:  180 min ÷ 3 = 60 min/month avg
                        ──────
Total time on money:    ~3.5 hrs/month
```

3.5 hours per month for full financial discipline. Most operators
spend 30+ hours per month panicking about money. The cadence trades
panic for ritual.

---

## What goes into BUSINESS-BRAIN.md § Numbers

After every monthly + quarterly review, update the Numbers section
of BUSINESS-BRAIN.md:

```yaml
# § Numbers

revenue:
  current_month_actual: $XX,XXX
  current_month_target: $XX,XXX
  trailing_3mo_avg: $XX,XXX
  trailing_12mo_total: $XXX,XXX

unit_economics:
  cac: $XXX
  ltv: $X,XXX
  ltv_cac_ratio: X.X
  gross_margin: XX%
  payback_months: X

profit_first:
  profit_pct: 5%
  owner_pay_pct: 60%
  tax_pct: 15%
  opex_pct: 20%
  profit_account_balance: $X,XXX
  next_distribution_target: $X,XXX

forecast:
  current_balance: $XX,XXX
  week_4_projected: $XX,XXX
  week_13_projected: $XX,XXX
  status: GREEN | YELLOW | RED

quadrant_mix:
  S_pct: XX%
  B_pct: XX%
  I_pct: XX%
  target_next_quarter: shift S→B by X%

quarterly_rocks:
  - rock_1: ...
  - rock_2: ...
  - rock_3: ...
```

This section becomes the live financial truth of the business.
Updated monthly. Trusted. Acted on.

---

## Apply it to /cash-engine

The engine should support all 4 cadences:

### Daily mode (60-sec brief):
```bash
/cash-engine daily
```
Outputs: bank balances, today's Stripe gross, flags.

### Weekly mode (Friday wrap):
```bash
/cash-engine weekly
```
Outputs: full Friday wrap, forecast update, Profit First transfer
suggestion, action items.

### Monthly mode:
```bash
/cash-engine monthly
```
Outputs: P&L, unit economics dashboard, trend charts, next month's
targets.

### Quarterly mode:
```bash
/cash-engine quarterly
```
Outputs: 8-integrity audit, quadrant review, pricing audit, fresh
13-week forecast, Rocks template.

The engine reads BUSINESS-BRAIN.md § Numbers, pulls live data from
Stripe + Notion, runs the analysis, and saves outputs to Drive
in standardized locations.

---

## The 1-question dashboard

Every review · regardless of cadence · ends with answering ONE
question:

> "What ONE specific action will I take in the next 7 days based on
> what I just saw?"

Write it down. Calendar it. Do it.

If you can't name a specific action · the review was just
information consumption. The discipline ISN'T in the review · it's
in the action that follows.

---

## When the cadence saves you

Real scenarios where this cadence catches issues:

**Daily catches:** failed payment from a top customer · respond
within 24 hours · keep them.

**Weekly catches:** pipeline conversion dropped 40% this week ·
investigate Monday · likely fix in 2 weeks.

**Monthly catches:** CAC has crept up 15% over 3 months · shifts
acquisition strategy before LTV/CAC drops below 2.

**Quarterly catches:** S-quadrant work has expanded again · time to
re-systemize · shift the quadrant mix.

Each cadence catches a different time horizon. Together they form
a complete defense against financial drift.
