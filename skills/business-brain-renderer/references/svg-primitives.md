# SVG Primitives — Business Brain Renderer

Every SVG used in a Business Brain render. Copy exactly — do not reconstruct from memory. All SVGs are stroke-only or simple fills, optimized for inline HTML embedding, print, and PDF export.

Rules:
- All SVGs use `viewBox` so they scale cleanly
- `currentColor` is used for stroke where the icon inherits from text
- Engine icons use `fill="currentColor"` on the primary shape + white stroke where needed
- Never reference external images. Everything inlined.

---

## Engine Icons (5 × 24px, rendered inside 44px filled circles)

All engine icons are designed to render as white shapes on a colored circle background. Use inside Cover Hero badges and Actions Panel cards.

### 1. Marketing Engine — Megaphone

```html
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 10v4a1 1 0 001 1h2l4 4V5L6 9H4a1 1 0 00-1 1z" fill="#ffffff"/>
  <path d="M14 7s2 1.5 2 5-2 5-2 5" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
  <path d="M18 4s4 3 4 8-4 8-4 8" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
</svg>
```

### 2. Sales Engine — Target

```html
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="9" stroke="#ffffff" stroke-width="2"/>
  <circle cx="12" cy="12" r="5" stroke="#ffffff" stroke-width="2"/>
  <circle cx="12" cy="12" r="1.5" fill="#ffffff"/>
</svg>
```

### 3. Operations Engine — Grid/Kanban

```html
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="3" width="7" height="10" rx="1" stroke="#ffffff" stroke-width="2"/>
  <rect x="14" y="3" width="7" height="6" rx="1" stroke="#ffffff" stroke-width="2"/>
  <rect x="3" y="17" width="7" height="4" rx="1" stroke="#ffffff" stroke-width="2"/>
  <rect x="14" y="13" width="7" height="8" rx="1" stroke="#ffffff" stroke-width="2"/>
</svg>
```

### 4. Cash Engine — Bar Chart Ascending

```html
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="14" width="4" height="7" fill="#ffffff"/>
  <rect x="10" y="9" width="4" height="12" fill="#ffffff"/>
  <rect x="17" y="4" width="4" height="17" fill="#ffffff"/>
</svg>
```

### 5. Leadership Engine — Compass

```html
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="9" stroke="#ffffff" stroke-width="2"/>
  <path d="M15.5 8.5l-2 5-5 2 2-5 5-2z" fill="#ffffff"/>
</svg>
```

---

## Platform Icons (used by content-visual-builder; included for plugin consistency)

### LinkedIn

```html
<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
  <path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.63-1.85 3.36-1.85 3.59 0 4.25 2.37 4.25 5.45v6.29zM5.34 7.44a2.06 2.06 0 110-4.13 2.06 2.06 0 010 4.13zM3.56 20.45h3.56V9H3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/>
</svg>
```

### X (Twitter)

```html
<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117L17.083 19.77z"/>
</svg>
```

### Instagram (solid, not gradient — gradient applied via CSS on container)

```html
<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
</svg>
```

### Newsletter — Envelope

```html
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <rect x="3" y="5" width="18" height="14" rx="2"/>
  <path d="M3 7l9 6 9-6"/>
</svg>
```

---

## Radial Score Meter (AI Visibility Card)

A 180×180 SVG showing a 0–100 score as an arc. Uses `stroke-dasharray` math to render the filled portion.

### Template

```html
<svg width="180" height="180" viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg">
  <!-- Background track -->
  <circle cx="90" cy="90" r="72" fill="none" stroke="#e8e2d8" stroke-width="12" stroke-linecap="round" transform="rotate(-90 90 90)"/>

  <!-- Filled arc (stroke-dasharray = circumference × (score / 100) ; gap = circumference × (1 - score/100)) -->
  <!-- Circumference ≈ 452.39 (2πr, r=72) -->
  <circle cx="90" cy="90" r="72" fill="none" stroke="#EAB308" stroke-width="12" stroke-linecap="round"
          stroke-dasharray="{{FILLED_LENGTH}} {{GAP_LENGTH}}"
          transform="rotate(-90 90 90)"/>

  <!-- Score text -->
  <text x="90" y="88" text-anchor="middle" font-family="Rethink Sans, Inter, sans-serif" font-size="48" font-weight="700" fill="#1a1a1a">{{SCORE}}</text>
  <text x="90" y="112" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#6b6b6b" letter-spacing="1">/ 100</text>
</svg>
```

### Calculation

For `{{SCORE}}` = integer 0–100:
- `{{FILLED_LENGTH}}` = `452.39 * (SCORE / 100)` rounded to 2 decimals
- `{{GAP_LENGTH}}` = `452.39 - FILLED_LENGTH`

Example: SCORE = 68 → FILLED_LENGTH = 307.63, GAP_LENGTH = 144.76

### Color variants by score

