# Purely Personal · Frameworks Library

> The intellectual core underneath all 5 engines. 38 framework files
> across 5 directories · curated from operator canon · structures
> only (no name credit). The engines READ from these before
> generating output. Edit any file → engine behavior updates
> immediately.

---

## Directory map

```
frameworks/
├── marketing/          ·  9 files · LinkedIn · newsletter · webinar · brand
├── sales/              ·  7 files · NEPQ · BANT · outreach · close · price
├── operations/         ·  7 files · 4DX · habits · L10 · PARA · SOP
├── cash/               ·  7 files · Profit First · quadrant · forecast · pricing
└── leadership/         ·  8 files · identity · mindset · faculties · WIG · V/TO · 10X
                       ─────────
                        38 framework files + 5 READMEs + this index
```

---

## How the engines use it

```
/marketing-engine      reads → frameworks/marketing/
/sales-engine          reads → frameworks/sales/
/operations-engine     reads → frameworks/operations/
/cash-engine           reads → frameworks/cash/
/leadership-engine     reads → frameworks/leadership/
```

Each engine command file (in `commands/`) explicitly references the
relevant framework files. When you run an engine, it loads:

1. `BUSINESS-BRAIN.md` (your business context)
2. The engine's framework directory (the structures to apply)
3. Generates output that's grounded in BOTH

Without the frameworks, engines produce decent output (Claude's
internal knowledge). With the frameworks, output is consistent,
operator-grade, and aligned to your specific stage.

---

## Quick reference · which framework for which job

### Marketing
- Writing a LinkedIn post → `linkedin-hooks.md` + `hook-story-offer.md`
- Drafting a newsletter → `newsletter-structures.md` + `storybrand-narrative.md`
- Building a sales page → `storybrand-narrative.md` + `aida-pas-bab.md`
- Auditing an offer → `value-equation.md`
- Planning a launch → `perfect-webinar.md`
- Setting content rhythm → `content-pillars.md`
- Algorithm-aware design → `hook-retain-reward.md`

### Sales
- Live sales call → `nepq-questions.md` + `decisive-close.md`
- Building an offer → `grand-slam-offer.md` + `price-anchoring.md`
- Cold outreach → `cold-outreach-cadence.md`
- Qualifying prospects → `qualification-bant-meddic-spin.md`
- Handling objections → `objection-handling.md`

### Operations
- Weekly meeting → `eos-level-10-meeting.md`
- Setting WIGs / scoreboard → `four-disciplines-execution.md`
- Designing a routine → `atomic-habits-4-laws.md`
- Filing knowledge → `para-second-brain.md`
- Daily prioritization → `eisenhower-matrix.md`
- Writing an SOP → `sop-template.md`
- Deciding what to build → `automation-hierarchy.md`

### Cash
- Setting up cash discipline → `profit-first.md`
- Understanding your money mix → `cashflow-quadrant.md`
- Auditing the business → `business-integrity-triangle.md`
- Knowing your numbers → `unit-economics.md`
- Setting prices → `pricing-frameworks.md`
- Forecasting → `ninety-day-forecast.md`
- Review rhythm → `money-review-cadence.md`

### Leadership
- Daily identity → `identity-based-habits.md`
- Quarterly mindset audit → `wealth-mindset.md`
- Decision quality → `six-mental-faculties.md`
- Strategic operating system → `scaling-up-4-decisions.md`
- Picking goals → `wildly-important-goals.md`
- 2-page strategy → `vision-traction-organizer.md`
- Big goal-setting → `ten-x-mindset.md`
- Calendar design → `maker-vs-manager.md`

---

## The full file list

### `frameworks/marketing/` (9 files)
- [README.md](marketing/README.md)
- [value-equation.md](marketing/value-equation.md)
- [hook-story-offer.md](marketing/hook-story-offer.md)
- [storybrand-narrative.md](marketing/storybrand-narrative.md)
- [linkedin-hooks.md](marketing/linkedin-hooks.md)
- [aida-pas-bab.md](marketing/aida-pas-bab.md)
- [perfect-webinar.md](marketing/perfect-webinar.md)
- [newsletter-structures.md](marketing/newsletter-structures.md)
- [content-pillars.md](marketing/content-pillars.md)
- [hook-retain-reward.md](marketing/hook-retain-reward.md)

### `frameworks/sales/` (7 files)
- [README.md](sales/README.md)
- [nepq-questions.md](sales/nepq-questions.md)
- [grand-slam-offer.md](sales/grand-slam-offer.md)
- [qualification-bant-meddic-spin.md](sales/qualification-bant-meddic-spin.md)
- [cold-outreach-cadence.md](sales/cold-outreach-cadence.md)
- [objection-handling.md](sales/objection-handling.md)
- [decisive-close.md](sales/decisive-close.md)
- [price-anchoring.md](sales/price-anchoring.md)

