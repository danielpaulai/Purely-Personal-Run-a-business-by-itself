# Design System, AI CEO Brain
# Purely Personal · by Daniel Paul

---

## CLIENT COLOR OVERRIDE, READ FIRST

Before building any HTML output:
1. Check if user has provided brand colors (they may say "my colors are #hex" or paste a brand doc)
2. If YES → replace `--primary: #E8294C` and `--primary-rgb: 232,41,76` with their values
3. If NO → use Purely Personal red `#E8294C` throughout

---

## Brand Tokens

```css
:root {
  /* PRIMARY, Purely Personal Red (override with client colors) */
  --primary:        #E8294C;
  --primary-dark:   #C4203D;
  --primary-light:  #F5607A;
  --primary-rgb:    232, 41, 76;

  /* SURFACES */
  --bg:             #0A0A0A;
  --bg-card:        #111111;
  --bg-card-2:      #181818;
  --bg-card-3:      #1F1F1F;

  /* BORDERS */
  --border:         rgba(255,255,255,0.07);
  --border-2:       rgba(255,255,255,0.13);

  /* TEXT */
  --text:           #FFFFFF;
  --text-2:         rgba(255,255,255,0.58);
  --text-3:         rgba(255,255,255,0.28);

  /* STATUS */
  --green:          #22C55E;
  --green-bg:       rgba(34,197,94,0.10);
  --amber:          #F59E0B;
  --amber-bg:       rgba(245,158,11,0.10);
  --red-status:     #EF4444;
  --red-status-bg:  rgba(239,68,68,0.10);

  /* TYPOGRAPHY */
  --font-display:   'Playfair Display', Georgia, serif;
  --font-body:      'Poppins', system-ui, sans-serif;
  --font-mono:      'DM Mono', monospace;

  /* RADIUS */
  --r-sm:  8px;
  --r-md:  16px;
  --r-lg:  24px;
  --r-pill: 9999px;

  /* SHADOWS */
  --shadow-card:  0 4px 24px rgba(0,0,0,0.45);
  --shadow-glow:  0 0 40px rgba(232,41,76,0.22);
  --shadow-lift:  0 16px 48px rgba(0,0,0,0.6);
}
```

---

## Google Fonts Import

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Poppins:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
```

| Font | Role |
|------|------|
| Playfair Display | Hero headings, section titles, cover numbers |
| Poppins | All body copy, labels, action steps, UI |
| DM Mono | Pillar badges, tags, metadata, code |

---

## Base CSS Reset + Body

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font-body);
  background: var(--bg);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
  padding: 40px 32px 80px;
  max-width: 820px;
  margin: 0 auto;
}
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-card); }
::-webkit-scrollbar-thumb { background: rgba(232,41,76,0.4); border-radius: 3px; }
::selection { background: rgba(232,41,76,0.25); }
```

---

## Section Label

```css
.sec-label {
  font-family: var(--font-mono);
  font-size: 11px; font-weight: 500;
  letter-spacing: .12em; text-transform: uppercase;
  color: var(--primary); margin-bottom: 16px;
  display: flex; align-items: center; gap: 10px;
}
.sec-label::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}
```

---

## Card Components

```css
/* Standard card */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 24px 28px;
  margin-bottom: 14px;
}
/* Accented, red left border */
.card--accent {
  border-left: 3px solid var(--primary);
}
/* Dark variant */
.card--dark {
  background: var(--bg-card-2);
}
/* Action card, red tint */
.card--action {
  background: rgba(var(--primary-rgb), 0.07);
  border: 1px solid rgba(var(--primary-rgb), 0.25);
  border-radius: var(--r-lg);
  padding: 24px 28px;
}

/* Card label */
.card__label {
  font-family: var(--font-mono);
  font-size: 10px; font-weight: 500;
  letter-spacing: .12em; text-transform: uppercase;
  color: var(--primary); margin-bottom: 10px;
}
/* Card heading */
.card__title {
  font-family: var(--font-display);
  font-size: 20px; font-weight: 800;
  letter-spacing: -.01em; margin-bottom: 10px; color: var(--text);
}
/* Card body */
.card__body {
  font-family: var(--font-body);
  font-size: 14px; line-height: 1.8; color: var(--text-2);
}
```

---

## Pillar Badge

```css
.pillar-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 10px; font-weight: 500;
  letter-spacing: .1em; text-transform: uppercase;
  color: var(--primary);
  background: rgba(var(--primary-rgb), 0.10);
  border: 1px solid rgba(var(--primary-rgb), 0.25);
  padding: 4px 12px; border-radius: var(--r-pill);
  margin-bottom: 16px;
}
```

