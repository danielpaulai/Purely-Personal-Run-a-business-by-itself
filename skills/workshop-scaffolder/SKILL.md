---
name: workshop-scaffolder
description: Generate the complete launch package for a brand-new workshop. Triggers on "new workshop", "spin up another workshop", "next workshop launch", "scaffold workshop", "workshop number 2", "second workshop", "duplicate workshop", "another live workshop", or any request to create a fresh workshop project from the existing Purely Personal Workshop 01 as a template. Reads BUSINESS-BRAIN.md for voice + brand. Outputs a self-contained folder with branded landing page, install guide, 21-email campaign, DM outreach, VSL script, agenda xlsx, Notion master doc, and 4 phase-walkthrough video compositions. Used by the `/new-workshop` slash command.
---

# Workshop Scaffolder

Take an existing workshop launch package (the one you already built) and produce a copy customized for a new workshop. Reuses the styles, structure, and machinery; replaces the workshop-specific content (name, dates, price, hook, topics, audience).

## How This Skill Works

This skill does NOT regenerate everything from scratch. It picks values from a parameter inventory, reads source files from Workshop 01, applies substitutions, and writes a new self-contained workshop directory.

1. Read `BUSINESS-BRAIN.md` (project root or path provided) for voice + brand
2. Ask the 8 questions in [references/question-flow.md]
3. Read the parameter map in [references/parameters.md] · knows where every token lives
4. For each output file:
   - Read the source from `purely-personal/` (the existing Workshop 01 repo)
   - Apply token substitutions
   - For unique copy (VSL hook, DM openers, voiceover scripts), generate in the user's voice using the Brain
5. Write the new workshop to `<output-dir>/<workshop-slug>/`
6. Run the validation checklist
7. Print the quickstart for the user

**ALWAYS read [references/parameters.md] BEFORE generating any output.** It's the load-bearing map of which tokens live in which files.

## Reference Files

| File | What It Contains | When to Read |
|------|-----------------|--------------|
| [references/question-flow.md] | The 8 questions with defaults, validation, examples | ALWAYS · first step |
| [references/parameters.md] | Every token, every file it lives in, default values | ALWAYS · second step |
| [references/output-structure.md] | The folder layout the new workshop should produce | ALWAYS · before writing files |
| [references/voice-rules.md] | Banned phrases, voice patterns, the AI-tells filter | When generating any copy (VSL, DMs, voiceover) |
| [references/quickstart.md] | The handoff message to print at the end | ALWAYS · last step |
| [references/file-map.md] | Source-file → output-file map for every asset | When writing each file |

## The 8 Inputs

In order:

1. **Workshop name** · full title, used in headlines (e.g., "Build Your Sales Machine in 30 Days")
2. **Workshop slug** · kebab-case, used in URLs and folder names (e.g., `sales-machine-30`)
3. **Workshop number** · integer (defaults to next available, e.g., 02)
4. **Day 1 date + Day 2 date** · ISO 8601 (e.g., `2026-06-14` + `2026-06-15`)
5. **Day 1 topic + Day 2 topic** · one sentence each (e.g., "Build your prospect engine" / "Build your follow-up engine")
6. **Price + seat count** · USD integer + integer (e.g., `79` + `60`)
7. **Core hook** · one sentence (the VSL one-liner)
8. **Cohort upsell** · price + start month (e.g., `$3,200, June 2026`) or "skip"

## The 9 Outputs

For every new workshop, this skill produces:

| Output | Source it copies from | What changes |
|--------|----------------------|--------------|
| `landing-page/index.html` | `purely-personal/landing-page/index.html` | Title, dates, price, hook, post-card content, CTA links |
| `landing-page/install-guide/index.html` | `purely-personal/landing-page/install-guide/index.html` | Workshop name, slash command list (if engines change), step copy |
| `landing-page/install-guide/videos/` | (regenerate via hyperframes) | New voiceover scripts in user's voice |
| `campaign/email-campaign.md` | `purely-personal/campaign/email-campaign.md` | Subjects, dates, prices, CTAs, hook references |
| `campaign/vsl-script.md` | `purely-personal/campaign/vsl-script.md` | Full rewrite · VSL is workshop-unique |
| `campaign/dm-outreach.md` | `purely-personal/campaign/dm-outreach.md` | Segment openers customized to new audience |
| `campaign/video-scripts.md` | `purely-personal/campaign/video-scripts.md` | 3 short Ava-style scripts for the new workshop |
| `workshop/Workshop-Agenda.xlsx` | `purely-personal/workshop/Workshop-Agenda.xlsx` | Day 1/Day 2 topic columns + outcomes (regenerate with openpyxl) |
| `notion-master-doc.md` | `purely-personal/campaign/notion-master-doc.md` (or generate fresh) | All workshop-specific values, ready to paste into Notion |
| `README.md` | (generate fresh) | The quickstart + 5 things to customize |

