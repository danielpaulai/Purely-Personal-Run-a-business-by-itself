# Output Modes — Engine Output Builder

Minimal page shells for each dimension. Each shell:
- Loads the shared Purely Personal design-system CSS (`:root` custom properties)
- Frames a single section from `business-brain-renderer`
- Adds a brand corner mark + optional footer
- Sets viewport so the HTML renders at the target dimension

**Rule:** every shell uses the same base CSS. Only the outer frame changes.

---

## Base Shell (shared across all dimensions)

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{SECTION_NAME}} — {{BRAIN_NAME}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&family=Rethink+Sans:wght@400;500;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --page-bg:#faf8f4; --card-bg:#ffffff; --sub-card-bg:#fbf9f6;
  --divider:#e8e2d8; --divider-strong:#d0cdc8;
  --text-primary:#1a1a1a; --text-secondary:#6b6b6b; --text-muted:#a8a39b;
  --pp-red:#e90d41; --pp-red-deep:#c70a38; --pp-red-soft:#fce8ed; --pp-red-whisper:#fdf2f5;
  --dark:#0f0f10; --dark-card:#1a1a1d;
  --engine-marketing:#3B82F6; --engine-sales:#22C55E;
  --engine-operations:#8B5CF6; --engine-cash:#EAB308; --engine-leadership:#DC2626;
  --engine-marketing-soft:#EBF2FE; --engine-sales-soft:#E8FAEE;
  --engine-operations-soft:#F1ECFD; --engine-cash-soft:#FCF5D9; --engine-leadership-soft:#FCE8E8;
  --display:'Rethink Sans','Inter',sans-serif;
  --body:'Inter',sans-serif;
  --mono:'JetBrains Mono',Menlo,monospace;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--page-bg);font-family:var(--body);color:var(--text-primary)}
.label{font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-secondary)}
.label-red{color:var(--pp-red)}
.title{font-family:var(--display);font-size:30px;font-weight:800;margin:0 0 6px;line-height:1.1;letter-spacing:-0.015em;color:var(--text-primary)}
.subtitle{font-size:15px;color:var(--text-secondary);margin:0 0 18px}
.big-stat{font-family:var(--display);font-weight:800;line-height:0.95;letter-spacing:-0.03em;font-feature-settings:'tnum'}

