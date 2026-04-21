# Slide Patterns — Business Brain Renderer

Pre-engineered layout patterns for cover, section dividers, persona/quote cards, and presentation-style renderings. These are the visual "chapter markers" of a Business Brain — the Cover Hero, section dividers in print-optimized mode, and standalone single-section renders used as screenshotable micro-assets.

Use patterns from this file when:
- Rendering the Cover Hero (Section 1)
- Generating a standalone section render (e.g. "just the ICP card")
- Building print-optimized mode where each section gets a full-page divider
- Making a screenshot-worthy micro-asset for LinkedIn sharing

---

## Pattern 1 — Cover Hero (full-bleed)

The signature opener. Defined structurally in [visual-catalog.md] §1 and implemented in [code-templates.md] Template #1. This file adds the layout variants:

### Variant 1A — Standard Cover

```
┌────────────────────────────────────────────────┐
│                                                │
│                   [96×96]                      │
│                                                │
│               Daniel Paul                      │  ← 48px display 700
│   AI-powered business systems for solopreneurs │  ← 18px secondary
│                                                │
│                   ────                         │  ← 48×3 red accent
│                                                │
│      ●    ●    ●    ●    ●                     │  ← 5 engine badges
│      M    S    O    C    L                     │
│                                                │
│   BUSINESS BRAIN · Apr 2026 · Purely Personal  │  ← 12px meta
│                                                │
└────────────────────────────────────────────────┘
```

Used when a full headshot is available and the Brain is public-facing.

### Variant 1B — Initials Cover (no headshot)

Same structure, with placeholder avatar SVG (initials in `--pp-red-soft` circle with `--pp-red` initials — see [svg-primitives.md]).

### Variant 1C — Minimalist Cover

For users who want maximum focus, drop the headshot and shrink vertical padding:

```
┌────────────────────────────────────────────────┐
│                                                │
│               Daniel Paul                      │
│   AI-powered business systems for solopreneurs │
│                                                │
│                   ────                         │
│                                                │
│      ●    ●    ●    ●    ●                     │
│                                                │
└────────────────────────────────────────────────┘
```

Use when user says "minimalist cover" or the Brain is embedded inside a larger asset.

---

## Pattern 2 — Section Divider (print-optimized mode only)

In print-optimized mode, each section gets a full-page divider before it so the PDF paginates cleanly. Divider is ~40% page height, centered.

```html
<section class="page-break" style="display:flex;align-items:center;justify-content:center;min-height:400px;text-align:center;background:var(--page-bg);padding:48px 24px">
  <div>
    <div class="label" style="margin-bottom:16px">{{SECTION_NUMBER}}</div>
    <h2 style="font-family:var(--display);font-size:56px;font-weight:700;margin:0 0 12px;line-height:1.05;letter-spacing:-0.01em">{{SECTION_NAME}}</h2>
    <p style="font-size:16px;color:var(--text-secondary);margin:0 0 24px;max-width:520px;margin-left:auto;margin-right:auto">{{SECTION_SUBTITLE}}</p>
    <div style="width:32px;height:2px;background:var({{ENGINE_VAR}});margin:0 auto"></div>
  </div>
</section>
```

### Section Subtitle Mapping

Use these canonical subtitles (one line each):

| Section | Subtitle |
|---------|----------|
| 01 Voice | "How you actually write, as rules your AI can follow" |
| 02 Business | "What you sell, who you sell it to, what's next" |
| 03 Ideal Client | "One named person, specified deeply" |
| 04 Competitors | "Three competitors, three gaps to own" |
| 05 Brand Identity | "The visual language your AI should match" |
| 06 AI Visibility | "How ChatGPT, Perplexity, and Claude answer for you" |
| 07 Audience Pain | "Real complaints from real users, pulled live" |
| 08 Take Action | "Five commands. Each one reads this Brain." |

### Engine Color Mapping for Divider Accent