| Score range | Stroke color |
|-------------|--------------|
| 0–39 | `#DC2626` (engine-leadership red) |
| 40–69 | `#EAB308` (engine-cash gold) — default |
| 70–100 | `#22C55E` (engine-sales green) |

Swap the `stroke` on the filled arc accordingly.

---

## Decorative & Structural SVGs

### Thin Divider (horizontal rule alternative)

```html
<svg width="100%" height="2" viewBox="0 0 100 2" preserveAspectRatio="none">
  <line x1="0" y1="1" x2="100" y2="1" stroke="#e8e2d8" stroke-width="1"/>
</svg>
```

### Section Break (dotted)

Used between major sections in print-optimized mode:

```html
<svg width="100%" height="8" viewBox="0 0 200 8" preserveAspectRatio="none">
  <line x1="0" y1="4" x2="200" y2="4" stroke="#a8a39b" stroke-width="1" stroke-dasharray="2 4"/>
</svg>
```

### Red Underline Accent (Cover Hero)

```html
<svg width="48" height="3" viewBox="0 0 48 3" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="3" fill="#e90d41"/>
</svg>
```

---

## Primitive Shapes

### Filled Pill (badge background — use as container, not standalone)

Rendered via CSS `border-radius: 999px`, not SVG.

### Checkmark (done, rule)

```html
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 8l3.5 3.5L13 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### X Mark (banned, missing)

```html
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
```

### Arrow Right (CTA)

```html
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### Quote Mark (large, decorative for Pain Themes)

```html
<svg width="32" height="24" viewBox="0 0 32 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M8 24V12h6V4H4v8h2c0 6-4 8-4 8v4c6 0 8-4 8-4l-2-4z M24 24V12h6V4H20v8h2c0 6-4 8-4 8v4c6 0 8-4 8-4l-2-4z" fill="currentColor" opacity="0.15"/>
</svg>
```

### Spinner (loading, interactive mode only — never in static render)

```html
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="spin">
  <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-dasharray="24" stroke-dashoffset="0"/>
</svg>
<style>
.spin { animation: spin 800ms linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

---

## Placeholder Avatar (when no headshot provided)

When `{{BRAIN_HEADSHOT}}` is missing, render initials in a filled circle:

```html
<svg width="96" height="96" viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">
  <circle cx="48" cy="48" r="48" fill="#fce8ed"/>
  <text x="48" y="58" text-anchor="middle" font-family="Rethink Sans, Inter, sans-serif" font-size="36" font-weight="700" fill="#e90d41">{{INITIALS}}</text>
</svg>
```

`{{INITIALS}}` = first letter of first word + first letter of last word, uppercased. Max 2 characters.

---

## Connector Lines (for Competitor Matrix — optional decorative)

If the matrix feels too boxy, drop a subtle connector line between competitor columns and the "gap to own" row:

```html
<svg width="100%" height="40" viewBox="0 0 300 40" preserveAspectRatio="none">
  <path d="M50 0 Q50 20 150 20 T250 40" fill="none" stroke="#e8e2d8" stroke-width="1" stroke-dasharray="3 3"/>
</svg>
```

Use sparingly — matrix is strong enough without.

---

## Brand Mark (Purely Personal signature — bottom-right of Cover)

```html
<svg width="28" height="28" viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">
  <rect width="28" height="28" rx="4" fill="#e90d41"/>
  <text x="14" y="19" text-anchor="middle" font-family="Rethink Sans, Inter, sans-serif" font-size="16" font-weight="700" fill="#ffffff">pp</text>
</svg>
```

---

## Usage Rules

1. **Inline every SVG.** Never use `<img src=".svg">` — breaks PDF export and offline rendering.
2. **Set explicit `width` and `height`** on the `<svg>` element. Don't rely on CSS alone for sizing (print treats undefined SVG sizes inconsistently).
3. **For engine icons inside badges,** the SVG's `width`/`height` is 22 but the parent circle is 44 — the 11px padding is load-bearing visual weight.
4. **For the radial meter,** always compute `{{FILLED_LENGTH}}` and `{{GAP_LENGTH}}` before emitting. Never leave math to render-time.
5. **Use `currentColor` aggressively.** It lets the icon inherit from parent text color, which simplifies theming.
6. **Never animate in static/print mode.** Spinner only in interactive mode, and even then only during actual pending states.

---

## Reusable Engine Icon Lookup

When filling `{{ENGINE_ICON_SVG}}` in templates, use this map:

```js
const ENGINE_ICONS = {
  marketing: /* megaphone svg above */,
  sales: /* target svg above */,
  operations: /* grid svg above */,
  cash: /* bar chart svg above */,
  leadership: /* compass svg above */
};
```

For the inverted variant (`{{ENGINE_ICON_SVG_WHITE}}` used on colored backgrounds), the SVGs above already use white fills — they are the inverted variant. For dark-text-on-light-background variant (used in Actions Panel cards with soft backgrounds), swap `fill="#ffffff"` → `fill="currentColor"` and set the parent's text color to the engine color.
