# Visual Catalog — Business Brain Renderer

Every section of a Business Brain one-pager, specified structurally. Use this file to decide which visual to render, what data it needs, and what its anti-patterns are.

Sections are numbered in render order. A complete Brain renders all 9 (plus the V3 Proof Stats Band as 1.5). A partial render picks a subset but keeps the order intact.

**V3 rhythm rule:** every full Brain needs at least 2 dark color drumbeats — the Proof Stats Band (1.5) and the Pain Hero quote (8). These break the warm-cream baseline and turn the one-pager from "nice doc" into "share-worthy editorial."

---

## Section 1 · Cover Hero

**Template:** `code-templates.md` → Template #1
**Engine accent:** `--pp-red` (brand, not an engine)
**Height:** ~480px
**Position:** full-bleed top, no margin

### Purpose
First impression. The single screenshot that gets shared on LinkedIn when someone says *"look what my Claude Code just built for me."* This is the asset the workshop is selling.

### Structural spec
- Headshot: 96×96 round, 2px border
- Name: 48px display, weight 700, -0.01em tracking
- Tagline: 18px body, secondary color, max-width 560px
- Red underline: 48×3px, centered, 32px margin below
- 5 engine badges: 44px circles, flex row, 16px gap, center-aligned
- Meta line: 12px, monospace brand mark, muted

### Variables required
`{{BRAIN_NAME}}`, `{{BRAIN_HEADSHOT}}`, `{{BRAIN_TAGLINE}}`, `{{BRAIN_DATE}}`, `{{ENGINE_BADGES}}`

### When to render
Always. Even a partial Brain always shows the cover — it anchors identity.

### Empty state
If headshot missing: render placeholder avatar SVG (initials circle in `--pp-red-soft` with red initials).
If tagline missing: render `{{BRAIN_NAME}}'s Business Brain` as fallback.

### Anti-patterns
- ❌ Don't use the user's logo here. Use their face. The workshop promise is personal, not corporate.
- ❌ Don't gradient the background beyond the soft cream→white + radial red glows (V3 spec). No bold gradients.
- ❌ Don't animate the engine badges. Static. Print-ready.
- ❌ Don't omit the asymmetric accents (tilted `Ch. 01 / 09` stamp + date tick). They're what distinguish the V3 cover from a generic profile header.

---

## Section 1.5 · Proof Stats Band (V3 — NEW)

**Template:** `code-templates.md` → Template #1.5
**Engine accent:** `--pp-red` on `--dark` background
**Height:** ~180px
**Position:** full-bleed, directly after Cover, before Voice

### Purpose
The page's first dark drumbeat. Three proof stats that justify the whole Brain before anyone reads a single section. Typical values from Danny's own brain: `$0` content-team cost, `2hr/wk` time on content, `5` engines running.

Without this band, the page reads as a clean doc. With it, the page reads as a *receipt* — "this is working, here's the proof."

### Structural spec
- Full-bleed dark (`--dark` = `#0f0f10`) with 3px `--pp-red` bottom border
- Top-left red `◆ PROOF` corner mark (mono, 10px)
- Top-right muted index (`01 · 02 · 03`)
- 3-column grid: each column centered
- Each stat: red uppercase label (10px mono), 88px white big-stat, 13px muted caption
- Thin vertical dividers between columns (10% top/bottom gap)
- Unit suffix (e.g. `/wk`): 60% size, 60% opacity

### Variables required
`{{STAT_1_LABEL}}`, `{{STAT_1_VALUE}}`, `{{STAT_1_CAPTION}}` (×3)

### When to render
Always, if 3 proof stats are available in the Brain. If the Brain has no genuine proof stats, render the section as empty state with CTA `/add-proof-stats`. **Never fabricate proof stats** — false proof is worse than no proof.

### Stat composition rule
Pick 3 from these categories:
- **Stat 1 — Cost saved/avoided:** `$0`, `$499/mo eliminated`, `$2,400 not spent`
- **Stat 2 — Time saved:** `2hr/wk` (from 12), `15min/day` (from 2hr), `0 days/mo`
- **Stat 3 — Quantity running:** `5 engines`, `47 skills`, `3 executives always-on`