| Section | `{{ENGINE_VAR}}` |
|---------|------------------|
| 01 Voice | `--engine-marketing` |
| 02 Business | `--engine-leadership` |
| 03 Ideal Client | `--engine-sales` |
| 04 Competitors | `--engine-operations` |
| 05 Brand Identity | `--pp-red` |
| 06 AI Visibility | `--engine-cash` |
| 07 Audience Pain | `--engine-sales` |
| 08 Take Action | `--pp-red` |

---

## Pattern 3 — Standalone Section Page

When a user requests a single section as a standalone (e.g. "just the ICP card"), wrap it in this minimal page shell so it works as its own asset:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{SECTION_NAME}} — {{BRAIN_NAME}}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Rethink+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>
/* Same :root CSS custom properties as base wrapper */
/* ... */
body{background:var(--page-bg);margin:0;padding:48px 32px;font-family:var(--body)}
main{max-width:720px;margin:0 auto}
</style>
</head>
<body>
<main>

  <!-- Mini-header (top-left brand mark) -->
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:24px">
    <div style="width:20px;height:20px;background:var(--pp-red);border-radius:4px"></div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text-secondary)">{{BRAIN_NAME}} · Business Brain</div>
  </div>

  {{SECTION_CARD}}

  <!-- Footer -->
  <footer style="margin-top:32px;padding-top:20px;border-top:1px solid var(--divider);display:flex;justify-content:space-between;font-size:12px;color:var(--text-muted)">
    <span>{{SECTION_NUMBER}} of 9</span>
    <span style="font-family:var(--mono)">purelypersonal.ai</span>
  </footer>

</main>
</body>
</html>
```

This shell prioritizes screenshotability — single section centered, brand mark visible, no padding waste.

---

## Pattern 4 — Hero Quote Card

A single-concept render used when someone wants to share one verbatim pain quote or one voice rule as a standalone graphic. Ideal for LinkedIn square posts (1080×1080 or equivalent).

```html
<section style="background:var(--card-bg);padding:56px 48px;max-width:720px;margin:0 auto;border:1px solid var(--divider);border-radius:4px;position:relative">

  <!-- Corner brand -->
  <div style="position:absolute;top:20px;right:24px;font-family:var(--mono);font-size:10px;color:var(--text-muted);letter-spacing:0.08em;text-transform:uppercase">{{BRAIN_NAME}} · Brain</div>

  <!-- Big quote mark (decorative) -->
  <div style="color:var(--pp-red);opacity:0.15;margin-bottom:-40px">
    <svg width="80" height="60" viewBox="0 0 80 60" fill="currentColor">
      <path d="M20 60V30h15V10H10v20h5c0 15-10 20-10 20v10c15 0 15-10 15-10l-5-10z M60 60V30h15V10H50v20h5c0 15-10 20-10 20v10c15 0 15-10 15-10l-5-10z"/>
    </svg>
  </div>

  <!-- Quote -->
  <p style="font-family:var(--display);font-size:32px;font-weight:700;line-height:1.25;margin:0 0 32px;color:var(--text-primary)">"{{QUOTE}}"</p>

  <!-- Attribution -->
  <div style="display:flex;align-items:center;gap:12px;padding-top:20px;border-top:1px solid var(--divider)">
    <div style="width:40px;height:40px;border-radius:999px;overflow:hidden;background:var(--pp-red-soft);flex-shrink:0">
      <img src="{{BRAIN_HEADSHOT}}" style="width:100%;height:100%;object-fit:cover" alt="{{BRAIN_NAME}}">
    </div>
    <div>
      <div style="font-family:var(--display);font-size:14px;font-weight:700">{{BRAIN_NAME}}</div>
      <div style="font-size:12px;color:var(--text-secondary)">{{ATTRIBUTION_LINE}}</div>
    </div>
  </div>
