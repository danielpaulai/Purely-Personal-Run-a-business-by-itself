# File Map

For each output file in the new workshop, this map says:
- The source file in `purely-personal/`
- Whether it's "hard" (token-replace) or "soft" (Claude rewrites)
- Notes for any tricky substitutions

---

## Hard substitution (mechanical token replace)

These are read from source, tokens replaced, written to output.

| Output | Source | Notes |
|--------|--------|-------|
| `landing-page/index.html` | `purely-personal/landing-page/index.html` | Replace `WORKSHOP_NAME`, `DAY_1_DATE_HUMAN`, `DAY_2_DATE_HUMAN`, `WORKSHOP_DATES_RANGE`, `PRICE`, `SEAT_COUNT`, `DAY_1_DELIVERABLE`, `DAY_2_DELIVERABLE`, `CTA_PAYMENT_URL`, `LANDING_PAGE_URL`. The post-card body is workshop-specific · replace with new VSL hook (first 100 words). |
| `landing-page/install-guide/index.html` | `purely-personal/landing-page/install-guide/index.html` | Replace `WORKSHOP_NAME` in title + intro h1. Replace `WORKSHOP_DATES_RANGE` in footer. Replace `GITHUB_REPO_URL` in clone command. The 8 slash commands list stays the same (engines don't change unless user explicitly says so in a follow-up). |
| `landing-page/install-guide/CAPTURE-CHECKLIST.md` | `purely-personal/landing-page/install-guide/CAPTURE-CHECKLIST.md` | Copy verbatim. Workshop-agnostic. |
| `integrations/vercel-to-ghl.md` | `purely-personal/integrations/vercel-to-ghl.md` | Copy verbatim. Workshop-agnostic. |
| `integrations/ghl-build-spec.md` | `purely-personal/integrations/ghl-build-spec.md` | Replace `WORKSHOP_NUMBER`, `WORKSHOP_NAME`, `DAY_1_DATE_HUMAN`, `DAY_2_DATE_HUMAN`, `PRICE`, `SEAT_COUNT`. The funnel name = `Workshop <NUM> · <DATES>`. |
| `workshop/worksheets/*` | `purely-personal/workshop/worksheets/*` | Copy verbatim. The 5 fillable HTML worksheets are plugin content, not workshop content. |
| `.gitignore` | `purely-personal/.gitignore` | Copy verbatim. |

---

## Hybrid (token-replace + soft rewrite of certain sections)

These have token-replaceable headers/dates/CTAs PLUS workshop-unique prose that needs rewriting.

| Output | Source | What gets rewritten |
|--------|--------|---------------------|
| `campaign/email-campaign.md` | `purely-personal/campaign/email-campaign.md` | Subject lines (all 21). Email A1 body (the 9-Word Email). Email A2 body (Event Promo Response). Email A3 body (Client Win · must reference workshop's domain, not Workshop 01's). Email A4–A14 bodies: token-replace dates/prices, lightly edit hook references. Email B1–B7: token-replace + edit lead-magnet references if they changed. **Skip A12 + A13 if user said "skip cohort" on Q8.** |
| `campaign/dm-outreach.md` | `purely-personal/campaign/dm-outreach.md` | Each segment's 2 openers (8 total). Reply flow templates token-replaced. |
| `notion-master-doc.md` | `purely-personal/campaign/notion-master-doc.md` (if it exists; otherwise generate fresh) | Workshop name, dates, price, financial model, refreshed timeline (T-9 to T+6 dates derived from Day 1), team table (same people), folder structure. The "What This Actually Is" section needs a workshop-specific paragraph. |

---

## Full rewrite (Claude regenerates from scratch)

These are workshop-unique. The structure stays the same as Workshop 01, but the prose is generated fresh in the user's voice using their CORE_HOOK from Q7.

| Output | Reference structure | Length target |
|--------|---------------------|---------------|
| `campaign/vsl-script.md` | Same 7-beat structure as Workshop 01 (problem → reframe → install moment → 5 engines → cost → offer → CTA) | 345 words / 2:13 runtime at 150 wpm |
| `campaign/video-scripts.md` | 3 short Ava-style scripts (60–65s each). Same structure: hook → tension → reframe → CTA | ~150 words each |
| `videos/pp-install-phase-1/assets/narration-script.txt` | Same install steps as Phase 1 (CLI, GitHub, Git, clone, plugin, verify) | ~330 words / 1:45 |
| `videos/pp-install-phase-2/assets/narration-script.txt` | Same connector steps (Gmail, Notion, Calendar, Drive, Stripe) | ~290 words / 1:30 |
| `videos/pp-install-phase-3/assets/narration-script.txt` | Same Apify MCP flow (token, config, verify) | ~340 words / 2:00 |
| `videos/pp-install-phase-4/assets/narration-script.txt` | Same final prep (LinkedIn URL, business folder, BUSINESS-BRAIN.md) | ~280 words / 1:30 |
| `README.md` (new workshop folder) | New file, 5-section structure: What this is, Folder layout, Next steps (5 things to customize), Render commands, Deploy commands | 30–60 lines |

---

## Regenerate (programmatic, not text)

These need code execution, not text replacement.

| Output | Method | Notes |
|--------|--------|-------|
| `workshop/Workshop-Agenda.xlsx` | Python + openpyxl | Read source xlsx structure, regenerate with new Day 1/Day 2 topics, deliverables, and dates. Pre-Session Setup sheet stays the same. |
| `videos/pp-install-phase-N/index.html` | Read template + token replace + new SUBTITLES inline | Composition ID = `<slug>-phase-N`. New voiceover script means new transcript means new subtitles. The skill needs to: (1) read the rewritten narration script, (2) generate audio via `npx hyperframes tts`, (3) transcribe via `npx hyperframes transcribe`, (4) run gen-subtitles.py, (5) embed new subtitles array in the composition HTML. This is a multi-step operation · see [video-pipeline.md] for details. |
| `videos/pp-install-phase-N/assets/narration.wav` | Generated by hyperframes tts | After Claude writes the narration-script.txt |
| `videos/pp-install-phase-N/transcript.json` | Generated by hyperframes transcribe | After narration.wav exists |
| `videos/pp-install-phase-N/subtitles.json` | Generated by gen-subtitles.py | After transcript.json exists |

For the video pipeline, the skill outputs the COMPOSITION HTML + SCRIPT TEXT only. Actually rendering audio + video is a separate command the user runs (`cd videos/pp-install-phase-1 && npx hyperframes tts assets/narration-script.txt --voice am_adam --speed 0.88 --output assets/narration.wav`). The skill emits a `videos/RENDER.sh` script that does all 4 phases sequentially.

---

## Special cases

### If user said "skip cohort" on Q8

- Skip emails A12 and A13 entirely
- Remove cohort upsell paragraph from VSL (the "$2,400 in June" line)
- Remove cohort waitlist CTA from landing page (or replace with "Workshop 02 waitlist" CTA)
- Remove cohort row from financial model in Notion master doc

### If user provided a new GitHub repo URL in a follow-up

- Replace the clone command in install-guide
- Replace the GitHub repo link in landing page footer
- Update the README to reference the new repo

### If user changed the ENGINES_LIST

- Update install-guide step 6 (the slash command verification)
- Update Phase 1 voiceover script (the part that lists 8 commands)
- Update the install-guide success-mockup card (which references `/marketing-engine` etc.)
- Update the Notion master doc's "What This Is" section