### `frameworks/operations/` (7 files)
- [README.md](operations/README.md)
- [four-disciplines-execution.md](operations/four-disciplines-execution.md)
- [atomic-habits-4-laws.md](operations/atomic-habits-4-laws.md)
- [eos-level-10-meeting.md](operations/eos-level-10-meeting.md)
- [para-second-brain.md](operations/para-second-brain.md)
- [eisenhower-matrix.md](operations/eisenhower-matrix.md)
- [sop-template.md](operations/sop-template.md)
- [automation-hierarchy.md](operations/automation-hierarchy.md)

### `frameworks/cash/` (7 files)
- [README.md](cash/README.md)
- [profit-first.md](cash/profit-first.md)
- [cashflow-quadrant.md](cash/cashflow-quadrant.md)
- [business-integrity-triangle.md](cash/business-integrity-triangle.md)
- [unit-economics.md](cash/unit-economics.md)
- [pricing-frameworks.md](cash/pricing-frameworks.md)
- [ninety-day-forecast.md](cash/ninety-day-forecast.md)
- [money-review-cadence.md](cash/money-review-cadence.md)

### `frameworks/leadership/` (8 files)
- [README.md](leadership/README.md)
- [identity-based-habits.md](leadership/identity-based-habits.md)
- [wealth-mindset.md](leadership/wealth-mindset.md)
- [six-mental-faculties.md](leadership/six-mental-faculties.md)
- [scaling-up-4-decisions.md](leadership/scaling-up-4-decisions.md)
- [wildly-important-goals.md](leadership/wildly-important-goals.md)
- [vision-traction-organizer.md](leadership/vision-traction-organizer.md)
- [ten-x-mindset.md](leadership/ten-x-mindset.md)
- [maker-vs-manager.md](leadership/maker-vs-manager.md)

---

## Editing rules

- **Files are LIVE** · the engines read them every time they run
- **Edit any file** to update engine behavior immediately · no rebuild required
- **Add new frameworks** as new `.md` files in the relevant directory · update the directory's `README.md`
- **Naming convention** · slug-style (kebab-case) · `linkedin-hooks.md` not `Linkedin Hooks.md`
- **File length** · keep under ~500 lines · longer = ignored by engines

---

## How to add YOUR own framework

If you have a framework specific to your business or your unique
take · add it. The engine will read it alongside the canonical ones.

1. Pick the right directory (marketing / sales / ops / cash /
   leadership)
2. Create a new `.md` file (slug-style name)
3. Follow the same structure as existing frameworks:
   - **What it is** · the core principle in 1-2 sentences
   - **The structure** · the steps / parts / mechanism
   - **Worked examples** · ideally from YOUR business
   - **When to use** · explicit triggers
   - **Common mistakes** · what kills the framework
   - **Apply it** · how the engine should use it
4. Add a row to that directory's `README.md`
5. Reference it in BUSINESS-BRAIN.md if business-critical

---

## Source canon (no name credit · structures only)

These frameworks compress the working principles from operators who
have moved billions of dollars · taught millions of students · and
shaped how the most successful founders think:

**Offer construction + value math:**
- $100M Offers value-equation discipline
- Grand Slam Offer 4-lever construction
- Price anchoring + decoy effect (Cialdini canon)

**Storytelling + narrative:**
- DotCom/Expert Secrets hook-story-offer
- StoryBrand 7-part narrative structure
- AIDA / PAS / BAB · the 100-year copywriting canon
- Perfect Webinar 4-question close

**Sales methodology:**
- NEPQ (Neuro-Emotional Persuasion Questions)
- Classic BANT · SPIN · MEDDIC qualification
- The 5 universal objections
- The decisive close + standing-up close

**Operating discipline:**
- 4 Disciplines of Execution · WIGs · lead vs lag · scoreboards
- Atomic Habits · 4 laws · identity-based habits · 1% compounding
- EOS · Level 10 meeting · IDS · quarterly Rocks · V/TO
- Building a Second Brain / PARA · knowledge architecture
- Eisenhower Matrix · the urgent/important framing
- Maker vs Manager schedule · the calendar fundamentals

**Money + capital:**
- Profit First · 5-account cash discipline
- Cashflow Quadrant · E/S/B/I model
- Business Integrity Triangle · 8 pieces of a real business
- Unit economics · CAC/LTV/payback (canonical SaaS metrics)
- Rolling 13-week cash flow forecasting

**Mindset + leadership:**
- The 17 wealth patterns · operator-life psychology
- The 6 mental faculties · classic mind-as-OS philosophy
- Scaling Up · 4 decisions · operating-team standard
- The 10X Rule · why bigger goals are mathematically easier

These are the structures behind the structures. Names compressed.
Wisdom retained. Use them.