### Anti-patterns
- ❌ Don't use cumulative or "total" numbers (`$50k generated`) — they feel like marketing, not proof.
- ❌ Don't use percentages (`93% faster`) — less concrete than a raw number.
- ❌ Don't render 2 stats or 4 stats. Three is the magic number for this band.
- ❌ Don't reorder. Cost → Time → Quantity is the narrative arc (least → most visible outcome).

---

## Section 2 · Voice Card

**Template:** `code-templates.md` → Template #2
**Engine accent:** `--engine-marketing` (blue)
**Height:** ~320px

### Purpose
Prove the AI knows how you write. Show tone, banned phrases, hook patterns, example openings. This is the "wait, that's exactly my voice" moment — so precision matters.

### Structural spec
- Engine indicator: 8×24px blue pill top-left
- Label: "01 · VOICE" (uppercase)
- Title: "How {Name} Writes" (28px display)
- Subtitle: tone description (1–2 sentences)
- 2-column grid:
  - Left: banned phrase pills + voice rules list (3–5 rules)
  - Right: hook patterns (3–5 formulas) + 2–3 example post openings

### Variables required
`{{VOICE_TONE}}`, `{{BANNED_PHRASE_PILLS}}`, `{{VOICE_RULES_LIST}}`, `{{HOOK_PATTERNS_LIST}}`, `{{EXAMPLE_POSTS_CARDS}}`

### When to render
Always. Voice is the single most-referenced section by downstream skills.

### Empty state
If Voice section missing: render the card with a single message *"Run /extract-my-voice to fill this in"* and a CTA linking to the slash command. Do NOT fabricate voice.

### Anti-patterns
- ❌ Don't fill with generic writing tips. Voice is personal or it's nothing.
- ❌ Don't use more than 5 banned phrases — too many reads like a policy doc, not a voice.
- ❌ Example posts must be *real excerpts*. Never paraphrase.

---

## Section 3 · Business Card

**Template:** `code-templates.md` → Template #3
**Engine accent:** `--engine-leadership` (red)
**Height:** ~280px

### Purpose
Single source of truth for what this business sells, to whom, for how much, and what the 90-day target is. Every other engine reads from here.

### Structural spec
- Engine indicator: 8×24px red pill top-left
- Label: "02 · BUSINESS"
- Title: "What {Name} Sells"
- 2-column grid (1.4fr : 1fr):
  - Left: Offer (22px display) + Positioning (15px body) + Pricing (mono)
  - Right: Sub-card with red left-border — 90-Day Goal + Key Metric (40px display number)

### Variables required
`{{OFFER}}`, `{{POSITIONING}}`, `{{PRICING}}`, `{{GOAL_90D}}`, `{{KEY_METRIC_VALUE}}`, `{{KEY_METRIC_LABEL}}`

### When to render
Always — this is the business itself in one card.

### Empty state
If Business section missing: render with placeholder text *"Run /extract-my-business to auto-fill from your site"* and CTA.

### Anti-patterns
- ❌ Don't pad with generic business copy. If the offer is one sentence, that's the whole card.
- ❌ Key metric must be quantitative (number, %, $). If user writes "growth" as their metric, push back — render empty state.
- ❌ No industry jargon. The business card should read clearly to a smart outsider.

---

## Section 4 · ICP Persona Card

**Template:** `code-templates.md` → Template #4
**Engine accent:** `--engine-sales` (green)
**Height:** ~360px

### Purpose
Single persona, deeply specified. Pain / Desire / Objection — the three dimensions every sales copywriter needs. This unlocks `cold-outreach-sequence` and `sales-research-agent`.

