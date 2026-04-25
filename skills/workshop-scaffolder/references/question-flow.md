# Question Flow

The exact 8 questions to ask, in order, with defaults and validation. Follow this script verbatim.

---

## Q1 · Workshop name

**Ask:**
> "What's the workshop called?  Full title, the one you'd put on the landing page.  (e.g., Build Your Sales Machine in 30 Days)"

**Capture as:** `WORKSHOP_NAME` (string, 3–80 chars)

**Default:** none · required.

**Validation:** non-empty, no quotes wrapping. If user wraps in quotes, strip them.

---

## Q2 · Workshop slug

**Ask:**
> "Slug for URLs and folder names.  Kebab-case, no spaces.  Default: I'll generate one from your title.  Edit if you want."

Auto-suggest from Q1: lowercase, replace spaces with hyphens, strip non-alphanumeric except hyphen.
Example: `Build Your Sales Machine in 30 Days` → `build-your-sales-machine-in-30-days`. Suggest a tighter version: `sales-machine-30`.

**Capture as:** `WORKSHOP_SLUG` (string, kebab-case)

**Validation:** matches `^[a-z0-9]+(-[a-z0-9]+)*$`. If invalid, reject and re-suggest.

---

## Q3 · Workshop number

**Ask:**
> "Workshop number.  Default: 02 (next after Workshop 01).  Edit if you have multiple in flight."

**Capture as:** `WORKSHOP_NUMBER` (integer, 1–99) and `WORKSHOP_NUMBER_PADDED` (string, e.g., `02`)

**Default:** 02 (or the next available after scanning sibling workshop folders if any exist).

---

## Q4 · Day 1 + Day 2 dates

**Ask:**
> "Day 1 + Day 2 dates.  Both are required.  Format: YYYY-MM-DD or natural language like 'June 14 + June 15 2026'."

Parse user input.  If only one date, ask for both.  Convert to ISO 8601.

**Capture as:**
- `DAY_1_DATE_ISO` → `2026-06-14`
- `DAY_2_DATE_ISO` → `2026-06-15`
- `DAY_1_DATE_HUMAN` → `Saturday June 14, 2026` (long form for landing page)
- `DAY_2_DATE_HUMAN` → `Sunday June 15, 2026`
- `DAY_1_DATE_SHORT` → `Sat Jun 14` (compact for emails)
- `DAY_2_DATE_SHORT` → `Sun Jun 15`
- `DAY_1_MONTH_LABEL` → `June 14` (for short-video copy)
- `DAY_2_MONTH_LABEL` → `June 15`
- `WORKSHOP_DATES_RANGE` → `June 14–15, 2026` (for headlines)

**Validation:** dates must parse, Day 2 must be one calendar day after Day 1, both must be future.

**Also derive:**
- `REGISTRATION_OPENS` = Day 1 minus 9 days
- `REGISTRATION_CLOSES` = Day 1 minus 1 day
- `T_MINUS_TIMELINE` = day-by-day map for the email campaign (T-9, T-8, …, T+6)

---

## Q5 · Day 1 + Day 2 topics

**Ask:**
> "Day 1 topic + Day 2 topic.  One sentence each.  These are what attendees walk away with.  (e.g., 'Day 1: Build your prospect engine. Day 2: Build your follow-up engine.')"

Parse the response.  If user gives one combined sentence, ask to split.

**Capture as:**
- `DAY_1_TOPIC` → "Build your prospect engine"
- `DAY_2_TOPIC` → "Build your follow-up engine"
- `DAY_1_DELIVERABLE` → derived shorter form for badges (e.g., "Prospect Machine")
- `DAY_2_DELIVERABLE` → e.g., "Follow-up Machine"

If user can't shorten the deliverables themselves, ask: "What's the 2-word name?  (e.g., Marketing Machine, Sales Machine)"

---

## Q6 · Price + seat count

**Ask:**
> "Workshop price (USD) and seat count?  Defaults are $49 and 40 if you skip."

Parse.

**Capture as:**
- `PRICE` → integer, e.g., `79`
- `PRICE_DISPLAY` → `$79`
- `SEAT_COUNT` → integer, e.g., `60`
- `SEAT_COUNT_DISPLAY` → `60 seats`

**Validation:** price 1–500. Seat count 5–200.

---

## Q7 · Core hook

**Ask:**
> "The core hook.  One sentence.  This goes in the VSL opener and the landing page subheadline.  (e.g., 'Stop chasing leads. Start running a system that researches and writes them for you.')"

**Capture as:** `CORE_HOOK` (string, 60–180 chars)

**Validation:** non-empty, no banned phrases (check against BUSINESS-BRAIN.md voice rules). If banned phrase found, reject and ask for rewrite.

If user provides multiple sentences: keep all of them, but extract the strongest 1-sentence version for places where only one sentence fits.

**Also derive:**
- `HOOK_HEADLINE` · title-case version for the landing page H1
- `HOOK_VSL_OPENER` · the first 3 sentences of the VSL (Claude generates this from the hook + Brain voice)
- `HOOK_TWITTER` · 220-char version for short video scripts

---

## Q8 · Cohort upsell (optional)

**Ask:**
> "Cohort upsell.  Price + start month, or skip if you don't have one.  (e.g., '$3,200, June 2026' or 'skip')"

If user says "skip" or empty: set all cohort fields to empty strings; the email campaign skips the cohort upsell emails (A12, A13).

**Capture as:**
- `COHORT_PRICE` → `$3,200`
- `COHORT_START` → `June 2026`
- `COHORT_TOPIC` → derived from Day 1/Day 2 topics ("90 days of building Prospect + Follow-up Machines together")

---

## Confirmation

Print all 8 answers as a summary table:

```
┌────────────────────────────────────────────────────────────────────┐
│ NEW WORKSHOP · review before generating                            │
├────────────────────────────────────────────────────────────────────┤
│  1. Name        Build Your Sales Machine in 30 Days                │
│  2. Slug        sales-machine-30                                   │
│  3. Number      Workshop 02                                        │
│  4. Dates       June 14–15, 2026 (Sat + Sun)                       │
│  5. Topics      D1: Build your prospect engine                     │
│                 D2: Build your follow-up engine                    │
│  6. Price       $79 · 60 seats                                     │
│  7. Hook        Stop chasing leads. Start running a system…        │
│  8. Cohort      $3,200 · starts June 2026                          │
└────────────────────────────────────────────────────────────────────┘
```

Ask: "Looks right? (yes / edit Q-N to change)"

If user says "edit Q4" → re-ask just that question, update the summary, re-confirm.

When user says "yes" or "go", proceed to Phase 3 (Generate).

---

## Edge Cases

- **User skips multiple questions:** that's fine. Defaults fill in. The VSL and email campaign will be more generic.
- **User wants to use a custom output directory:** ask after Q8: "Output to ~/Desktop/<slug>/ or different path?"
- **User wants the same engines as Workshop 01:** that's the default. If they want to add or remove engines, that's a separate `/build-my-brain` flow · out of scope for this skill.
- **User says "actually, do another"** mid-flow: cancel, restart fresh.
