# Sales Frameworks · Index

The framework library `/sales-engine` reads from before drafting any
sales asset. Each framework is operator-grade — pulled from systems
that have closed billions in revenue.

## When to use which

| Framework | When |
|---|---|
| [nepq-questions.md](nepq-questions.md) | Live sales calls · 5 question types · 70/30 talk-listen ratio |
| [grand-slam-offer.md](grand-slam-offer.md) | Building a new offer · 4-lever value-equation construction · 11-point audit |
| [qualification-bant-meddic-spin.md](qualification-bant-meddic-spin.md) | Pre-call qualification · pick by deal size (BANT/SPIN/MEDDIC) |
| [cold-outreach-cadence.md](cold-outreach-cadence.md) | Cold DMs / emails · 3-step or 7-touch sequences |
| [objection-handling.md](objection-handling.md) | The 5 universal objections · pre-handling + real-time scripts |
| [decisive-close.md](decisive-close.md) | The 4 levels of close · the standing-up close · 1-line closer |
| [price-anchoring.md](price-anchoring.md) | Anchor high · stack value · decoy effect · the contrast principle |

## How `/sales-engine` uses these

When generating Tuesday Lead Research:

1. Reads BUSINESS-BRAIN.md for ICP, offer, voice
2. Apify scrapes 10 prospects matching ICP
3. Each prospect scored against `qualification-bant-meddic-spin.md` BANT criteria
4. Top 3 (BANT > 80) get 3-step outreach using `cold-outreach-cadence.md`
5. Each outreach sentence audited for 3-specifics personalization

When generating Thursday Meeting Prep:

1. Reads tomorrow's calendar
2. Apify scrapes each external attendee
3. Generates NEPQ questions tailored to prospect (`nepq-questions.md`)
4. Generates likely objections + responses (`objection-handling.md`)
5. Generates trial close + decisive close lines (`decisive-close.md`)
6. Saves brief to Gmail Drafts

When you're building a new offer:

1. Run the 11-point audit from `grand-slam-offer.md`
2. Apply 4-lever value equation (`marketing/value-equation.md`)
3. Construct the stack with retail anchors (`price-anchoring.md`)
4. Pre-script the 5 objection responses (`objection-handling.md`)
5. Pre-script the decisive close (`decisive-close.md`)

## The sales-call playbook (combine all 7)

```
PRE-CALL    · qualification (BANT/SPIN/MEDDIC) · NEPQ prep
OPENING     · 60-sec connection question (NEPQ Stage 1)
DISCOVERY   · 5 question types · 25 min · 70/30 ratio (NEPQ Stage 2)
PRESENT     · stack + price anchoring + decoy
HANDLE      · 5 universal objection responses
CLOSE       · decisive close (Level 3) · standing-up move
LOCK        · payment confirmation BEFORE call ends
```

## Editing rules

- Files are LIVE · the engine reads them every run
- Edit any file to update behavior immediately
- Add new frameworks as new `.md` files · update this README
- Keep file names slug-style (kebab-case)

## Source canon (no name credit · structures only)

These frameworks compress the working principles from:
- NEPQ (Neuro-Emotional Persuasion Questions) by major modern operators
- $100M Offers · Grand Slam Offer construction · 4-lever math
- Classic BANT (1960s IBM-era) · SPIN (consultative) · MEDDIC (enterprise)
- 7-touch outreach cadences from top B2B operators
- The 5 universal objections (timeless · same for 100 years)
- The decisive close + standing-up close from live-launch operators
- Price anchoring · decoy effect · Cialdini's contrast principle