---

## Action Step List

```css
.action-list { list-style: none; }
.action-item {
  display: flex; gap: 14px; align-items: flex-start;
  padding: 12px 0; border-bottom: 1px solid var(--border);
}
.action-item:last-child { border-bottom: none; }
.action-num {
  font-family: var(--font-display);
  font-size: 20px; font-weight: 900; color: var(--primary);
  flex-shrink: 0; line-height: 1.2; min-width: 24px;
}
.action-text {
  font-family: var(--font-body);
  font-size: 14px; line-height: 1.7; color: var(--text);
}
```

---

## Monday Session Step Cards

```css
.step-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 20px 24px;
  margin-bottom: 12px;
  display: flex; gap: 16px; align-items: flex-start;
}
.step-badge {
  width: 36px; height: 36px; border-radius: 10px;
  background: rgba(var(--primary-rgb), 0.10);
  border: 1px solid rgba(var(--primary-rgb), 0.25);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-mono); font-size: 12px; color: var(--primary);
  flex-shrink: 0;
}
.step-content { flex: 1; }
.step-label {
  font-family: var(--font-mono);
  font-size: 10px; color: var(--text-3);
  letter-spacing: .1em; text-transform: uppercase; margin-bottom: 6px;
}
.step-value {
  font-family: var(--font-body);
  font-size: 14px; line-height: 1.7; color: var(--text);
}
```

---

## Footer

```css
footer {
  margin-top: 56px; padding-top: 24px;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between;
  align-items: center; flex-wrap: wrap; gap: 12px;
}
.footer__brand {
  font-family: var(--font-display);
  font-size: 18px; font-weight: 800; color: var(--primary);
}
.footer__by {
  font-family: var(--font-body);
  font-size: 13px; color: var(--text-3); margin-left: 8px;
}
.footer__meta {
  font-family: var(--font-mono);
  font-size: 11px; color: var(--text-3);
}
```

---

## Animations

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-up { opacity: 0; animation: fadeUp .45s ease forwards; }
.fd-1 { animation-delay: .05s; }
.fd-2 { animation-delay: .10s; }
.fd-3 { animation-delay: .15s; }
.fd-4 { animation-delay: .20s; }
.fd-5 { animation-delay: .25s; }
```

---

## PURELY PERSONAL BRAND IDENTITY SYSTEM

### The Full Visual Language

**Primary color:** `#E8294C`, Purely Personal Red
This is the brand's signature. It appears on:
- All CTA buttons and action elements
- Score rings and metric highlights
- Section labels and pillar badges
- Cover page accents and borders
- Footer brand name

**Typography hierarchy:**
```
DISPLAY (Playfair Display 700–900):
  Hero titles, cover headings, score numbers, section titles
  → "This is Danny's thinking. Not generic AI advice."

BODY (Poppins 300–800):
  All running text, labels, card content, descriptions
  → Clean, modern, highly readable at all sizes

MONO (DM Mono 400–500):
  Pillar badges, metadata, file names, version info
  → Technical precision, premium detail
```

**Dark surface system:**
```
Page background:   #0A0A0A (near-black)
Card level 1:      #111111 (primary card)
Card level 2:      #181818 (nested card)
Card level 3:      #1F1F1F (deep nested)
```

**Premium effects:**
- Radial gradient glow behind hero elements: `rgba(232,41,76,0.15)`
- Score ring filter: `drop-shadow(0 0 10px rgba(232,41,76,0.7))`
- Card hover: `border-color: rgba(255,255,255,0.13)`
- Button shadow: `0 8px 32px rgba(232,41,76,0.35)`

### Cover Page Standard

Every HTML output opens with a cover section:
```
Background: radial-gradient(ellipse at 60% 20%, rgba(232,41,76,0.16) 0%, transparent 65%), #0A0A0A
+ dot grid texture overlay (rgba(255,255,255,0.015))

Title: Playfair Display 900, clamp(36px, 5vw, 64px), letter-spacing -0.02em
Badge: Poppins 700, 11px, uppercase, letter-spacing 0.12em, red pill
Subtitle: Poppins 400, 15px, rgba(255,255,255,0.58)
```

### The One Rule

Every HTML output must look like a premium product.
Not a Claude output. Not a template. A product Daniel Paul would be proud to share.

If it doesn't feel premium, add:
1. The radial glow to the cover
2. The dot grid texture
3. Staggered fade-up animations on cards
4. Red left-border accent on the primary insight card
5. DM Mono for all metadata and labels