</section>
```

Used when: user says "make a quote card", "share this as a graphic", or any Pain Theme verbatim needs to be broken out as a standalone.

---

## Pattern 5 — Stat Row

A 3-stat horizontal row. Used at the top of the Business Card or in dashboard strip when showing 3 key numbers side-by-side.

```html
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;border:1px solid var(--divider);border-radius:4px;overflow:hidden;background:var(--card-bg)">

  <div style="padding:20px 24px;border-right:1px solid var(--divider);text-align:center">
    <div style="font-family:var(--display);font-size:44px;font-weight:700;line-height:1;font-feature-settings:'tnum';color:var(--text-primary)">{{STAT_1_VALUE}}</div>
    <div class="label" style="margin-top:6px">{{STAT_1_LABEL}}</div>
  </div>

  <div style="padding:20px 24px;border-right:1px solid var(--divider);text-align:center">
    <div style="font-family:var(--display);font-size:44px;font-weight:700;line-height:1;font-feature-settings:'tnum';color:var(--text-primary)">{{STAT_2_VALUE}}</div>
    <div class="label" style="margin-top:6px">{{STAT_2_LABEL}}</div>
  </div>

  <div style="padding:20px 24px;text-align:center">
    <div style="font-family:var(--display);font-size:44px;font-weight:700;line-height:1;font-feature-settings:'tnum';color:var(--pp-red)">{{STAT_3_VALUE}}</div>
    <div class="label" style="margin-top:6px">{{STAT_3_LABEL}}</div>
  </div>

</div>
```

### Standard Stat Combinations

For the top-of-Brain stat row (optional):

| Stat 1 | Stat 2 | Stat 3 |
|--------|--------|--------|
| `{{YEARS_IN_BUSINESS}}` years | `{{ICP_COUNT}}` clients served | `{{AI_VISIBILITY_SCORE}}`/100 AI score |

Or for the Business Card internal stats:

| Stat 1 | Stat 2 | Stat 3 |
|--------|--------|--------|
| `{{PRICE_POINT}}` starting | `{{DELIVERY_TIME}}` timeframe | `{{CAPACITY}}` slots |

Stat 3 is always the "hero" stat — rendered in `--pp-red`. Stats 1 and 2 are primary text color.

---

## Pattern 6 — Two-Column Compare (Before / After)

Used rarely in Brain renders, but useful for showing Before (user's current positioning) vs After (proposed positioning from competitor analysis).

```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--divider);border-radius:4px;overflow:hidden">

  <!-- BEFORE -->
  <div style="padding:24px 28px;background:var(--sub-card-bg);border-right:1px solid var(--divider)">
    <div class="label" style="color:var(--text-muted);margin-bottom:10px">Before</div>
    <p style="font-family:var(--display);font-size:18px;font-weight:400;line-height:1.4;margin:0;color:var(--text-secondary)">{{BEFORE_TEXT}}</p>
  </div>

  <!-- AFTER -->
  <div style="padding:24px 28px;background:var(--card-bg);border-left:3px solid var(--pp-red);margin-left:-1px">
    <div class="label" style="color:var(--pp-red);margin-bottom:10px">After</div>
    <p style="font-family:var(--display);font-size:18px;font-weight:700;line-height:1.4;margin:0;color:var(--text-primary)">{{AFTER_TEXT}}</p>
  </div>

</div>
```

Use sparingly — more than one compare per Brain reads as gimmicky.

---

## Pattern 7 — Engine Badge Row (reusable across sections)

5 badges in a row, used in Cover Hero and can be dropped into any section as a navigation hint.

```html
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;padding:16px 0">
  {{ENGINE_BADGE_1}}
  {{ENGINE_BADGE_2}}
  {{ENGINE_BADGE_3}}
  {{ENGINE_BADGE_4}}
  {{ENGINE_BADGE_5}}
</div>
```

Each badge is generated from the sub-template in [code-templates.md] Template #1 (Engine Badge Sub-Template).

### Compact Variant (for dashboard strip)

Smaller, no labels:

```html
<div style="display:flex;gap:6px">
  <div style="width:20px;height:20px;border-radius:999px;background:var(--engine-marketing)"></div>
  <div style="width:20px;height:20px;border-radius:999px;background:var(--engine-sales)"></div>
  <div style="width:20px;height:20px;border-radius:999px;background:var(--engine-operations)"></div>
  <div style="width:20px;height:20px;border-radius:999px;background:var(--engine-cash)"></div>
  <div style="width:20px;height:20px;border-radius:999px;background:var(--engine-leadership)"></div>
