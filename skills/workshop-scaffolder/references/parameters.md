# Parameter Inventory

Every variable, where it lives in the existing Workshop 01 source, and the substitution rule.

---

## How to use this file

For each parameter:
- **Token** · the variable name from question-flow.md
- **Source files** · files in `purely-personal/` that contain Workshop-01 specific values
- **Find pattern** · the literal string in the source file (use grep)
- **Replace with** · the new value derived from the user's answers

The skill reads the source file, applies all replacements, writes to the new workshop folder.

---

## Workshop-level parameters

### `WORKSHOP_NAME`
**Default Workshop 01 value:** `Build a Business That Runs By Itself`

**Source files + find patterns:**
- `landing-page/index.html` · `<title>...</title>`, `<h1>` headline, OG tags
- `landing-page/install-guide/index.html` · `<title>`, intro h1
- `campaign/email-campaign.md` · header references
- `campaign/vsl-script.md` · full rewrite required (workshop-unique)
- `workshop/Workshop-Agenda.xlsx` · sheet 1 header, sheet 2/3 headers
- `notion-master-doc.md` · title and references
- `README.md` · header

### `WORKSHOP_SLUG`
**Default:** `purely-personal`

**Source files:**
- All paths and folder names in the new project use this
- Used for the new top-level folder name
- GitHub repo URL placeholder

### `WORKSHOP_NUMBER` / `WORKSHOP_NUMBER_PADDED`
**Default Workshop 01 value:** `1` / `01`

**Source files:**
- `landing-page/index.html` · `Workshop 01` mentions
- `landing-page/install-guide/index.html` · none currently (good)
- `campaign/email-campaign.md` · "Workshop 01 · MASTER DOCUMENT" header, "Workshop 02" in B7 fallback
- `notion-master-doc.md` · page title "Workshop 01 · MASTER DOCUMENT"
- `campaign/vsl-script.md` · none directly

---

## Date parameters

### `DAY_1_DATE_ISO` / `DAY_2_DATE_ISO`
**Default Workshop 01:** `2026-05-02` / `2026-05-03`

### `DAY_1_DATE_HUMAN` / `DAY_2_DATE_HUMAN`
**Default Workshop 01:** `Saturday May 2, 2026` / `Sunday May 3, 2026`

### `DAY_1_DATE_SHORT` / `DAY_2_DATE_SHORT`
**Default Workshop 01:** `Sat May 2` / `Sun May 3`

### `WORKSHOP_DATES_RANGE`
**Default Workshop 01:** `May 2–3, 2026`

**Source files containing date references:**
- `landing-page/index.html` · line ~310 "Live · May 2–3, 2026", lines ~470 "Saturday May 2", ~480 "Sunday May 3"
- `landing-page/install-guide/index.html` · line ~XXXX "May 2–3, 2026" in footer
- `campaign/email-campaign.md` · every email mentions May 2 or May 3
- `campaign/vsl-script.md` · "May 2nd and 3rd"
- `workshop/Workshop-Agenda.xlsx` · sheet 2 header "Saturday May 2, 2026", sheet 3 header "Sunday May 3, 2026"
- `notion-master-doc.md` · multiple

### `REGISTRATION_OPENS` / `REGISTRATION_CLOSES`
**Default Workshop 01:** `April 23, 2026` / `May 1, 2026`

**Derived from Day 1 - 9 days / Day 1 - 1 day.** Used in landing page urgency, emails A1, A6, A14.

### `WORKSHOP_TIME` / `WORKSHOP_TIMEZONE`
**Default Workshop 01:** `11:00am` / `Finland (EET)`

If user wants to change time/timezone, ask in Q4 follow-up.

---

## Pricing parameters

### `PRICE`
**Default Workshop 01:** `49`

**Source files:**
- `landing-page/index.html` · every `$49`
- `landing-page/install-guide/index.html` · none directly (correct, install is free)
- `campaign/email-campaign.md` · `$49` in every workshop CTA
- `campaign/vsl-script.md` · "49 dollars" / "$49"
- `notion-master-doc.md` · financial model section

### `SEAT_COUNT`
**Default Workshop 01:** `40`

**Source files:**
- `landing-page/index.html` · `40 seats remaining`
- `campaign/email-campaign.md` · `25 seats` (note: copy mentions 25 in some emails · flag for user to align)
- `campaign/vsl-script.md` · `40 seats`

### `COHORT_PRICE` / `COHORT_START`
**Default Workshop 01:** `$2,400` / `June 2026`

**Source files:**
- `campaign/email-campaign.md` · emails A12, A13
- `notion-master-doc.md` · financial model
- `campaign/vsl-script.md` · none directly

If user skipped cohort: set both to empty string. Skill should detect and:
- Skip emails A12, A13
- Remove cohort references from VSL outro
- Remove cohort waitlist CTA from landing page

---

## Topic parameters

### `DAY_1_TOPIC` / `DAY_2_TOPIC`
**Default Workshop 01:** `Marketing Machine · content in your voice every week, automated` / `Sales Machine · prospect research + outreach in your voice, automated`

**Source files:**
- `landing-page/index.html` · "Day 1 · Automate Your Marketing", "Day 2 · Automate Your Sales"
- `landing-page/install-guide/index.html` · none (install is workshop-agnostic)
- `campaign/email-campaign.md` · every reference to "Day 1: your Marketing Machine. Day 2: your Sales Machine."
- `workshop/Workshop-Agenda.xlsx` · sheet 2/3 outcome rows
- `campaign/vsl-script.md` · full rewrite (workshop-unique)

