---
description: Generate personalized opening slides for every workshop attendee. Scrapes each LinkedIn URL, extracts voice signatures, renders a dark-themed slide with their name, signature hook, favorite word, AI-slop score, and one mind-blowing observation. Output cycles as a slideshow at the start of Day 1.
argument-hint: <csv-path> OR paste-linkedin-urls-one-per-line
---

# /prep-workshop-slides

You are the Workshop Producer. Your job: turn a list of LinkedIn URLs into a personalized opening slideshow that makes every attendee feel seen in the first 10 seconds of Day 1.

**This is the single highest-impact workshop asset.** Do not skip it. Do not fabricate data. If a scrape fails, flag it so the facilitator knows before Day 1.

---

## Input

One of:
1. **CSV path:** `./workshop/attendees.csv` with columns: `name`, `linkedin_url`, `email`
2. **Inline paste:** user pastes LinkedIn URLs one per line, ≥2 and ≤50

If no input: ask user to paste URLs.

---

## Step 1 — Scrape + Analyze Each Attendee

For each LinkedIn URL, run in parallel:

1. `apify-linkedin` → pull profile headline, headshot URL, last 30 posts
2. `voice-extractor` on the posts → tone, hook pattern, banned phrases, example openings

From the raw output, derive these 5 data points per attendee:

### Attendee data schema

| Field | Source | Example |
|-------|--------|---------|
| `name` | profile → name | "Daniel Paul" |
| `initials` | first letter + last letter of name | "DP" |
| `headshot_url` | profile → photo URL | ... |
| `verdict_bold` | 3 adjectives describing their tone | "Direct. Conversational. Allergic to corporate." |
| `verdict_rest` | 1 complementary sentence | "You write like you talk. The AI already knows." |
| `data.posts.value` | count of posts analyzed | 30 |
| `data.hook.value` | their signature hook pattern | "Personal<br>Proof" |
| `data.hook.sub` | their most-used hook opener | "\"I built X. It cost me zero dollars.\"" |
| `data.word.value` | most frequent non-stopword, with count | "\"system\"" |
| `data.word.sub` | "Used N times · non-stopword" | "Used 27 times · non-stopword" |
| `data.slop.value` | AI-slop score 1–10 | 7 |
| `data.slop.sub` | explanation | "Em-dashes in 19 of 30 posts" |
| `data.slop.warn` | true if score ≥ 6 | true |
| `observation.bold` | the mind-blown stat | "34% of your sentences" |
| `observation.text` | the insight that makes it personal | "start with 'And' or 'But.' That's not an accident. That's your voice." |

**Rule:** every observation must be *specific, countable, and slightly invasive* — think psychic reading, not horoscope. Generic ("you like stories") is banned. Specific ("every 4th post opens with a number") is the bar.

### Picking the Observation — the load-bearing detail

The "observation" field is what makes this work. Pull from:
- Opening word distribution ("34% of sentences start with 'And'")
- Average sentence length ("Your posts average 11 words per sentence. Danko's law territory.")
- Post cadence ("You post 4x per month. Consistency of anyone in this workshop.")
- Word frequency surprises ("You've used 'actually' 41 times in 30 posts. You know something others don't want to hear.")
- Structural quirks ("Every post ends with a P.S. question. You're not coincidentally viral — you're deliberately viral.")

If you can't find something specific, scrape more posts (up to 90 day lookback). Never ship a generic observation.

---

## Step 2 — Write to attendees.json

Save to `workshop/attendee-slides/attendees.json`:

```json
{
  "workshop": "01",
  "date": "Apr 2026",
  "attendees": [
    {
      "name": "...",
      "initials": "...",
      "headshot_url": "...",
      "verdict_bold": "...",
      "verdict_rest": "...",
      "data": { "posts": {...}, "hook": {...}, "word": {...}, "slop": {...} },
      "observation": { "bold": "...", "text": "..." }
    },
    ...
  ]
}
```

Schema matches the `attendees.sample.json` already in the folder — same shape.

---

## Step 3 — Wire Into the Slideshow

`workshop/attendee-slides/index.html` already reads attendee data inline. Update the `const ATTENDEES = [...]` array in that file to load from the JSON:

```javascript
// Replace the inline ATTENDEES array with:
const ATTENDEES = await fetch('./attendees.json').then(r => r.json()).then(d => d.attendees);
```

Alternatively, for simpler hosting (no CORS issues with `file://`), regenerate the inline array in `index.html` from the JSON. Use the `embed_attendees.py` helper script (write it if missing).

---

## Step 4 — Generate Standalone Previews (optional)

For attendees who want to screenshot their slide individually, also generate a standalone HTML per attendee:

`workshop/attendee-slides/{slug}.html` — one per attendee, same layout as `daniel-paul.html`.

Slug format: lowercase name, hyphens, no special chars. "Daniel Paul" → `daniel-paul`.

---

## Step 5 — Report

After generation, tell the user:

```
✓ Processed {N} attendees

  Ready:     {N_ok} attendees (slides + observations generated)
  Flagged:   {N_flagged} attendees (scrape failed — needs manual fix)
  Skipped:   {N_skipped} attendees (insufficient LinkedIn activity)

Output:
  workshop/attendee-slides/index.html       (cycling slideshow)
  workshop/attendee-slides/attendees.json   (data file)
  workshop/attendee-slides/{N}.html         (per-attendee standalones)

Preview:
  open workshop/attendee-slides/index.html

Flagged attendees needing manual data:
  - {name} ({url}): {reason}
  - ...
```

---

## Step 6 — Pre-Workshop Rehearsal

Before Day 1, do this:

1. Open `index.html`
2. Play through all slides
3. Read each observation aloud — does it feel *specific* enough to make the attendee go "oh shit, they know me"?
4. Flag any slide where the observation feels generic. Regenerate that attendee's data with different prompts.

**Quality bar:** if you'd be embarrassed to show a slide to the named attendee, don't ship it.

---

## Anti-patterns

- ❌ Never fabricate observations when a scrape fails. Use the fallback state: "Welcome, {name}. Your Brain is about to get built." — honest, no fake data.
- ❌ Never generate generic observations ("you're creative and thoughtful"). The whole point is specificity.
- ❌ Never include banned phrases in the generated copy itself. If the attendee uses "unlock" 40 times, the observation might be "you use 'unlock' 40 times" — but your own prose must never use it.
- ❌ Never show another attendee's private data (email, exact post content) on-slide. Abstracted stats only.
- ❌ Never skip the headshot fallback. Use the initials-circle SVG if no photo is available.
- ❌ Never exceed 1 observation per slide. One is specific. Two is noise.

---

## Chaining

**Upstream:**
- `apify-linkedin` — the scraper
- `voice-extractor` — extracts tone + hook patterns

**Downstream:**
- Slideshow controller in `workshop/attendee-slides/index.html`
- Workshop opening moment (`workshop/mind-blown-activities.md` → Activity #1)

---

## Facilitator Tip

Run this command **24 hours before Day 1**. The scrape takes 5–10 min for 42 attendees. Build in a buffer — you want time to review each slide before attendees see it.

If someone registers same-day, skip their slide or manually add them using the template in `daniel-paul.html`. Don't block the cohort for one late signup.
