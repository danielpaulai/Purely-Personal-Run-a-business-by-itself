# Design System — Business Brain Renderer

The complete token system for rendering Business Brain one-pagers in the Purely Personal visual language. Use these tokens as CSS custom properties and as literal hex values inside inline-styled templates.

---

## Color Palette

### Page & Surface Tokens

| Token | Hex | Usage |
|-------|-----|-------|
| `page-bg` | `#faf8f4` | Warm cream page background — never pure white |
| `card-bg` | `#ffffff` | Section card fill |
| `sub-card-bg` | `#fbf9f6` | Nested box inside a card |
| `divider` | `#e8e2d8` | All borders, dividers, rule lines |
| `divider-strong` | `#d0cdc8` | Stronger borders for emphasis rows |
| `shadow-soft` | `rgba(20, 14, 8, 0.04)` | Subtle card shadow (use sparingly) |
| `dark` | `#0f0f10` | Full-bleed dark sections (Proof Band, Pain Hero) |
| `dark-card` | `#1a1a1d` | Dark sub-surfaces / gradient endpoints |
| `dark-border` | `#2a2a2e` | Dividers on dark surfaces |
| `pp-red-whisper` | `#fdf2f5` | Faded red for hero numerals and soft decorations |

### Text Tokens

| Token | Hex | Usage |
|-------|-----|-------|
| `text-primary` | `#1a1a1a` | Near-black for headings and body — NEVER `#000` |
| `text-secondary` | `#6b6b6b` | Labels, helper text, metadata |
| `text-muted` | `#a8a39b` | Footer text, timestamps, hints |
| `text-inverse` | `#ffffff` | Text on dark/engine-colored surfaces |

### Brand Accents (Purely Personal)

| Token | Hex | Usage |
|-------|-----|-------|
| `pp-red` | `#e90d41` | Primary accent — hero underline, CTA buttons, brand mark |
| `pp-red-deep` | `#c70a38` | Hover state, active state |
| `pp-red-soft` | `#fce8ed` | Tinted background for red highlights |
| `pp-charcoal` | `#0a0a0a` | Dark mode surfaces |
| `pp-silver` | `#b8bec1` | Secondary metal, subtle dividers on dark |

### The Five Engine Colors

One color per engine. Used for engine badges, section accents, and the Actions Panel command pills.

| Engine | Token | Hex | Soft Tint (bg) |
|--------|-------|-----|----------------|
| Marketing | `engine-marketing` | `#3B82F6` | `#EBF2FE` |
| Sales | `engine-sales` | `#22C55E` | `#E8FAEE` |
| Operations | `engine-operations` | `#8B5CF6` | `#F1ECFD` |
| Cash | `engine-cash` | `#EAB308` | `#FCF5D9` |
| Leadership | `engine-leadership` | `#DC2626` | `#FCE8E8` |

### The Four Platform Colors

Used only by `content-visual-builder`. Included here for shared-system consistency.

| Platform | Token | Value |
|----------|-------|-------|
| LinkedIn | `platform-linkedin` | `#0A66C2` |
| X | `platform-x` | `#0F1419` |
| Instagram | `platform-instagram` | `linear-gradient(135deg, #833AB4, #FD1D1D, #FCB045)` |
| Newsletter | `platform-newsletter` | `#E8D9C5` |

### CSS Custom Property Block

Drop this inside `:root` for any rendered HTML:

```css
:root {
  /* Surfaces */
  --page-bg: #faf8f4;
  --card-bg: #ffffff;
  --sub-card-bg: #fbf9f6;
  --divider: #e8e2d8;
  --divider-strong: #d0cdc8;
  --shadow-soft: 0 1px 2px rgba(20,14,8,0.04);

  /* Dark surfaces (rhythm breaks) */
  --dark: #0f0f10;
  --dark-card: #1a1a1d;
  --dark-border: #2a2a2e;

  /* Text */
  --text-primary: #1a1a1a;
  --text-secondary: #6b6b6b;
  --text-muted: #a8a39b;
  --text-inverse: #ffffff;

  /* Brand */
  --pp-red: #e90d41;
  --pp-red-deep: #c70a38;
  --pp-red-soft: #fce8ed;
  --pp-red-whisper: #fdf2f5;

  /* Engines */
  --engine-marketing: #3B82F6;
  --engine-sales: #22C55E;
  --engine-operations: #8B5CF6;
  --engine-cash: #EAB308;
  --engine-leadership: #DC2626;

  --engine-marketing-soft: #EBF2FE;
  --engine-sales-soft: #E8FAEE;
  --engine-operations-soft: #F1ECFD;
  --engine-cash-soft: #FCF5D9;
  --engine-leadership-soft: #FCE8E8;
}
```