## Workflow

### Step 1: Load the Brain
Read `BUSINESS-BRAIN.md`. Extract:
- Voice section → tone, hook patterns, banned phrases (5+ phrases minimum)
- Operator → host name, email, LinkedIn URL
- Brand → primary color, fonts, logo if present
- ICP → audience description for DM targeting

If Brain is missing: STOP. Tell user to run `/build-my-brain` first. Do not proceed.

### Step 2: Ask 8 Questions
Follow [references/question-flow.md]. Print all answers back as a summary before generating. Let user edit.

### Step 3: Confirm Output Location
Default: `~/Desktop/<workshop-slug>/`. Ask user to confirm or provide a different path. Create the folder.

### Step 4: Generate Hard Templates
For each file in [references/file-map.md]:
1. Read source from existing Workshop 01 repo (use absolute paths)
2. Apply substitutions per [references/parameters.md]
3. Write to new workshop folder

These are the deterministic ones · landing page HTML, install guide HTML, agenda xlsx, etc. Just token replacement.

### Step 5: Generate Soft Copy
For workshop-unique copy:
- **VSL script** · full rewrite using user's hook + Brain voice. Target 2:13 runtime, 345 words.
- **DM segment openers** · 4 segments × 2 openers each, customized to new audience.
- **Phase walkthrough voiceover scripts** · 4 scripts, one per phase. Same install steps but worded for new workshop context.
- **Email subject lines** · 14 subjects in user's voice for Category A, 7 for Category B.
- **3 short video scripts** · Ava-style, hook based on workshop's core promise.

For each, read [references/voice-rules.md] and apply.

### Step 6: Validate
Run the validation checklist:
- [ ] Zero em-dashes anywhere in generated output (use periods or middle-dot)
- [ ] Zero banned phrases from BUSINESS-BRAIN.md voice rules
- [ ] All 8 inputs appear correctly in landing page H1, dates, price, CTAs
- [ ] All file paths in landing page are workshop-relative (e.g., `videos/phase-1.mp4`, not `purely-personal/...`)
- [ ] Email campaign dates align with Day 1/Day 2 (Email A1 sent T-9 days, A14 sent T+6, etc.)
- [ ] VSL runtime estimate: 130–145 seconds at 150 wpm
- [ ] Install guide references the correct slash commands (if user changed engine list)
- [ ] README.md lists the 5 things to customize and the deploy command

If any check fails, fix before handoff.

### Step 7: Print Quickstart
Read [references/quickstart.md]. Substitute the new workshop's values. Print to user.

### Step 8: Optional Open
Ask: "Want me to open the landing page or VSL first?" Use `open <path>` if yes.

## Voice Discipline

The new workshop must sound like the SAME PERSON as Workshop 01. Same:
- Sentence length (short)
- Specifics (numbers, names, amounts)
- Hook patterns (from Brain)
- No em-dashes, no banned phrases
- No fake testimonials or invented metrics

The differences are:
- Workshop name + topic
- Dates + price + seat count
- The hook (one sentence promise)
- Day 1 + Day 2 deliverables
- Audience-specific DM segment openers

Everything else stays in the same voice.

## Anti-Patterns

Do NOT:
- Hardcode values from Workshop 01 (e.g., "May 2–3", "$49", "5 jobs") into the new output
- Generate testimonials or numbers the user didn't provide
- Skip the BUSINESS-BRAIN.md read because "we already know the voice"
- Output without running the validation checklist
- Write files to the existing `purely-personal/` repo · always to a new directory

## Quick Triggers

| User Says | Action |
|-----------|--------|
| `/new-workshop` (no args) | Run full 8-question flow |
| `/new-workshop "Title"` | Use title as Q1, ask Q2-Q8 |
| `new workshop scaffold` | Same as `/new-workshop` |
| `duplicate this workshop for a new launch` | Same as `/new-workshop` |
| `make Workshop 02` | Same, default Q3 to current next number |
