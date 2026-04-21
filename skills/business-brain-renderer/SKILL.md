---
name: business-brain-renderer
description: Render a filled BUSINESS-BRAIN.md into a visually stunning single-page HTML artifact with exportable PDF. Triggers on "render my brain", "business brain artifact", "render business brain", "print my brain", "brain one-pager", "business brain pdf", "business brain card", "visualize my business brain", "brain hero page", "render BUSINESS-BRAIN.md", or any request to turn a Business Brain document into a visual one-pager. Also triggers when someone says "make my brain beautiful", "Purely Personal brain card", or "export my brain". Use for ANY visual rendering of BUSINESS-BRAIN.md content — even casual requests like "show me my brain".
---

# Business Brain Renderer

Turn a filled `BUSINESS-BRAIN.md` into a single-page HTML artifact that looks like it cost a design agency $5k. Every section maps to a pre-built template with `{{VARIABLE}}` placeholders. PDF-exportable, print-ready, screenshot-worthy.

## How This Skill Works

This skill does NOT generate design from scratch. It picks templates from reference files, fills variables from the user's Business Brain, and assembles a deterministic one-pager.

1. Read `BUSINESS-BRAIN.md` (path provided, or look in project root)
2. Parse each section → map to the matching visual type
3. Pick the template from [references/code-templates.md]
4. Fill `{{VARIABLES}}` from the parsed Brain data
5. Inject SVG from [references/svg-primitives.md] where needed
6. Add interactivity (editable fields, PDF export button) from [references/interactive-patterns.md]
7. Validate against the quality checklist
8. Emit one HTML artifact

**ALWAYS read [references/code-templates.md] BEFORE generating.** The templates are load-bearing — deviation produces off-brand output.

## Reference Files

| File | What It Contains | When to Read |
|------|-----------------|--------------|
| [references/code-templates.md] | Complete HTML/CSS for every section with `{{VARIABLE}}` placeholders | ALWAYS — primary build tool |
| [references/visual-catalog.md] | Structural spec for each of the 9 section types | When choosing layouts or explaining outputs |
| [references/design-system.md] | Color tokens, typography, spacing, anti-patterns | When customizing brand or troubleshooting |
| [references/svg-primitives.md] | Engine badges, platform icons, radial meter, dividers | When a section needs an icon or shape |
| [references/content-library.md] | Voice-rule examples, hook patterns, empty-state copy | When pre-filling or generating fallback content |
| [references/interactive-patterns.md] | JS for editable fields, auto-save, PDF export, share links | When producing an interactive artifact |
| [references/slide-patterns.md] | Hero layouts, section dividers, persona cards, quote cards | When rendering the cover or headline sections |

## The 9 Section Types

A complete Business Brain one-pager has these sections, in order:

1. **Cover Hero** — headshot + name + tagline + 5 engine badges
2. **Voice Card** — tone rules, banned phrases, hook patterns
3. **Business Card** — offer, positioning, 90-day goal
4. **ICP Persona Card** — named avatar, pain, desire, objections
5. **Competitor 3×3 Matrix** — top 3 competitors × positioning/gap/angle
6. **Brand Identity Card** — color palette, typography, visual voice
7. **AI Visibility Scorecard** — radial meter + gap queries
8. **Audience Pain Themes** — top Reddit/forum themes with verbatims
9. **Actions Panel** — 5 engine slash commands, always pinned bottom

Each section has its own template in `code-templates.md` and its own structural spec in `visual-catalog.md`.

## Variable System

Every template uses `{{DOUBLE_BRACE}}` variables. Standard variables:

### Global Variables (every section)
```
{{BRAIN_NAME}}          — "Daniel Paul"
{{BRAIN_TAGLINE}}       — "AI-powered business systems for solopreneurs"
{{BRAIN_HEADSHOT}}      — url or base64 image
{{BRAIN_DATE}}          — "Apr 2026" (auto from render date)
{{BRAND_NAME}}          — "Purely Personal"
{{BRAND_TAGLINE}}       — "purelypersonal.ai"
{{BRAND_ACCENT}}        — "#e90d41" (default) or brand override
```