### Structural spec
- Engine indicator: 8×24px green pill top-left
- Label: "03 · IDEAL CLIENT"
- Title: "Who {Name} Serves"
- Persona strip: 44px initial circle (green) + name + where-they-hang-out (in green-soft background)
- 3-column grid (Pain / Desire / Objection) with color-coded labels:
  - Pain → `--engine-leadership` red label
  - Desire → `--engine-sales` green label
  - Objection → `--engine-cash` gold label
- Each column: 3–5 bullet items

### Variables required
`{{ICP_INITIAL}}`, `{{ICP_NAME}}`, `{{ICP_WHERE}}`, `{{ICP_PAIN_LIST}}`, `{{ICP_DESIRE_LIST}}`, `{{ICP_OBJECTIONS_LIST}}`

### When to render
Always. Without ICP, downstream sales skills fail silently.

### Empty state
Render empty card with *"Run /define-my-icp to build this in 2 minutes"* + CTA.

### Anti-patterns
- ❌ Don't render multiple ICPs side-by-side. One ICP per Brain. If user has three, build three Brains.
- ❌ Don't use generic demographics ("30–45 year old professional"). Use role + context ("SaaS founder, $500k–$5M ARR, solo or small team").
- ❌ Each bullet must be a specific complaint/desire/objection. Not a category.

---

## Section 5 · Competitor 3×3 Matrix

**Template:** `code-templates.md` → Template #5
**Engine accent:** `--engine-operations` (violet)
**Height:** ~360px

### Purpose
Deliver the moment: *"This is the competitor research I've been paying an agency for."* Three competitors, each with their angle and the gap you can own.

### Structural spec
- 3-column grid with internal vertical borders
- Each column has 3 stacked blocks:
  1. Competitor name (display font) + URL (mono, muted)
  2. "Their angle" — 1-sentence positioning
  3. "Gap to own" — highlighted violet block (violet-soft background, violet left border), 1-sentence angle

### Variables required
`{{COMPETITOR_COLUMNS}}` → each column fills `{{COMP_NAME}}`, `{{COMP_URL}}`, `{{COMP_POSITIONING}}`, `{{COMP_GAP}}`

### When to render
Always, if 3 competitors are provided. If 1–2, render the available columns + an empty third column with *"Add competitor"* CTA.

### Empty state
If no competitors: full card empty state with *"Run /analyze-competitors with 3 URLs"* + CTA.

### Anti-patterns
- ❌ Never more than 3 competitors. Four+ turns into a table — loses visual punch.
- ❌ Don't render competitor logos. Keeps it clean and avoids trademark concerns.
- ❌ The "gap" is not a hole — it's your move. Phrase it as what YOU can own, not what THEY miss.

---

## Section 6 · Brand Identity Card

**Template:** `code-templates.md` → Template #6
**Engine accent:** `--pp-red` (brand, not an engine)
**Height:** ~280px

### Purpose
Colors + fonts + visual voice extracted from user's website. The "it pulled my brand automatically" moment.

### Structural spec
- 2-column grid
- Left: 4-column grid of color swatches (up to 8 colors shown). Each swatch is `aspect-ratio: 1` with hex code below in mono.
- Right: Display font sample (24px in that font, showing "Aa Bb Cc 0 1 2") + Body font sample (16px) + visual voice description (1 sentence)

### Variables required
`{{COLOR_SWATCHES}}` (up to 8), `{{BRAND_DISPLAY_FONT}}`, `{{BRAND_BODY_FONT}}`, `{{BRAND_VISUAL_VOICE}}`

### When to render
Always. If extraction didn't run, render empty state.

### Empty state
*"Run /extract-brand-identity on your site URL"* + CTA.

### Anti-patterns
- ❌ Don't render fonts as images. Use actual `font-family` so they render live if available.
- ❌ Don't show more than 8 colors. Pick the 4–8 most dominant from extraction.
- ❌ Never show pure white (`#ffffff`) or pure black (`#000000`) as "brand colors". Those aren't identity — those are defaults. Filter them out.

---

## Section 7 · AI Visibility Scorecard

**Template:** `code-templates.md` → Template #7
**Engine accent:** `--engine-cash` (gold)
**Height:** ~260px