</div>
```

---

## Pattern 8 — Red Accent Line (section transitions)

Between sections in single-page mode, use a subtle red accent rather than a divider rule. Adds brand warmth without chrome.

```html
<div style="display:flex;align-items:center;gap:12px;margin:32px 0">
  <div style="flex:1;height:1px;background:var(--divider)"></div>
  <div style="width:16px;height:2px;background:var(--pp-red)"></div>
  <div style="flex:1;height:1px;background:var(--divider)"></div>
</div>
```

Use at most 2–3 times per Brain. More than that and it becomes noise.

---

## Pattern 9 — Footer (end of Brain page)

Every rendered Brain ends with this footer block. Provides meta, brand, and a subtle call-to-action.

```html
<footer style="margin-top:64px;padding-top:32px;border-top:1px solid var(--divider);text-align:center">

  <!-- Brand mark -->
  <div style="display:inline-flex;align-items:center;gap:8px;margin-bottom:12px">
    <div style="width:24px;height:24px;background:var(--pp-red);border-radius:4px;display:flex;align-items:center;justify-content:center;color:#fff;font-family:var(--display);font-weight:700;font-size:13px">pp</div>
    <div style="font-family:var(--display);font-weight:700;font-size:16px">Purely Personal</div>
  </div>

  <!-- Meta line -->
  <div style="font-size:12px;color:var(--text-muted);font-family:var(--mono)">
    BUSINESS BRAIN · {{BRAIN_DATE}} · purelypersonal.ai
  </div>

  <!-- Subtle CTA -->
  <div style="margin-top:12px;font-size:12px;color:var(--text-secondary)">
    Built with <a href="https://github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself" style="color:var(--pp-red);text-decoration:none;border-bottom:1px solid currentColor">purely-personal</a>
  </div>

</footer>
```

---

## Page Order in a Complete Brain

Fixed order. Print-optimized mode inserts a Section Divider (Pattern 2) before each content section. Single-page mode inserts an Accent Line (Pattern 8) between major transitions only.

```
1. Cover Hero                                    (Pattern 1)
   [Accent Line]                                 (Pattern 8)
2. Voice Card                                    (Template #2)
3. Business Card                                 (Template #3)
   [Accent Line]                                 (Pattern 8)
4. ICP Persona Card                              (Template #4)
5. Competitor 3×3 Matrix                         (Template #5)
   [Accent Line]                                 (Pattern 8)
6. Brand Identity Card                           (Template #6)
7. AI Visibility Scorecard                       (Template #7)
   [Accent Line]                                 (Pattern 8)
8. Pain Themes                                   (Template #8)
9. Actions Panel                                 (Template #9)
   Footer                                        (Pattern 9)
```

Print-optimized mode:

```
1. Cover Hero
   [Page break → Section Divider 01]
2. Voice Card
   [Page break → Section Divider 02]
3. Business Card
   [Page break → Section Divider 03]
4. ICP Persona Card
...
9. Actions Panel
   Footer
```

---

## Anti-patterns for Slide Patterns

- ❌ **Never animate the Cover Hero.** It's a still asset. No typewriter effects, no reveals.
- ❌ **Never stack more than one Section Divider before content.** One divider, one section.
- ❌ **Never use the Hero Quote pattern for anything except a single quote.** It's not a caption, tweet embed, or bio card.
- ❌ **Never put all 3 stats in `--pp-red`.** Only the hero stat (stat 3). More than one and they stop reading as a hierarchy.
- ❌ **Never omit the Footer.** Every Brain must be attributable. The brand mark at the bottom is not decoration — it's the source-of-truth stamp.
- ❌ **Never use Pattern 6 (Before/After) for anything other than positioning comparisons.** It's not a feature comparison, a before/after photo grid, or a pricing table.