### Voice Variables
```
{{VOICE_TONE}}          — 2–3 sentence tone description
{{BANNED_PHRASES}}      — array of words/characters to avoid ("—", "unlock", "delve")
{{HOOK_PATTERNS}}       — array of 5 hook formulas
{{EXAMPLE_POSTS}}       — 3 short post excerpts in user's voice
```

### Business Variables
```
{{OFFER}}               — one-line offer statement
{{POSITIONING}}         — one-line positioning
{{PRICING}}             — price point(s)
{{GOAL_90D}}            — 90-day target (one sentence)
{{KEY_METRIC}}          — the one number that matters
```

### ICP Variables
```
{{ICP_NAME}}            — "SaaS Founder, $500k–$5M ARR"
{{ICP_PAIN}}            — array of 3 pains
{{ICP_DESIRE}}          — array of 3 desires
{{ICP_OBJECTIONS}}      — array of 3 objections
{{ICP_WHERE}}           — where they hang out
```

### Competitor Variables
```
{{COMPETITORS}}         — array of 3 { name, positioning, gap, angle }
```

### Brand Variables
```
{{BRAND_COLORS}}        — array of hex values (extracted from site)
{{BRAND_FONTS}}         — { display, body } font names
{{BRAND_VISUAL_VOICE}}  — 1-sentence description of visual style
```

### Intel Variables
```
{{AI_VISIBILITY_SCORE}} — 0–100 integer
{{AI_GAP_QUERIES}}      — array of queries where user doesn't rank
{{PAIN_THEMES}}         — array of { theme, verbatim, source }
```

### Actions Variables
```
{{ACTIONS}}             — array of 5 { command, label, engine, engine_color }
```

## Workflow: Step by Step

### Step 1: Locate the Brain
- If user provides a path, read that file
- Otherwise look for `BUSINESS-BRAIN.md` in project root or `shared/`
- If missing, ask the user to run `/build-my-brain` first — do NOT fabricate data

### Step 2: Parse Sections
Parse the Brain's markdown into the 9 section blocks. For each section, extract the variables listed above. Missing sections render as empty-state cards (see [references/content-library.md] for copy).

### Step 3: Pick Output Mode
- **Single-page HTML** (default): all 9 sections stacked on one tall page
- **Print-optimized**: A4 portrait, one page per section with print CSS
- **Interactive**: same as default + editable fields, auto-save, PDF export button
- **Dashboard strip**: compact 3-column summary for embedding

### Step 4: Assemble
Read [references/code-templates.md] and copy the base page wrapper + each section template. Replace `{{VARIABLES}}` with parsed values. Inject SVGs from [references/svg-primitives.md] where the template has an SVG slot.

### Step 5: Validate
Run the quality checklist below. Do not ship until all boxes check.

### Step 6: Deliver
Output a single HTML artifact. The user can screenshot, print-to-PDF, or run `/export-brain-pdf` for automated export.

## Quality Validation Checklist

Before shipping EVERY render, verify:

**Layout checks:**
- [ ] Page background is `#faf8f4` (warm cream) — never pure white
- [ ] Section cards have `background: #ffffff` with `border: 1px solid #e8e2d8`
- [ ] Border-radius is `4px` on cards, `0` on dividers
- [ ] Section spacing is `32px` between cards, `16px` inside cards
- [ ] Cover hero is full-bleed at top (no margin)
- [ ] Actions Panel is sticky-bottom OR pinned to bottom of page

**Typography checks:**
- [ ] Display font is `'Rethink Sans', 'Inter', sans-serif`
- [ ] Body font is `'Inter', -apple-system, sans-serif`
- [ ] Only 2 weights used: 400 and 700
- [ ] Body text color is `#1a1a1a` — NEVER pure `#000`
- [ ] Secondary text is `#6b6b6b`
- [ ] Labels are 11–12px uppercase with `letter-spacing: 0.06em`