/* Brand corner mark (every standalone output has one) */
.brand-mark{position:absolute;bottom:20px;right:24px;display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;color:var(--text-muted);letter-spacing:0.08em;z-index:5}
.brand-mark .dot{width:18px;height:18px;background:var(--pp-red);border-radius:4px;display:flex;align-items:center;justify-content:center;color:#fff;font-family:var(--display);font-weight:800;font-size:10px}

@media print{
  html,body{background:#ffffff}
  .no-print{display:none!important}
}
</style>
</head>
<body>

<div class="frame">
  {{SECTION_TEMPLATE}}
  <div class="brand-mark"><div class="dot">pp</div> {{BRAIN_NAME}} · Business Brain</div>
</div>

</body>
</html>
```

---

## Shell: Square 1080×1080 (LinkedIn / Instagram / X square)

Best for: single-stat sections (Business $75K, AI Visibility meter, Brand identity, Pain hero quote).

```css
.frame {
  width: 1080px;
  height: 1080px;
  padding: 60px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  background: var(--page-bg);
  overflow: hidden;
}
.frame > *:not(.brand-mark) {
  width: 100%;
  max-width: 960px;
  max-height: 900px;
}
```

Rules:
- Inner content max 960×900 (leaves 60px margin)
- Section's internal card should have generous padding so the number or meter dominates
- For `Pain hero quote` in this format: the big dark card becomes the whole square — replace internal card padding with frame padding

---

## Shell: Portrait 1080×1350 (LinkedIn carousel / Instagram portrait)

Best for: rich-content sections (Voice card, ICP persona, Brand identity with breakdown).

```css
.frame {
  width: 1080px;
  height: 1350px;
  padding: 56px 60px;
  position: relative;
  background: var(--page-bg);
  overflow: hidden;
}
.frame > *:not(.brand-mark) {
  max-width: 100%;
}
```

Rules:
- Full vertical height available — sections render naturally without compression
- Add a top-of-page header strip (small brand mark + section number) for orientation:

```html
<div style="margin-bottom:32px;display:flex;justify-content:space-between;align-items:center">
  <div style="font-family:var(--mono);font-size:12px;color:var(--pp-red);letter-spacing:0.15em;font-weight:700;text-transform:uppercase">{{BRAIN_NAME}} · Business Brain</div>
  <div style="font-family:var(--mono);font-size:12px;color:var(--text-muted);letter-spacing:0.12em">{{SECTION_NUMBER}} / 09</div>
</div>
```

---

## Shell: Landscape 1200×628 (LinkedIn feed landscape / newsletter hero)

Best for: wide sections (Competitor 3×3, Proof Stats Band).

```css
.frame {
  width: 1200px;
  height: 628px;
  padding: 40px 48px;
  position: relative;
  background: var(--page-bg);
  overflow: hidden;
}
.frame > *:not(.brand-mark) {
  max-height: 548px;
}
```

Rules:
- Competitor 3×3 renders natively in this frame — 3 columns fit perfectly
- Proof Stats Band: remove the section's own `margin: 0 -32px` outer negatives — the frame IS the full-bleed
- Max internal height 548 (40px top + 40px bottom padding)

---

## Shell: X Landscape 1600×900

Best for: Competitor 3×3 on X threads, Proof Band wide.

```css
.frame {
  width: 1600px;
  height: 900px;
  padding: 48px 64px;
  position: relative;
  background: var(--page-bg);
  overflow: hidden;
}
```

Same rules as 1200×628 but scaled up. Prefer this over 1200×628 if the section has dense content (Competitor matrix with long gap-text benefits from the extra width).

---

## Shell: A4 Print (for PDF handout)

```css
@page { size: A4 portrait; margin: 0 }
.frame {
  width: 595pt;
  min-height: 842pt;
  padding: 48pt 56pt;
  position: relative;
  background: #ffffff;
}
```

Rules:
- Background forced to white (ink-saving)
- Padding in pt not px (print-appropriate)
- No screenshots of this format — user hits Cmd+P → Save as PDF

---

## Per-Section Format Preferences

| Section | Best format | Reason |
|---------|-------------|--------|
| Voice card | Portrait 1080×1350 | 2-column layout needs vertical room |
| Business card | Square 1080×1080 | The $75K stat card dominates and pops |
| ICP persona | Portrait 1080×1350 | 3-column pain/desire/objection needs height |
| Competitor 3×3 | Landscape 1200×628 or X 1600×900 | Natively 3-column, width-friendly |
| Brand identity | Square 1080×1080 | 2-column layout fits square well |
| AI visibility | Square 1080×1080 | Big radial meter is the hero |
| Pain hero quote | Square 1080×1080 | Dark card becomes the whole graphic |
| Proof stats band | Landscape 1200×628 | Already full-bleed horizontal |

If user doesn't specify format: use the "best" column.

---

## Brand Corner Mark (all shells)

Every shell includes this block at bottom-right. It's the attribution stamp — without it, the image is orphaned.

```html
<div class="brand-mark">
  <div class="dot">pp</div>
  {{BRAIN_NAME}} · Business Brain
</div>
```

For landscape shells, can also go bottom-center. For portrait, always bottom-right.

**Never omit the brand mark.** Standalone images without attribution look like random stock graphics.

---

## Tuning: Square Format Gotchas

Square (1080×1080) compresses vertical space. Some sections need padding/sizing tweaks to fit:

- **Voice card:** 2-column may crunch; prefer portrait instead OR show only banned + hooks (drop examples)
- **ICP card:** 3-column pain/desire/objection compresses; prefer portrait OR reduce to 2-column (pain + desire only)
- **Pain hero:** expand the inner dark card to fill the square — the hero quote card becomes the graphic itself

Rule of thumb: **if in doubt, go portrait.** Portrait is more flexible and LinkedIn rewards taller assets.

---

## Anti-patterns

- ❌ Don't render at screen density (2×, 3×). Always 1× (72dpi). Platforms don't re-scale.
- ❌ Don't rely on responsive CSS inside the shell. The dimensions are fixed (1080×1080, etc.) — the content must fit deterministically.
- ❌ Don't add interactive elements (editable fields, PDF export button) to standalone outputs. These are static image assets.
- ❌ Don't generate multiple formats at once unless explicitly asked. One call = one output.
- ❌ Don't cut off content. If a section doesn't fit at the requested format, pick a taller/wider format, don't truncate.
