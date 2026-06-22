# Design System — Purely Personal Brand Tokens
# by Daniel Paul · Purely Personal

---

## Primary Brand Colors

```css
:root {
  /* ── PURELY PERSONAL BRAND ─────────────────────── */
  --primary:        #E8294C;   /* Purely Personal Red — primary CTAs, headings, badges */
  --primary-dark:   #C4203D;   /* Darker red — hover states */
  --primary-light:  #F5607A;   /* Lighter red — tints, soft accents */
  --primary-rgb:    232, 41, 76;

  --black:          #0A0A0A;   /* Near-black — dark backgrounds, strong text */
  --white:          #FFFFFF;   /* Pure white — card backgrounds, text on dark */
  --off-white:      #F8F7F5;   /* Warm off-white — page background */
  --gray:           #E4E3E0;   /* Light gray — dividers, borders */
  --gray-text:      #555555;   /* Medium gray — secondary copy */
  --gray-light:     #F2F1EE;   /* Very light gray — alt section backgrounds */

  /* ── SCORE INDICATORS ───────────────────────────── */
  --score-high:     #16A34A;   /* Green — strong scores (8–10) */
  --score-mid:      #D97706;   /* Amber — mid scores (5–7) */
  --score-low:      #DC2626;   /* Red — weak scores (1–4) */

  /* ── TYPOGRAPHY ─────────────────────────────────── */
  --font-heading:   'Rethink Sans', sans-serif;
  --font-body:      'Rethink Sans', sans-serif;

  /* ── RADIUS ─────────────────────────────────────── */
  --radius-sm:      8px;
  --radius-md:      16px;
  --radius-lg:      28px;
  --radius-pill:    9999px;

  /* ── SHADOWS ─────────────────────────────────────── */
  --shadow-primary: 0 8px 32px rgba(232,41,76,0.22);
  --shadow-card:    0 4px 24px rgba(0,0,0,0.07);
  --shadow-lift:    0 12px 48px rgba(0,0,0,0.13);
}
```

---

## Color Usage Guide

| Token | Hex | Use For |
|-------|-----|---------|
| `--primary` | `#E8294C` | CTA buttons, score badges, section accents, cover ring |
| `--primary-dark` | `#C4203D` | Hover states on buttons |
| `--primary-light` | `#F5607A` | Tinted backgrounds, soft highlights |
| `--black` | `#0A0A0A` | Cover page bg, report headers, strong headings |
| `--white` | `#FFFFFF` | Card backgrounds, text on dark surfaces |
| `--off-white` | `#F8F7F5` | Page background, alternating sections |

---

## HTML Report Standard Structure

Every HTML report produced by any Purely Personal skill follows this layout:

```
Cover page (black bg, red ring, Rethink Sans heading)
  ↓
Tab navigation (red active state)
  ↓
Section cards (white bg, shadow-card, 28px radius)
  ↓
Score badges (red = primary metric, green/amber/red = performance)
  ↓
CTA footer (red button, Purely Personal branding)
```

---

## Typography Rules

- All headings: Rethink Sans, font-weight 700 or 800
- Body copy: Rethink Sans, font-weight 400, line-height 1.7
- Monospace/code: DM Mono or system monospace
- Never use system-ui or Arial for Purely Personal output

---

## Branding Footer (every HTML report)

```html
<footer>
  <p>Built by <strong>Daniel Paul</strong> · <a href="https://purelypersonal.com">Purely Personal</a></p>
  <p style="color:var(--gray-text);font-size:12px">
    © Purely Personal. All rights reserved.
  </p>
</footer>
```

---

## The One Rule

Everything Purely Personal produces must look like a premium product.
Not a Claude output. Not a template. A product.

If Daniel Paul saw this and it looked like AI made it — rebuild it.