### Purpose
The "oh god, AI can't find me" moment. Surface the score and name the queries where the user is invisible.

### Structural spec
- 2-column grid (200px : 1fr)
- Left: SVG radial meter (from svg-primitives) displaying 0–100 score in gold
- Right: list of 3–7 gap queries, each in a gold-accented row with a ✗ mark, mono font

### Variables required
`{{RADIAL_METER_SVG}}` (with score baked in), `{{GAP_QUERY_ROWS}}`

### When to render
Always, if audit ran. If no score: empty state.

### Empty state
*"Run /audit-ai-visibility to score your ChatGPT + Perplexity + Claude presence"* + CTA.

### Anti-patterns
- ❌ Don't gamify the score with badges or levels. It's a number, not an achievement.
- ❌ Don't suggest fixes here — that belongs to the downstream `ai-discoverability-audit` skill. Keep this card diagnostic only.
- ❌ If score > 80, render a congratulatory line instead of empty gap list — don't leave the card half-empty.

---

## Section 8 · Pain Themes

**Template:** `code-templates.md` → Template #8
**Engine accent:** `--engine-sales` (green)
**Height:** ~320px

### Purpose
The "wait, this is what my prospects actually say?" moment. Real Reddit/forum verbatims, themed, sourced.

### Structural spec
- 2-column grid of theme cards
- Each card has:
  - Theme name (green uppercase label)
  - Verbatim quote (italic, primary color, line-height 1.55)
  - Source line (mono, muted, prefixed with "— ")

### Variables required
`{{PAIN_THEME_CARDS}}` → each card fills `{{THEME_NAME}}`, `{{VERBATIM}}`, `{{SOURCE}}`

### When to render
Always, if Reddit/forum scraping ran. Render 4–6 themes max (2-col × 2–3 rows).

### Empty state
*"Run /pull-reddit-pain on your ICP keyword"* + CTA.

### V3 layout: hero quote + 3 small
The card opens with ONE full-width hero quote on dark charcoal — the most emotionally resonant verbatim, 28px italic display, giant red `"` decoration, `◆ TOP THEME` tag. Below: 3-column grid of smaller themes (13px italic, 44px faded `"` decoration).

Theme picking:
- **Hero:** most personal/raw quote (the one readers re-read)
- **Three small:** topical variety (not 3 variations of the same complaint)
- Verbatims in small cards may be trimmed for length (only from start/end — never paraphrase)

### Anti-patterns
- ❌ Don't edit or paraphrase verbatims in the hero. Full raw quote or nothing. Typos stay in.
- ❌ Don't over-theme. 4–6 clusters max. More themes = blurrier insight.
- ❌ Source must be specific (subreddit name, forum thread). "Reddit" is not a source; "r/SaaS" is.
- ❌ Don't skip the hero → the V3 page *needs* that second dark drumbeat.

---

## Section 9 · Actions Panel

**Template:** `code-templates.md` → Template #9
**Engine accent:** `--pp-red` border + 5 engine colors in cards
**Height:** ~240px
**Position:** bottom of page (sticky optional in interactive mode)

### Purpose
Make the Brain *actionable*. Five engine commands, one per engine, each reading this Brain as context.

### Structural spec
- Card with 2px red border and "TAKE ACTION" badge top-left
- 5-column grid of action cards (stacks to 2-col, then 1-col on small screens)
- Each action card:
  - Engine-colored soft background
  - Engine-colored border
  - Engine icon in filled circle (top)
  - Action label (display, 14px, 700)
  - Command in mono (engine color)

### Variables required
`{{ACTION_CARDS}}` (always 5 — hardcoded list)

### The 5 actions (always identical)

| # | Engine | Label | Command |
|---|---|---|---|
| 1 | Marketing | Ship This Week's Content | `/marketing-engine` |
| 2 | Sales | Research + Outreach | `/sales-engine` |
| 3 | Operations | Triage + SOPs | `/operations-engine` |
| 4 | Cash | Pull + Forecast | `/cash-engine` |
| 5 | Leadership | Morning Brief | `/leadership-engine` |