### V3 Rhythm Rule

The page must have **color drumbeats** that break the warm baseline:
- Warm cover (cream + white) → **dark proof band** → warm cards → **hero colored card** ($75K red, ICP green, competitor violet gaps) → warm → **dark pain hero** → **red actions close**

A Brain render without at least 2 dark sections feels too flat. A Brain render with more than 3 dark sections feels too heavy. Target: **dark proof band + dark pain hero** = 2 dark moments minimum.

---

## Typography

### Font Stack

```css
/* Display — headings, hero copy, framework names */
font-family: 'Rethink Sans', 'Inter', -apple-system, sans-serif;

/* Body — all prose, labels, values */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Mono — code blocks, slash commands, hex values */
font-family: 'JetBrains Mono', 'SF Mono', Menlo, monospace;
```

### Scale

| Element | Size | Weight | Style | Color |
|---------|------|--------|-------|-------|
| Cover hero name | **72px** | **800** | letter-spacing: -0.03em | `var(--text-primary)` |
| Cover tagline | **22px** | 400 | — | `var(--text-secondary)` |
| Proof band big stat | **88px** | **800** | letter-spacing: -0.03em, tnum | `#ffffff` on dark |
| Business card hero stat | **96px** | **800** | letter-spacing: -0.03em, tnum | `#ffffff` on red gradient |
| AI score (radial center) | **88px** | **800** | letter-spacing: -3 | `var(--text-primary)` |
| Pain hero quote | **28px** | **700** | italic | `#ffffff` on dark |
| Section title | 30px | **800** | letter-spacing: -0.015em | `var(--text-primary)` |
| Section hero numeral (editorial bg) | **72px** | **800** | tnum | `var(--pp-red-whisper)` |
| Section label (uppercase) | 11px | **700** | letter-spacing: 0.1em | `var(--pp-red)` |
| Card title | 20px | **800** | — | `var(--text-primary)` |
| Card subtitle | 15px | 400 | — | `var(--text-secondary)` |
| Body text | 14–15px | 400 | — | `var(--text-primary)` |
| Stat label (small) | 10–11px | **700** | uppercase, letter-spacing: 0.1–0.15em | context-dependent |
| Mono (slash command) | 11–13px | 500 | — | engine color |
| Signature block (data) | 12px | 400 | mono, on dark | `#fff` with red label |
| Vertical chapter marker | 10px | **700** | mono, rotate 90°, letter-spacing: 0.15em | `var(--pp-red)` |
| Footer brand name | 22px | **800** | — | `var(--text-primary)` |
| Footer meta | 12px | 400 | mono | `var(--text-muted)` |

### Rules

- Only 2 weights: **400 (regular)** and **700 (bold)**. Never 500, 600, 800.
- Only 1 italic usage: direct verbatim quotes from Reddit/forums. Everywhere else upright.
- Left-align all prose. Center only: Cover hero, big stats, engine badges row.
- Labels are UPPERCASE with `letter-spacing: 0.06em`. Titles are sentence case.
- Never underline anything except links. Links use `color: var(--pp-red); text-decoration: none; border-bottom: 1px solid currentColor;`

---

## Layout

### Page Dimensions

```
Single-page mode:   max-width: 960px; margin: 0 auto; padding: 0 32px;
Print-optimized:    A4 portrait 595 × 842pt per section
Dashboard strip:    max-width: 1200px; 3-column grid
```

### Spacing Scale

Use a 4px base unit:

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Tight (icon-text) |
| `space-2` | 8px | Between label and value |
| `space-3` | 12px | Inside a pill/badge |
| `space-4` | 16px | Inside a card |
| `space-6` | 24px | Between cards (tight) |
| `space-8` | 32px | Between cards (default) |
| `space-12` | 48px | Between major sections |
| `space-16` | 64px | Hero top/bottom padding |

### Grid

