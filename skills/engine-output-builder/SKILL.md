---
name: engine-output-builder
description: Render a single Business Brain section as a standalone shareable graphic. Use for screenshot assets, LinkedIn image posts, and social sharing. Triggers on "competitor matrix standalone", "voice card graphic", "ICP card", "brand identity card", "AI visibility card", "pain theme quote", "one section as image", "share this section", "make a graphic of my [section]", "standalone [section]", or any request to render a single section of BUSINESS-BRAIN.md as a self-contained visual asset. Also triggers when someone says "screenshot my voice rules" or "make a shareable [section]".
---

# Engine Output Builder

Render a single Business Brain section as a self-contained HTML artifact optimized for screenshotting and social sharing. Same design language as `business-brain-renderer`, but scoped to one section on a minimal page shell.

## Why This Exists

The full Brain one-pager is 9 sections and scrolls. Sometimes you want just the competitor matrix, or just the voice card, or just the top pain quote — rendered at sharable square / portrait dimensions for LinkedIn, X, or a deck screenshot.

This skill gives you that, without rebuilding templates.

## How This Skill Works

1. Read `BUSINESS-BRAIN.md` (same location logic as `business-brain-renderer`)
2. Identify which section(s) the user wants
3. Load the matching template from `business-brain-renderer/references/code-templates.md`
4. Wrap it in the minimal standalone shell from [references/output-modes.md]
5. Add format-specific sizing (square 1080×1080 / portrait 1080×1350 / landscape 1200×628)
6. Emit the HTML artifact

**Rule:** this skill does NOT redesign sections. It reuses `business-brain-renderer` templates exactly. Any design change belongs upstream, in `business-brain-renderer/references/`.

## Reference Files

| File | What It Contains | When to Read |
|------|-----------------|--------------|
| [references/output-modes.md] | Minimal page shells for square / portrait / landscape / LinkedIn / X / print | ALWAYS before rendering |
| `../business-brain-renderer/references/code-templates.md` | The source-of-truth section templates | ALWAYS to get the section code |
| `../business-brain-renderer/references/design-system.md` | Design tokens — same `:root` CSS custom properties | ALWAYS, included in every shell |
| `../business-brain-renderer/references/svg-primitives.md` | Engine icons, radial meter, placeholder avatar | When a section needs an icon |

## The 8 Standalone Outputs

Each maps to a section of the full Brain, plus 2 composite formats.

| # | Output | Source section | Default dimensions |
|---|--------|---------------|-------------------|
| 1 | **Voice card graphic** | Section 2 | 1080×1350 portrait |
| 2 | **Business card** | Section 3 | 1080×1080 square (the $75K stat pops) |
| 3 | **ICP persona card** | Section 4 | 1080×1350 portrait |
| 4 | **Competitor 3×3** | Section 5 | 1200×628 landscape (for LinkedIn) |
| 5 | **Brand identity card** | Section 6 | 1080×1080 square |
| 6 | **AI visibility scorecard** | Section 7 | 1080×1080 square (meter dominates) |
| 7 | **Pain hero quote** | Section 8 hero | 1080×1080 square (shareable quote graphic) |
| 8 | **Proof stats band** | Section 1.5 | 1200×628 landscape (dark, striking) |

## Workflow

### Step 1: Identify the Target
Parse the user's request. Which section(s)? What platform / dimensions?

If ambiguous, default:
- "screenshot my voice" → Voice card, 1080×1350 portrait
- "share my positioning gaps" → Competitor 3×3, 1200×628 landscape
- "quote graphic" → Pain hero, 1080×1080 square

### Step 2: Load the Brain
Read `BUSINESS-BRAIN.md`. Extract only the target section's data. If section is empty, render the empty state card from `business-brain-renderer/references/content-library.md` instead.

### Step 3: Load the Template
Open `business-brain-renderer/references/code-templates.md` and locate the matching template. Copy EXACTLY — no modifications to the section itself.

### Step 4: Wrap in Output Shell
From [references/output-modes.md], pick the shell matching the requested dimensions. Drop the section template inside.

### Step 5: Tuning for Format
Some sections need minor padding tuning per format:
- Square (1:1): section may need wider inner padding to prevent vertical crunch
- Portrait (4:5): section can use full vertical height, no squeeze
- Landscape (1.91:1): section should be horizontal-friendly (Competitor 3×3 works natively, Voice card needs row-split layout)

See [references/output-modes.md] for format-specific rules.

### Step 6: Validate
Before shipping:
- [ ] Target section data present (no `{{placeholders}}`)
- [ ] Fits within the requested dimensions (no scrollbar)
- [ ] Brand mark present in corner or footer
- [ ] Print CSS active (for PDF export)
- [ ] Dimensions are 1080, 1200, or 628-multiples (LinkedIn/X/IG sizing)

### Step 7: Emit
One HTML file. User screenshots or opens-then-print-to-PDF for a shareable image.

## Quick Triggers

| User Says | Generate |
|-----------|----------|
| "voice card graphic" | Voice (Section 2), 1080×1350 portrait |
| "competitor matrix for LinkedIn" | Competitor 3×3 (Section 5), 1200×628 landscape |
| "ICP card standalone" | ICP (Section 4), 1080×1350 portrait |
| "quote graphic of [pain theme]" | Pain hero (Section 8 hero), 1080×1080 square |
| "$75K stat" | Business (Section 3), 1080×1080 square |
| "AI score card" | AI Visibility (Section 7), 1080×1080 square |
| "proof stats band" | Proof band (Section 1.5), 1200×628 landscape |
| "brand palette card" | Brand Identity (Section 6), 1080×1080 square |

## Format Selection Guide

| Platform | Best format | Why |
|----------|-------------|-----|
| LinkedIn feed post | 1200×628 landscape OR 1080×1350 portrait | Portrait = more feed real estate |
| LinkedIn carousel slide | 1080×1350 portrait | Standard carousel dimension |
| X post image | 1600×900 landscape OR 1080×1080 square | Landscape preferred for threads |
| Instagram feed | 1080×1080 square OR 1080×1350 portrait | Square most universal |
| Newsletter hero | 1200×600 landscape | Fits above-the-fold in most email clients |
| PDF handout | A4 portrait | Print-optimized shell |

## Chaining with Other Skills

- **Upstream:** `business-brain-renderer` is where templates live. This skill is a lightweight wrapper.
- **Upstream:** `content-visual-builder` for multi-platform content posts (different job — this skill is for Brain sections, that skill is for content posts).
- **Downstream:** `scripts/build_pdf.py` can auto-render any engine-output-builder HTML to PDF/PNG.

## Anti-patterns

- ❌ Never redesign a section. If the section needs visual changes, edit `business-brain-renderer/references/code-templates.md` — not here.
- ❌ Never render a section that's empty. Render the empty state instead, with a CTA.
- ❌ Never render at raw pixel dimensions without a frame — always use one of the standard LinkedIn/X/IG/Newsletter shells.
- ❌ Never combine 2+ sections in one output. Use `business-brain-renderer` for multi-section output; this skill is strictly single-section.
- ❌ Never omit the brand corner mark. Every standalone image must be attributable or it's just a random graphic.