### `DAY_1_DELIVERABLE` / `DAY_2_DELIVERABLE`
**Default Workshop 01:** `Marketing Machine` / `Sales Machine`

**Used in:**
- Landing page badges, install guide outro, every email CTA, VSL hook, video voiceover.

---

## Voice parameters (from BUSINESS-BRAIN.md)

These come from the user's Brain, not from question flow. Read them once at Step 1 and hold throughout.

### `HOST_NAME`
**Default Workshop 01:** `Daniel Paul`

**Source:** Operator section of BUSINESS-BRAIN.md

### `HOST_HANDLE`
**Default Workshop 01:** `@danielpaulai`

### `HOST_EMAIL`
**Default Workshop 01:** `danny@danielpaul.ai`

### `HOST_LINKEDIN`
**Default Workshop 01:** `linkedin.com/in/danielpaulai`

### `BRAND_NAME`
**Default Workshop 01:** `Purely Personal`

### `BRAND_RED` / `BRAND_DARK` / `BRAND_CREAM`
**Default Workshop 01:** `#e90d41` / `#0f0f10` / `#faf8f4`

### `BRAND_FONTS`
**Default Workshop 01:** `Rethink Sans` (display) / `Inter` (body) / `JetBrains Mono` (code)

These come from the Brain's Brand section. If absent, use Workshop 01 defaults.

---

## CTA parameters

### `CTA_PAYMENT_URL`
**Default Workshop 01:** `https://purelypersonal.ai/checkout` (placeholder, swapped at deploy time)

**Source files:**
- `landing-page/index.html` · every `href="..."` on CTA buttons
- `landing-page/install-guide/index.html` · top-right CTA button

The skill leaves this as a placeholder `[CTA_PAYMENT_URL]` in the new workshop. User swaps after GHL funnel built.

### `LANDING_PAGE_URL`
**Default Workshop 01:** `purely-personal-workshop.vercel.app`

Used in DM outreach, emails, social copy.

### `GITHUB_REPO_URL`
**Default Workshop 01:** `github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself`

Used in install guide for clone command. New workshop will need a NEW GitHub repo. Skill emits this as `[NEW_REPO_URL]` placeholder.

---

## Slash command list (if engines change)

### `ENGINES_LIST`
**Default Workshop 01:** `[/build-my-brain, /marketing-engine, /sales-engine, /operations-engine, /cash-engine, /leadership-engine, /prep-workshop-slides, /ship-it-live]`

**Source files:**
- `landing-page/install-guide/index.html` · slash menu reveal block (8 items)
- `videos/phase-1.mp4` · voiceover lists all 8 commands

For Workshop 02+: if user adds/removes engines, this list changes. Ask in a separate prompt: "Same 8 slash commands or different?" If different, capture the new list.

If list changes, the install guide step 6 (verify 8 commands) and Phase 1 video voiceover both need to be regenerated with the new list.

---

## Workshop-unique copy (no token, must regenerate)

These have no source file substitution · Claude rewrites them from scratch using the user's hook + Brain voice:

| Asset | Rewrite scope | Approx length |
|-------|--------------|---------------|
| **VSL script** | Full rewrite from scratch | 345 words / 2:13 runtime |
| **Email subject lines** | 14 + 7 = 21 subjects rewritten | 8–12 words each |
| **Email A1, A2, A3 bodies** | First 3 emails rewritten in voice | 80–120 words each |
| **Other email bodies (A4–A14, B1–B7)** | Mostly token replacement, only hook references rewritten | varies |
| **DM segment openers** | 4 segments × 2 openers = 8 unique openers | 25–40 words each |
| **Phase 1–4 voiceover scripts** | Full rewrite with new engines/topics | ~330 words each |
| **3 short video scripts (Ava-style)** | Full rewrite with workshop hook | ~150 words each |
| **Notion master doc executive summary** | Rewrite with new dates/price | ~80 words |
| **README.md (in new workshop folder)** | Generated fresh | 20–40 lines |

For each, follow the structure of the Workshop 01 version (headers, sections, length, beats), but rewrite the prose using the user's CORE_HOOK and BUSINESS-BRAIN.md voice. Apply [voice-rules.md] strictly.

---

## Substitution algorithm (per file)

```python
def substitute(source_path, output_path, params):
    text = read(source_path)
    for token, value in params.items():
        # Find all instances of the Workshop 01 default value
        # Replace with the new value
        old = WORKSHOP_01_DEFAULTS[token]
        text = text.replace(old, value)
    write(output_path, text)
```

Applied to every file in [file-map.md] except those marked "Generated fresh" (VSL, DMs, voiceover, etc.) · those are handled by Claude's prose generation in the user's voice.

---

## What NOT to substitute

Some Workshop 01 references should stay because they're examples or proof:

- The `BUSINESS-BRAIN.rendered.html` example (it's a demo, not workshop content)
- The 5 worksheets in `workshop/worksheets/` (they're plugin content, not workshop content)
- Plugin source code (`skills/`, `commands/`) · these are reusable across workshops
- Logo, brand assets · same brand
- The Apify MCP config example (technically same content, just demo)

The skill must NOT recurse into these directories. Only substitute in:
- `landing-page/`
- `campaign/`
- `workshop/Workshop-Agenda.xlsx`
- `notion-master-doc.md`