- Cover Hero: **full-bleed** (no max-width), text block centered with `max-width: 720px`
- Voice Card, Business Card, Brand Card: **2-column** at ≥768px, stack below
- ICP Card, AI Visibility Card: **full-width single column**
- Competitor Matrix: **3-column grid** (`grid-template-columns: repeat(3, 1fr)`)
- Pain Themes: **2-column grid** at ≥768px
- Actions Panel: **5-column grid** at ≥900px, 2-column below, stack at mobile

---

## Borders & Corners

- Card border: `1px solid var(--divider)`
- Strong divider: `1px solid var(--divider-strong)` (e.g. inside stat rows)
- **Border-radius:** `4px` on cards, `8px` on pills/badges, `999px` on circular badges, `0` on full-bleed dividers
- No double borders. No dashed. No dotted.

---

## Shadows & Elevation

Soft and minimal. The design reads as flat-with-warmth, not Material.

| Level | Value |
|-------|-------|
| Card resting | `box-shadow: 0 1px 2px rgba(20,14,8,0.04)` |
| Card hover (interactive mode) | `box-shadow: 0 4px 12px rgba(20,14,8,0.08)` |
| Engine badge | no shadow |
| PDF export button | `box-shadow: 0 2px 8px rgba(233,13,65,0.25)` |

Print CSS strips all shadows.

---

## Iconography Rules

All icons from [references/svg-primitives.md]. Rules:

- Stroke-only for decorative shapes; filled for engine badges
- Stroke width: `1.5` for 16–24px icons, `2` for ≥32px
- Stroke color: `currentColor` (inherits from text)
- Never use emoji in data sections (Voice, ICP, Competitors). Emoji OK in section labels only.

---

## Motion

Subtle. The one-pager is primarily a static artifact; motion only appears in interactive mode.

| Interaction | Motion |
|-------------|--------|
| Card hover (interactive) | `transition: box-shadow 160ms ease` |
| Editable field focus | `transition: background 120ms ease; background: var(--pp-red-soft)` |
| Auto-save indicator | fade in 200ms, hold 1.2s, fade out 300ms |
| PDF export click | no motion — immediate |

Never use spring, bounce, or stagger animations. Motion is purely functional feedback.

---

## Print CSS Rules

Every rendered artifact includes print-specific rules:

```css
@media print {
  :root { --page-bg: #ffffff; }             /* Save ink */
  body { background: #ffffff; }
  .no-print { display: none !important; }   /* Hide buttons */
  .page-break { page-break-after: always; } /* One section per page in print-optimized mode */
  .card { box-shadow: none; }
  a { color: var(--text-primary); }         /* No color ink for links */
}
```

Any interactive control (edit button, save indicator, PDF export button) gets `class="no-print"`.

---

## Anti-patterns

**Never do these. Ever.**

- ❌ Pure `#000` or `#ffffff` for text or large surfaces. Always use the warm off-variants.
- ❌ Gradients anywhere except the Instagram platform variant.
- ❌ Multiple font families on the same card.
- ❌ Rounded corners > 8px on cards.
- ❌ Drop shadows on text.
- ❌ Italic body copy (reserved for verbatim quotes only).
- ❌ Centered body text (reserved for hero + stats only).
- ❌ More than 2 font weights on the same page.
- ❌ Emoji used as data (e.g. in Voice rules or ICP pain). Emoji OK in labels only.
- ❌ Using engine colors as page backgrounds. Engine colors are accents, not fills.
- ❌ Mixing engine accents inside a single card (one card = one engine).
- ❌ Placeholder text that says "Lorem ipsum" or "Example value". If data is missing, render the empty state from `content-library.md`.

---

## Brand Override (for partner decks)

If the user invokes a custom brand mode, override only these tokens:

```
--pp-red          →  client's primary accent
--display-font    →  client's display font
--body-font       →  client's body font
```

All other tokens (engine colors, spacing, typography scale) stay fixed. Engine colors are part of the product identity, not the Purely Personal brand.

---

## Quality Anchor

When in doubt, compare against this mental reference:

> *"Stripe's docs site, but with a 1980s business consultant's warmth — serif/sans mix, cream paper, red accent, generous whitespace, zero chrome."*

If the render feels colder than that, add warmth (bigger line-height, more whitespace, warmer background). If it feels busier than that, strip chrome (fewer borders, less color, more quiet).