**Color checks:**
- [ ] Primary accent is `#e90d41` (Purely Personal red) unless brand override
- [ ] Engine colors used correctly: Marketing `#3B82F6`, Sales `#22C55E`, Operations `#8B5CF6`, Cash `#EAB308`, Leadership `#DC2626`
- [ ] No gradients except Instagram platform variant
- [ ] Engine badges are filled circles with white icon

**Content checks:**
- [ ] Every `{{VARIABLE}}` is replaced — scan for `{{` before shipping
- [ ] Banned phrases from Voice Card are absent from example text
- [ ] No em-dashes (`—`) anywhere unless user's voice explicitly allows
- [ ] Names, URLs, numbers match the source Brain exactly

**Interaction checks (if interactive mode):**
- [ ] PDF export button renders top-right of page
- [ ] Editable fields have subtle hover state
- [ ] Auto-save indicator appears briefly on change
- [ ] Print CSS hides all buttons and interactive UI

## Quick Triggers

| User Says | Generate |
|-----------|----------|
| "render my brain" | All 9 sections, single-page, default mode |
| "brain one-pager" | Same as above |
| "print my brain" | Print-optimized mode (A4 portrait, page breaks per section) |
| "interactive brain" | All sections + editable fields + auto-save + PDF export |
| "brain dashboard strip" | Compact 3-column summary |
| "brain cover only" | Section 1 only — Cover Hero |
| "competitor matrix" | Section 5 only — 3×3 matrix |
| "voice card" | Section 2 only — Voice Card |
| "ICP card" | Section 4 only — ICP Persona Card |
| "brand card" | Section 6 only — Brand Identity |
| "AI visibility card" | Section 7 only — Scorecard |
| "actions panel" | Section 9 only — 5 engine commands |

## Output Modes

### Single-Page HTML (default)
One long HTML artifact with all 9 sections. Renders in browser. Screenshot-friendly. Good for sharing as a single image.

### Print-Optimized
Same content, with `@media print { page-break-after: always }` on each card. Renders as a 9-page A4 PDF when user hits Cmd+P → Save as PDF.

### Interactive
Default + JS: editable fields, `localStorage` auto-save, PDF-export button, share-to-LinkedIn. Use when the Brain is a living document rather than a one-time artifact.

### Dashboard Strip
3-column compact summary: Left (Voice + Business), Middle (ICP + Competitors), Right (Brand + AI + Actions). For embedding in the top of `README.md` or a Notion page.

## Chaining with Other Skills

This skill sits downstream of Brain-building and upstream of content-production:

- **`/build-my-brain`** → writes `BUSINESS-BRAIN.md` → `business-brain-renderer` visualizes it
- **`content-visual-builder`** ← reads BUSINESS-BRAIN.md voice rules → produces 4-platform content
- **`engine-output-builder`** ← reads Brain → produces per-engine cards (competitor matrix standalone, ICP card standalone, etc.)
- **`linkedin-profile-optimizer`** → feeds Voice Card data
- **`brand-identity-extractor`** → feeds Brand Card data
- **`apify-linkedin`** → feeds Voice + Competitor data
- **`reddit-insights`** → feeds Pain Themes data
- **`ai-discoverability-audit`** → feeds AI Visibility Scorecard

## Anti-patterns (never do these)

- ❌ Never generate Brain content. If a section is missing, render its empty state. Let `/build-my-brain` do the filling.
- ❌ Never use pure `#000` or pure `#ffffff` in body copy. Always the off-variants.
- ❌ Never use em-dashes (`—`) unless the user's voice rules explicitly allow them.
- ❌ Never mix engine colors — each section has exactly one engine color association.
- ❌ Never produce more than one artifact per render call. One page = one render.
- ❌ Never deviate from `code-templates.md`. Copy exactly; fill variables; ship.
