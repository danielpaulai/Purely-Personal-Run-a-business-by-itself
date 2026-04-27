# Cash Frameworks · Index

The framework library `/cash-engine` reads from before generating any
financial output. Each framework is operator-grade · pulled from
real businesses managing real money.

## When to use which

| Framework | When |
|---|---|
| [profit-first.md](profit-first.md) | The 5-account cash discipline · pay profit first · OpEx cap |
| [cashflow-quadrant.md](cashflow-quadrant.md) | The E/S/B/I model · why some money compounds and other money doesn't |
| [business-integrity-triangle.md](business-integrity-triangle.md) | 8 integrities of a real business · audit + fix order |
| [unit-economics.md](unit-economics.md) | The 5 numbers · CAC · LTV · LTV/CAC · margin · payback |
| [pricing-frameworks.md](pricing-frameworks.md) | 5 methods · cost-plus · competitive · value-based · anchoring · decoy |
| [ninety-day-forecast.md](ninety-day-forecast.md) | Rolling 13-week cash flow forecast · weekly update protocol |
| [money-review-cadence.md](money-review-cadence.md) | Daily / Weekly / Monthly / Quarterly review rhythm |

## How `/cash-engine` uses these

When generating Friday Cash Wrap:

1. Reads BUSINESS-BRAIN.md § Numbers for current state
2. Pulls Stripe revenue + linked expense tracking
3. Updates 13-week forecast (`ninety-day-forecast.md`)
4. Calculates Profit First transfer amounts (`profit-first.md`)
5. Runs unit-economics audit (`unit-economics.md`)
6. Saves dashboard to Drive

When generating Monthly Review:

1. Pulls last 30 days of revenue + expense data
2. Generates P&L + unit-economics dashboard
3. Compares to last 3 months · trend
4. Surfaces drift (CAC creep · margin compression)
5. Sets next month's 1 priority

When generating Quarterly Review:

1. Runs 8-integrity audit (`business-integrity-triangle.md`)
2. Cashflow Quadrant mix audit (`cashflow-quadrant.md`)
3. Profit First calibration (`profit-first.md`)
4. Pricing audit (`pricing-frameworks.md`)
5. Fresh 13-week forecast
6. Saves quarterly review document to Drive

## The cash discipline cycle (combine all 7)

```
DAILY     ·  60 sec  ·  bank glance + Stripe pulse
WEEKLY    ·  20 min  ·  /cash-engine weekly · forecast + transfers
MONTHLY   ·  60 min  ·  P&L + unit economics + 1 priority
QUARTERLY ·  3 hrs   ·  8-integrity audit + quadrant + pricing
                        + fresh forecast + Rocks
```

Total: ~3.5 hrs/month of financial discipline. Catches issues 8 weeks
before they become crises.

## Editing rules

- Files are LIVE · the engine reads them every run
- Edit any file to update behavior immediately
- Add new frameworks as new `.md` files · update this README
- Keep file names slug-style (kebab-case)

## Source canon (no name credit · structures only)

These frameworks compress the working principles from:
- Profit First · 5-account cash discipline
- Cashflow Quadrant · E/S/B/I model · active vs passive income
- Business Integrity Triangle · the 8 pieces of a real business
- Unit Economics · CAC/LTV/LTV-CAC/Margin/Payback (canonical SaaS metrics)
- Value-based pricing + anchoring + decoy effect (Cialdini canon)
- Rolling 13-week cash flow forecasting (operator-grade discipline)
- 4-tier review cadence (daily/weekly/monthly/quarterly · finance-team practice)