### When to render
Always. This is the single consistent anchor across every Brain render.

### Empty state
Never empty. Even if other sections are empty, Actions are always rendered — they're the call to action to fill the Brain.

### Anti-patterns
- ❌ Don't reorder. Marketing → Sales → Operations → Cash → Leadership is the fixed order.
- ❌ Don't add a 6th action. Five engines, five cards.
- ❌ Don't rename the commands. The slash commands must match exactly what the plugin registers.

---

## Dashboard Strip (alt output)

**Template:** `code-templates.md` → Template #10
**Engine accent:** none (uses `--pp-red` for brand mark only)
**Height:** ~180px

### Purpose
Compact summary for embedding at the top of a README, Notion page, or email. Not a replacement for the full Brain — a preview.

### Structural spec
- 3-column grid
- Col 1: Name, tagline, 1-sentence voice summary
- Col 2: ICP name, offer (with dividers)
- Col 3: 90-day goal, AI visibility score (big number + label)

### When to render
Only when user explicitly asks for "dashboard strip", "compact brain", or "brain summary".

### Anti-patterns
- ❌ Don't use instead of full render unless asked. Full render is the hero.

---

## Choice Tree

Use this to decide what to render:

```
User request → match keyword:
  "render my brain" / "full brain" / "brain one-pager"
    → All 9 sections, single-page mode

  "print my brain" / "brain pdf"
    → All 9 sections, print-optimized mode (1 section per page)

  "interactive brain" / "editable brain"
    → All 9 sections + interactive-patterns.md scripts

  "brain summary" / "dashboard strip" / "compact brain"
    → Template #10 only

  "voice card" / "ICP card" / "competitor matrix" / etc.
    → Only that section, on a minimal page wrapper

  "cover slide" / "brain hero"
    → Section 1 only, full-bleed
```

---

## Section Rendering Order

Fixed. Do NOT reorder without user request.

```
1.   Cover Hero                            ← warm opening
1.5  Proof Stats Band  ◆ dark drumbeat    ← V3: the receipt
2.   Voice Card
3.   Business Card      ◆ red stat card    ← internal hero stat
4.   ICP Persona Card   ◆ green gradient   ← internal color moment
5.   Competitor 3×3     ◆ violet gaps      ← internal color moment
6.   Brand Identity Card
7.   AI Visibility Scorecard
8.   Pain Themes        ◆ dark drumbeat    ← V3: emotional peak
9.   Actions Panel      ◆ red close
     Footer
```

This order moves from **identity** (who you are) → **proof** (it works) → **market** (who you serve, who competes) → **visibility** (how you're seen) → **emotion** (their pain in their words) → **action** (what to do now). Reordering breaks the narrative arc.

The dark drumbeats at 1.5 and 8 bookend the warm middle. The colored moments at 3/4/5 provide internal rhythm. The red actions close the arc.

---

## Quality Bar Per Section

Every section must satisfy these, or render the empty state instead:

| Section | Quality bar |
|---------|-------------|
| Cover | Real headshot OR initials placeholder. Real tagline OR fallback. Never generic stock imagery. |
| Voice | ≥3 banned phrases + ≥3 voice rules + ≥2 example posts, OR empty state. |
| Business | Offer (≤15 words) + positioning (≤20 words) + quantitative metric. |
| ICP | Named persona (role + context) + ≥3 pains + ≥3 desires + ≥3 objections. |
| Competitors | 3 named competitors, each with positioning + gap. |
| Brand | ≥3 colors + ≥2 fonts + visual voice sentence. |
| AI Visibility | Score 0–100 integer + ≥3 gap queries (if score < 80). |
| Pain Themes | ≥3 themes with real verbatims + real sources. |
| Actions | Always 5 actions. Never fewer, never more. |

Fall back to empty state rather than fabricate. Empty state ≠ failure — it's an explicit CTA to fill the gap.
