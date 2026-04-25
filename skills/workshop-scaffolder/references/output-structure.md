# Output Structure

The folder layout the new workshop should produce. Mirrors Workshop 01's structure with workshop-specific paths.

---

## Default output location

`~/Desktop/<workshop-slug>/`

Example: `~/Desktop/sales-machine-30/`

The skill asks the user at Step 3 if this default works or if they want a different path. If they say a different path, validate it doesn't already exist (or ask to overwrite).

---

## Folder layout

```
<workshop-slug>/
├── README.md                                ← The 5 things to customize (NEW · generated)
├── BUSINESS-BRAIN.md                        ← Symlinked or copied from existing repo
├── landing-page/
│   ├── index.html                           ← Token-replaced from purely-personal/
│   ├── install-guide/
│   │   ├── index.html                       ← Token-replaced
│   │   ├── CAPTURE-CHECKLIST.md             ← Copied as-is (workshop-agnostic)
│   │   ├── screenshots/                     ← Empty folder (placeholder)
│   │   └── videos/                          ← Empty folder (videos to render)
│   └── .vercel/                             ← Empty (user runs `vercel link` after)
├── campaign/
│   ├── email-campaign.md                    ← Token-replaced + soft prose regenerated
│   ├── vsl-script.md                        ← FULL REWRITE in user's voice
│   ├── dm-outreach.md                       ← Token-replaced + soft prose regenerated
│   ├── video-scripts.md                     ← FULL REWRITE (3 Ava-style)
│   └── voice-research.md                    ← Optional, copied as-is
├── integrations/
│   ├── ghl-build-spec.md                    ← Token-replaced (workshop name, dates, price)
│   └── vercel-to-ghl.md                     ← Copied as-is (workshop-agnostic)
├── workshop/
│   ├── Workshop-Agenda.xlsx                 ← Regenerated with openpyxl + new topics
│   ├── worksheets/                          ← Copied as-is (5 fillable HTML)
│   └── install-guide/                       ← (legacy, not used)
├── videos/                                  ← Hyperframes compositions (4 phases)
│   ├── pp-install-phase-1/
│   │   ├── index.html                       ← Composition + new voiceover script
│   │   ├── meta.json                        ← Composition ID = <slug>-phase-1
│   │   ├── hyperframes.json
│   │   └── assets/
│   │       └── narration-script.txt         ← Generated in user's voice
│   ├── pp-install-phase-2/                  ← Same structure
│   ├── pp-install-phase-3/                  ← Same structure
│   └── pp-install-phase-4/                  ← Same structure
├── notion-master-doc.md                     ← Generated fresh, ready to paste into Notion
└── .gitignore                               ← Copied as-is
```

---

## What each output is for

### `README.md`
The first thing the user sees after generation. Lists the 5 things to customize before launching:
1. Add NEW GitHub repo URL to the install guide clone command
2. Swap landing page CTA placeholders for the GHL funnel URL once built
3. Review + edit the VSL script (it's a draft in your voice, but you'll iterate)
4. Run the email campaign through GHL
5. Render the 4 phase walkthrough videos (one command per phase, see videos/README.md)

### `landing-page/index.html`
Drop-in replacement for Workshop 01's landing page. New title, dates, price, hook, post-card content. CTAs point to placeholder URLs the user swaps post-deploy.

### `landing-page/install-guide/index.html`
Same install steps, customized references. The 8 slash commands list pulls from `ENGINES_LIST`. The success-mockup card examples mention the new workshop's deliverables.

### `landing-page/install-guide/videos/`
Empty folder. User renders the 4 videos in `videos/pp-install-phase-N/` and copies the resulting MP4s here.

### `campaign/email-campaign.md`
21 emails total. Subject lines all rewritten in voice. Bodies token-replaced + first 3 emails rewritten substantively (those are the most workshop-specific). Cohort upsell emails (A12, A13) skipped if user said "skip" on Q8.

### `campaign/vsl-script.md`
Full rewrite. The hook (Q7) drives the opener. Same 2:13 runtime, same beat structure (problem → reframe → install moment → 5 engines → cost → offer → CTA), but the prose is workshop-specific.

### `campaign/dm-outreach.md`
Same 4 segments. Each segment's openers (2 per) rewritten in voice with the new workshop hook. Reply flows token-replaced.

### `campaign/video-scripts.md`
3 short-form scripts (60–65s each, Ava-style). Workshop-unique. Same structure: hook → tension → reframe → CTA.

### `workshop/Workshop-Agenda.xlsx`
4-sheet xlsx regenerated with openpyxl. Sheets:
1. Pre-Session Setup · copied verbatim (install steps are universal)
2. Day 1 · TOPIC-specific (e.g., "Day 1 · Prospect Machine" with prospect-engine demo blocks)
3. Day 2 · TOPIC-specific
4. Autopilot Overview · 6 routines, names changed to match new engines

### `videos/pp-install-phase-N/`
4 hyperframes composition projects, one per phase. Each contains:
- `index.html` · composition with same animation structure, new voiceover script, new subtitle data
- `meta.json` · composition ID = `<slug>-phase-N`
- `assets/narration-script.txt` · voiceover text in user's voice

User runs `npx hyperframes render --quality draft --output renders/phase-N.mp4` from each folder. The 4 MP4s drop into `landing-page/install-guide/videos/`.

### `notion-master-doc.md`
Workshop 01's master doc structure with all values replaced. User pastes this into a new Notion page · it renders as the new workshop's master doc with proper headings, tables, callouts.

### `integrations/ghl-build-spec.md`
GHL specialist gets this. Funnel name, price, email schedule all updated for the new workshop.

---

## What does NOT get copied

- `purely-personal/` plugin folder · the new workshop uses the same plugin (cross-workshop). Symlink or reference, don't copy.
- `examples/` · those are demo artifacts, not workshop content.
- `skills/` · plugin internals.
- `commands/` · plugin internals.
- `.git/` · new workshop is a new repo or a new branch.
- `node_modules/` · plugin doesn't have one.

---

## Post-generation checklist (printed to user)

```
✓ <workshop-slug>/ generated at <output-path>

Next 5 things to do:
  1. cd <output-path> && open landing-page/index.html        ← review the landing page
  2. open campaign/vsl-script.md                              ← review the VSL draft
  3. Create new GitHub repo + edit install-guide clone URL   ← see README.md
  4. cd videos/pp-install-phase-1 && npx hyperframes render   ← render Phase 1 video
  5. Set up GHL funnel + paste CTA URL into landing page     ← see integrations/ghl-build-spec.md

Total estimated time to launch: 4–6 hours of editing + 1 hour of video rendering.
```
