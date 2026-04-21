# Code Templates — Business Brain Renderer

Production-ready HTML/CSS templates with `{{VARIABLE}}` placeholders. Copy the template, replace variables, deliver. **Do NOT reconstruct from memory.** Every template was engineered against the design system — deviation breaks the visual language.

---

## Template #0: Base Page Wrapper

Every Business Brain render uses this wrapper. Drop all section templates inside `<main>`.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{BRAIN_NAME}} — Business Brain</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Rethink+Sans:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --page-bg:#faf8f4; --card-bg:#ffffff; --sub-card-bg:#fbf9f6;
  --divider:#e8e2d8; --divider-strong:#d0cdc8;
  --text-primary:#1a1a1a; --text-secondary:#6b6b6b; --text-muted:#a8a39b;
  --pp-red:#e90d41; --pp-red-deep:#c70a38; --pp-red-soft:#fce8ed;
  --engine-marketing:#3B82F6; --engine-sales:#22C55E;
  --engine-operations:#8B5CF6; --engine-cash:#EAB308; --engine-leadership:#DC2626;
  --engine-marketing-soft:#EBF2FE; --engine-sales-soft:#E8FAEE;
  --engine-operations-soft:#F1ECFD; --engine-cash-soft:#FCF5D9; --engine-leadership-soft:#FCE8E8;
  --display:'Rethink Sans','Inter',-apple-system,sans-serif;
  --body:'Inter',-apple-system,sans-serif;
  --mono:'JetBrains Mono','SF Mono',Menlo,monospace;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--page-bg); color:var(--text-primary);
  font-family:var(--body); font-size:15px; line-height:1.55;
  -webkit-font-smoothing:antialiased;
}
main{max-width:960px;margin:0 auto;padding:48px 32px 96px}
@media (max-width:768px){
  main{padding:32px 20px 72px}
  .card{padding:20px 22px}
}
@media (max-width:640px){
  .brain-toolbar{top:auto;bottom:12px;right:12px;left:12px;justify-content:flex-end}
}
.card{
  background:var(--card-bg); border:1px solid var(--divider); border-radius:4px;
  padding:28px 32px; margin-bottom:32px;
  box-shadow:0 1px 2px rgba(20,14,8,0.04);
}
.label{
  font-size:11px; font-weight:600; letter-spacing:0.06em;
  text-transform:uppercase; color:var(--text-secondary);
}
.title{
  font-family:var(--display); font-size:28px; font-weight:700;
  margin:0 0 6px; line-height:1.15; color:var(--text-primary);
}
.subtitle{font-size:15px;color:var(--text-secondary);margin:0 0 20px}
.divider{height:1px;background:var(--divider);border:0;margin:20px 0}
@media print{
  :root{--page-bg:#ffffff}
  body{background:#ffffff}
  .no-print{display:none!important}
  .card{box-shadow:none;break-inside:avoid}
  .page-break{page-break-after:always}
}
</style>
</head>
<body>
<main>

<!-- NOTE: the {{SECTION_N_*}} tokens below are SLOTS, not string variables. -->
<!-- V3 adds the Proof Stats Band between Cover and Voice — it's the first dark drumbeat. -->
<!-- Fixed order. Every full Brain renders all of these. -->

{{SECTION_1_COVER_HERO}}
{{SECTION_1_5_PROOF_STATS_BAND}}
{{SECTION_2_VOICE_CARD}}
{{SECTION_3_BUSINESS_CARD}}
{{SECTION_4_ICP_CARD}}
{{SECTION_5_COMPETITOR_MATRIX}}
{{SECTION_6_BRAND_CARD}}
{{SECTION_7_AI_VISIBILITY}}
{{SECTION_8_PAIN_THEMES}}
{{SECTION_9_ACTIONS_PANEL}}
{{FOOTER}}

{{INTERACTIVE_SCRIPTS}}
</main>
</body>
</html>
```

---

## Template #1: Cover Hero (V3 — cinematic + asymmetric)

Full-bleed top section. Cream→white gradient background with soft red radial glows in corners. Tilted `Ch. 01 / 09` stamp top-right. Date tick top-left. Larger headshot (128px). Hero name at 72px weight 800. 64px engine badges with colored shadows.

```html
<section style="text-align:center;padding:64px 24px 56px;margin:0 -32px 0;background:linear-gradient(180deg, #ffffff 0%, #fbf9f6 100%);border-bottom:1px solid var(--divider);position:relative;overflow:hidden">

  <!-- Background radial glows -->
  <div style="position:absolute;top:-100px;left:-100px;width:300px;height:300px;background:radial-gradient(circle, rgba(233,13,65,0.05) 0%, transparent 70%);pointer-events:none"></div>
  <div style="position:absolute;bottom:-80px;right:-80px;width:260px;height:260px;background:radial-gradient(circle, rgba(233,13,65,0.04) 0%, transparent 70%);pointer-events:none"></div>

  <!-- ASYMMETRIC: tilted chapter stamp top-right -->
  <div style="position:absolute;top:24px;right:32px;transform:rotate(8deg);padding:6px 12px;border:1.5px solid var(--pp-red);background:var(--pp-red-soft);color:var(--pp-red-deep);font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;pointer-events:none">
    Ch. 01 <span style="color:var(--text-muted);font-weight:500">/ 09</span>
  </div>

  <!-- ASYMMETRIC: date tick top-left -->
  <div style="position:absolute;top:32px;left:32px;font-family:var(--mono);font-size:10px;color:var(--text-muted);letter-spacing:0.1em;pointer-events:none">
    <div style="width:32px;height:1px;background:var(--pp-red);margin-bottom:6px"></div>
    {{BRAIN_DATE_SHORT}}
  </div>

  <!-- Editorial brand mark -->
  <div style="font-family:var(--mono);font-size:11px;color:var(--pp-red);letter-spacing:0.2em;text-transform:uppercase;font-weight:700;margin-bottom:32px">— Business Brain —</div>

  <!-- 128px headshot with red glow -->
  <div style="width:128px;height:128px;border-radius:999px;overflow:hidden;margin:0 auto 24px;box-shadow:0 8px 32px rgba(233,13,65,0.15);position:relative">
    <img src="{{BRAIN_HEADSHOT}}" alt="{{BRAIN_NAME}}" style="width:100%;height:100%;object-fit:cover">
  </div>

  <!-- 72px hero name -->
  <h1 style="font-family:var(--display);font-size:72px;font-weight:800;margin:0 0 12px;letter-spacing:-0.03em;line-height:0.95">{{BRAIN_NAME}}</h1>

  <!-- 22px tagline -->
  <p style="font-size:22px;color:var(--text-secondary);margin:0 auto 28px;max-width:620px;line-height:1.4;font-weight:400">{{BRAIN_TAGLINE}}</p>

  <!-- Bold red underline -->
  <div style="width:64px;height:4px;background:var(--pp-red);margin:0 auto 36px;border-radius:2px"></div>

  <!-- 5 engine badges @ 64px -->
  <div style="display:flex;gap:24px;justify-content:center;flex-wrap:wrap;margin-bottom:28px">
    {{ENGINE_BADGES}}
  </div>

  <!-- Meta line -->
  <div style="font-size:12px;color:var(--text-muted);letter-spacing:0.06em;font-family:var(--mono)">
    {{BRAIN_DATE}} · <span style="color:var(--pp-red);font-weight:700">{{BRAND_NAME}}</span>
  </div>
</section>
```

### Engine Badge Sub-Template (V3 — 64px with colored shadow)

Repeat 5 times inside `{{ENGINE_BADGES}}`:

```html
<div style="display:flex;flex-direction:column;align-items:center;gap:8px">
  <div style="width:64px;height:64px;border-radius:999px;background:var({{ENGINE_VAR}});display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px {{ENGINE_SHADOW}}">
    {{ENGINE_ICON_SVG_32PX}}
  </div>
  <div class="label" style="font-size:10px;font-weight:700">{{ENGINE_NAME}}</div>
</div>
```

With per-engine variables:

| Engine | `{{ENGINE_VAR}}` | `{{ENGINE_SHADOW}}` |
|--------|------------------|---------------------|
| Marketing | `--engine-marketing` | `rgba(59,130,246,0.28)` |
| Sales | `--engine-sales` | `rgba(34,197,94,0.28)` |
| Operations | `--engine-operations` | `rgba(139,92,246,0.28)` |
| Cash | `--engine-cash` | `rgba(234,179,8,0.32)` |
| Leadership | `--engine-leadership` | `rgba(220,38,38,0.28)` |

Icons: 32px from [references/svg-primitives.md].

---

## Template #1.5: Proof Stats Band (V3 — NEW)

**Full-bleed dark band between Cover and Voice card.** This is the page's first drumbeat — without it the render feels flat. Three big stats, dark charcoal background, red accents, full-bleed with 3px red bottom border.

Data source: pulled from the user's Brain (Business section + observed results). Examples: `$0` monthly cost, `2hr/wk` time on X, `5` engines running.

```html
<section style="background:var(--dark);color:#fff;margin:0 -32px 32px;padding:40px 32px;border-bottom:3px solid var(--pp-red);position:relative;overflow:hidden">

  <!-- Corner marks -->
  <div style="position:absolute;top:14px;left:24px;font-family:var(--mono);font-size:10px;color:var(--pp-red);letter-spacing:0.15em;font-weight:700">◆ PROOF</div>
  <div style="position:absolute;top:14px;right:24px;font-family:var(--mono);font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:0.15em">01 · 02 · 03</div>

  <div style="max-width:960px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:32px;padding-top:12px">

    <!-- Stat 1 -->
    <div style="text-align:center;padding:0 12px;position:relative">
      <div style="font-family:var(--mono);font-size:10px;color:var(--pp-red);letter-spacing:0.15em;font-weight:700;margin-bottom:8px;text-transform:uppercase">{{STAT_1_LABEL}}</div>
      <div class="big-stat" style="font-size:88px;color:#ffffff;margin-bottom:6px">{{STAT_1_VALUE}}</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.4">{{STAT_1_CAPTION}}</div>
      <div style="position:absolute;top:10%;right:-16px;bottom:10%;width:1px;background:rgba(255,255,255,0.12)"></div>
    </div>

    <!-- Stat 2 -->
    <div style="text-align:center;padding:0 12px;position:relative">
      <div style="font-family:var(--mono);font-size:10px;color:var(--pp-red);letter-spacing:0.15em;font-weight:700;margin-bottom:8px;text-transform:uppercase">{{STAT_2_LABEL}}</div>
      <div class="big-stat" style="font-size:88px;color:#ffffff;margin-bottom:6px">{{STAT_2_VALUE}}</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.4">{{STAT_2_CAPTION}}</div>
      <div style="position:absolute;top:10%;right:-16px;bottom:10%;width:1px;background:rgba(255,255,255,0.12)"></div>
    </div>

    <!-- Stat 3 -->
    <div style="text-align:center;padding:0 12px">
      <div style="font-family:var(--mono);font-size:10px;color:var(--pp-red);letter-spacing:0.15em;font-weight:700;margin-bottom:8px;text-transform:uppercase">{{STAT_3_LABEL}}</div>
      <div class="big-stat" style="font-size:88px;color:#ffffff;margin-bottom:6px">{{STAT_3_VALUE}}</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.4">{{STAT_3_CAPTION}}</div>
    </div>

  </div>
</section>
```

### Value formatting

For values with units, split size: full size for number, 60% size for unit. Example: `2hr/wk`:
```html
<div class="big-stat" style="font-size:88px">2hr<span style="font-size:56px;opacity:0.6">/wk</span></div>
```

### Stat composition rule

Pick 3 proof stats from the Brain:
- **Stat 1**: a cost the user saved or avoided ($0, $499/mo eliminated)
- **Stat 2**: a time saved (2hr/wk from 12, 15min/day from 2hr)
- **Stat 3**: a quantity of the product working (5 engines, 47 skills, 3 engines always-on)

If no genuine proof stats exist in the Brain, render the empty state card instead. Never fabricate proof.

---

## Template #2: Voice Card

2-column card. Left: tone + banned phrases. Right: hook patterns + example posts.

```html
<section class="card" data-engine="marketing">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <div style="width:8px;height:24px;background:var(--engine-marketing);border-radius:2px"></div>
    <div class="label">01 · Voice</div>
  </div>
  <h2 class="title">How {{BRAIN_NAME}} Writes</h2>
  <p class="subtitle">{{VOICE_TONE}}</p>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:24px">

    <!-- LEFT: Banned + Rules -->
    <div>
      <div class="label" style="margin-bottom:10px">Banned phrases</div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:20px">
        {{BANNED_PHRASE_PILLS}}
      </div>

      <div class="label" style="margin-bottom:10px">Voice rules</div>
      <ul style="margin:0;padding-left:20px;font-size:14px;line-height:1.7">
        {{VOICE_RULES_LIST}}
      </ul>
    </div>

    <!-- RIGHT: Hooks + Examples -->
    <div>
      <div class="label" style="margin-bottom:10px">Hook patterns</div>
      <ol style="margin:0 0 20px;padding-left:20px;font-size:14px;line-height:1.7">
        {{HOOK_PATTERNS_LIST}}
      </ol>

      <div class="label" style="margin-bottom:10px">Example openings</div>
      <div style="display:flex;flex-direction:column;gap:10px">
        {{EXAMPLE_POSTS_CARDS}}
      </div>
    </div>

  </div>
</section>
```

### Banned Phrase Pill Sub-Template

```html
<span style="display:inline-block;padding:4px 10px;background:var(--pp-red-soft);color:var(--pp-red-deep);border-radius:999px;font-size:12px;font-weight:500;font-family:var(--mono)">{{PHRASE}}</span>
```

### Example Post Card Sub-Template

```html
<div style="padding:12px 14px;background:var(--sub-card-bg);border-left:3px solid var(--engine-marketing);font-size:13px;line-height:1.6">
  "{{POST_EXCERPT}}"
</div>
```

---

## Template #3: Business Card

2-column card. Left: offer + positioning. Right: 90-day goal + key metric.

```html
<section class="card">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <div style="width:8px;height:24px;background:var(--engine-leadership);border-radius:2px"></div>
    <div class="label">02 · Business</div>
  </div>
  <h2 class="title">What {{BRAIN_NAME}} Sells</h2>

  <div style="display:grid;grid-template-columns:1.4fr 1fr;gap:32px;margin-top:20px">

    <!-- LEFT: Offer + Positioning + Pricing -->
    <div>
      <div class="label" style="margin-bottom:8px">Offer</div>
      <p style="font-family:var(--display);font-size:22px;font-weight:700;margin:0 0 20px;line-height:1.3">{{OFFER}}</p>

      <div class="label" style="margin-bottom:8px">Positioning</div>
      <p style="font-size:15px;margin:0 0 20px;color:var(--text-secondary);line-height:1.55">{{POSITIONING}}</p>

      <div class="label" style="margin-bottom:8px">Pricing</div>
      <p style="font-family:var(--mono);font-size:15px;margin:0">{{PRICING}}</p>
    </div>

    <!-- RIGHT: 90-Day Goal + Key Metric -->
    <div style="background:var(--sub-card-bg);border-left:3px solid var(--engine-leadership);padding:16px 18px">
      <div class="label" style="margin-bottom:8px">90-Day Goal</div>
      <p style="font-size:14px;margin:0 0 16px;line-height:1.55">{{GOAL_90D}}</p>

      <div class="label" style="margin-bottom:8px">Key Metric</div>
      <div style="font-family:var(--display);font-size:40px;font-weight:700;line-height:1;font-feature-settings:'tnum'">{{KEY_METRIC_VALUE}}</div>
      <div style="font-size:12px;color:var(--text-secondary);margin-top:4px">{{KEY_METRIC_LABEL}}</div>
    </div>

  </div>
</section>
```

---

## Template #4: ICP Persona Card

Full-width card. Big persona header, then pain/desire/objection in 3 columns.

```html
<section class="card">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <div style="width:8px;height:24px;background:var(--engine-sales);border-radius:2px"></div>
    <div class="label">03 · Ideal Client</div>
  </div>
  <h2 class="title">Who {{BRAIN_NAME}} Serves</h2>

  <!-- Persona header strip -->
  <div style="display:flex;align-items:center;gap:16px;padding:16px 18px;background:var(--engine-sales-soft);border-radius:4px;margin:20px 0 24px">
    <div style="width:44px;height:44px;border-radius:999px;background:var(--engine-sales);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;font-family:var(--display)">{{ICP_INITIAL}}</div>
    <div>
      <div style="font-family:var(--display);font-size:18px;font-weight:700">{{ICP_NAME}}</div>
      <div style="font-size:13px;color:var(--text-secondary);margin-top:2px">Hangs out at: {{ICP_WHERE}}</div>
    </div>
  </div>

  <!-- 3-column: Pain / Desire / Objection -->
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;border-top:1px solid var(--divider);padding-top:20px">

    <div>
      <div class="label" style="margin-bottom:10px;color:var(--engine-leadership)">Pain</div>
      <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.7">
        {{ICP_PAIN_LIST}}
      </ul>
    </div>

    <div>
      <div class="label" style="margin-bottom:10px;color:var(--engine-sales)">Desire</div>
      <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.7">
        {{ICP_DESIRE_LIST}}
      </ul>
    </div>

    <div>
      <div class="label" style="margin-bottom:10px;color:var(--engine-cash)">Objection</div>
      <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.7">
        {{ICP_OBJECTIONS_LIST}}
      </ul>
    </div>

  </div>
</section>
```

---

## Template #5: Competitor 3×3 Matrix

Full-width card. Three columns (one per competitor), three rows (name, positioning, gap/angle).

```html
<section class="card">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <div style="width:8px;height:24px;background:var(--engine-operations);border-radius:2px"></div>
    <div class="label">04 · Competitors</div>
  </div>
  <h2 class="title">Who {{BRAIN_NAME}} Competes With</h2>
  <p class="subtitle">Top 3 competitors and the positioning gaps to own</p>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;border:1px solid var(--divider);margin-top:20px">
    {{COMPETITOR_COLUMNS}}
  </div>

</section>
```

### Competitor Column Sub-Template (repeat 3×)

```html
<div style="border-right:1px solid var(--divider);padding:18px;display:flex;flex-direction:column;gap:16px">

  <!-- Row 1: Name + Logo -->
  <div>
    <div class="label" style="margin-bottom:6px">Competitor</div>
    <div style="font-family:var(--display);font-size:18px;font-weight:700">{{COMP_NAME}}</div>
    <div style="font-size:12px;color:var(--text-muted);margin-top:2px;font-family:var(--mono)">{{COMP_URL}}</div>
  </div>

  <!-- Row 2: Their Positioning -->
  <div style="padding-top:14px;border-top:1px solid var(--divider)">
    <div class="label" style="margin-bottom:6px">Their angle</div>
    <p style="font-size:13px;margin:0;line-height:1.55;color:var(--text-secondary)">{{COMP_POSITIONING}}</p>
  </div>

  <!-- Row 3: Gap / Your Angle -->
  <div style="padding:12px;background:var(--engine-operations-soft);border-left:3px solid var(--engine-operations);margin-top:auto">
    <div class="label" style="margin-bottom:6px;color:var(--engine-operations)">Gap to own</div>
    <p style="font-size:13px;margin:0;font-weight:500;line-height:1.5">{{COMP_GAP}}</p>
  </div>

</div>
```

**Note:** last column removes `border-right`. Apply `style="border-right:0"` to the third column's outer `<div>`.

---

## Template #6: Brand Identity Card

2-column card. Left: color swatches. Right: typography + visual voice.

```html
<section class="card">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <div style="width:8px;height:24px;background:var(--pp-red);border-radius:2px"></div>
    <div class="label">05 · Brand Identity</div>
  </div>
  <h2 class="title">How {{BRAIN_NAME}} Looks</h2>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:20px">

    <!-- LEFT: Color Palette -->
    <div>
      <div class="label" style="margin-bottom:12px">Color palette</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">
        {{COLOR_SWATCHES}}
      </div>
    </div>

    <!-- RIGHT: Typography + Voice -->
    <div>
      <div class="label" style="margin-bottom:10px">Typography</div>
      <div style="margin-bottom:16px">
        <div style="font-family:var(--display);font-size:24px;font-weight:700;line-height:1.1">{{BRAND_DISPLAY_FONT}}</div>
        <div style="font-size:12px;color:var(--text-muted);font-family:var(--mono)">Display · Aa Bb Cc 0 1 2</div>
      </div>
      <div>
        <div style="font-family:var(--body);font-size:16px;font-weight:400;line-height:1.4">{{BRAND_BODY_FONT}}</div>
        <div style="font-size:12px;color:var(--text-muted);font-family:var(--mono)">Body · Aa Bb Cc 0 1 2</div>
      </div>

      <hr class="divider">

      <div class="label" style="margin-bottom:8px">Visual voice</div>
      <p style="font-size:14px;margin:0;line-height:1.55">{{BRAND_VISUAL_VOICE}}</p>
    </div>

  </div>
</section>
```

### Color Swatch Sub-Template

```html
<div style="display:flex;flex-direction:column;gap:4px">
  <div style="aspect-ratio:1;background:{{COLOR_HEX}};border:1px solid var(--divider);border-radius:4px"></div>
  <div style="font-size:10px;font-family:var(--mono);color:var(--text-muted)">{{COLOR_HEX}}</div>
</div>
```

---

## Template #7: AI Visibility Scorecard

Full-width card. Big radial meter on left, gap queries list on right.

```html
<section class="card">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <div style="width:8px;height:24px;background:var(--engine-cash);border-radius:2px"></div>
    <div class="label">06 · AI Visibility</div>
  </div>
  <h2 class="title">How AI Sees {{BRAIN_NAME}}</h2>
  <p class="subtitle">Your discoverability in ChatGPT, Perplexity, and Claude</p>

  <div style="display:grid;grid-template-columns:200px 1fr;gap:32px;margin-top:24px;align-items:center">

    <!-- LEFT: Radial meter (SVG from primitives) -->
    <div>
      {{RADIAL_METER_SVG}}
      <div style="text-align:center;font-size:12px;color:var(--text-muted);margin-top:8px">Visibility Score</div>
    </div>

    <!-- RIGHT: Gap queries -->
    <div>
      <div class="label" style="margin-bottom:12px">Queries where you don't rank</div>
      <div style="display:flex;flex-direction:column;gap:8px">
        {{GAP_QUERY_ROWS}}
      </div>
    </div>

  </div>
</section>
```

### Gap Query Row Sub-Template

```html
<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:var(--sub-card-bg);border-left:3px solid var(--engine-cash);font-size:13px">
  <span style="color:var(--engine-cash);font-weight:700">✗</span>
  <span style="font-family:var(--mono)">{{QUERY}}</span>
</div>
```

---

## Template #8: Pain Themes (V3 — hero quote + 3 small)

**Rhythm break.** One hero quote (most emotionally resonant) on a dark charcoal card + 3 smaller themes below in a 3-column grid. This is the second dark drumbeat of the page.

```html
<section class="card">
  <div class="section-numeral">07</div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
    <div style="width:8px;height:22px;background:var(--engine-sales);border-radius:2px"></div>
    <div class="label label-red">07 · Audience Pain</div>
  </div>
  <h2 class="title">What Your People Are Actually Saying</h2>
  <p class="subtitle">Real complaints. Real words. Pulled live.</p>

  <!-- HERO QUOTE (full-width dark card with giant quote mark) -->
  <div style="padding:32px 36px;background:linear-gradient(135deg, var(--dark) 0%, var(--dark-card) 100%);color:#fff;border-radius:8px;margin-top:20px;position:relative;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.15)">
    <div style="position:absolute;top:-16px;right:24px;font-family:var(--display);font-size:180px;color:var(--pp-red);opacity:0.25;line-height:0.7;font-weight:800;pointer-events:none">"</div>
    <div class="label" style="color:var(--pp-red);margin-bottom:14px;font-size:10px;font-weight:700">◆ TOP THEME · {{HERO_THEME_NAME}}</div>
    <p style="font-family:var(--display);font-size:28px;font-weight:700;line-height:1.3;margin:0 0 18px;color:#fff;font-style:italic;max-width:720px;position:relative;z-index:1">"{{HERO_VERBATIM}}"</p>
    <div style="display:flex;align-items:center;gap:10px;font-size:12px;color:rgba(255,255,255,0.6);font-family:var(--mono);letter-spacing:0.08em">
      <div style="width:24px;height:1px;background:var(--pp-red)"></div>
      <span>{{HERO_SOURCE_UPPERCASE}}</span>
    </div>
  </div>

  <!-- 3 SMALLER THEMES -->
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:14px">
    {{PAIN_THEME_SMALL_CARDS}}
  </div>
</section>
```

### Small Pain Theme Card Sub-Template (repeat 3×)

```html
<div style="padding:16px 18px;background:var(--sub-card-bg);border:1px solid var(--divider);border-radius:6px;position:relative">
  <div style="position:absolute;top:8px;right:14px;font-family:var(--display);font-size:44px;color:var(--pp-red);opacity:0.15;line-height:0.8;font-weight:800">"</div>
  <div class="label" style="margin-bottom:8px;color:var(--engine-sales);font-size:10px">{{THEME_NAME}}</div>
  <p style="font-size:13px;margin:0 0 8px;font-style:italic;line-height:1.5;color:var(--text-primary);position:relative;z-index:1">"{{VERBATIM_SHORT}}"</p>
  <div style="font-size:10px;color:var(--text-muted);font-family:var(--mono);letter-spacing:0.05em">— {{SOURCE}}</div>
</div>
```

### Theme picking rule

From the Brain's `{{PAIN_THEMES}}` array (typically 4–6):
- **Hero theme:** pick the MOST emotionally resonant — the one a reader will re-read. Typically the verbatim with raw personal detail ("...from 2022 when I wrote them angry in the car").
- **Three small themes:** pick the next 3 by topical variety. Don't pick 3 that all say "AI sounds generic" in different words.
- If fewer than 4 themes exist: render hero only, or hero + 2. Never pad with fabricated themes.

### Verbatim shortening rule

Small cards get SHORTER verbatims than the hero. If the source quote is >90 chars, trim to one punchy sentence. Edit only by cutting from start/end. Never paraphrase.

Example:
- **Full:** `"Taplio, Hypefury, Typefully, Buffer, Shield. I have so many tabs open my MacBook fan sounds like a jet."`
- **Shortened for small card:** `"Taplio, Hypefury, Typefully, Buffer. So many tabs my fan sounds like a jet."`

The `{{HERO_VERBATIM}}` never gets trimmed — full quote or nothing.

---

## Template #9: Actions Panel

Sticky-bottom or end-of-page card with 5 engine commands as clickable pills.

```html
<section class="card" style="border:2px solid var(--pp-red);background:var(--card-bg);position:relative">

  <div style="position:absolute;top:-10px;left:24px;background:var(--pp-red);color:#fff;padding:2px 10px;border-radius:4px;font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase">Take action</div>

  <h2 class="title" style="margin-top:4px">Run Your AI C-Suite</h2>
  <p class="subtitle">Each command below reads this Brain and acts in your voice</p>

  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:20px">
    {{ACTION_CARDS}}
  </div>

</section>
```

### Action Card Sub-Template (repeat 5×)

```html
<a href="#" onclick="return runCommand('{{COMMAND}}')" style="text-decoration:none;color:inherit;display:block">
  <div style="padding:16px 14px;background:var({{ENGINE_SOFT_VAR}});border:1px solid var({{ENGINE_VAR}});border-radius:6px;display:flex;flex-direction:column;gap:6px;transition:transform 120ms">

    <div style="width:32px;height:32px;border-radius:999px;background:var({{ENGINE_VAR}});display:flex;align-items:center;justify-content:center">
      {{ENGINE_ICON_SVG_WHITE}}
    </div>

    <div style="font-family:var(--display);font-size:14px;font-weight:700;line-height:1.2">{{ACTION_LABEL}}</div>
    <div style="font-family:var(--mono);font-size:11px;color:var({{ENGINE_VAR}});font-weight:500">{{COMMAND}}</div>

  </div>
</a>
```

With `{{ENGINE_VAR}}` / `{{ENGINE_SOFT_VAR}}` per engine:

| Engine | `--engine-{x}` | `--engine-{x}-soft` |
|---|---|---|
| Marketing | `--engine-marketing` | `--engine-marketing-soft` |
| Sales | `--engine-sales` | `--engine-sales-soft` |
| Operations | `--engine-operations` | `--engine-operations-soft` |
| Cash | `--engine-cash` | `--engine-cash-soft` |
| Leadership | `--engine-leadership` | `--engine-leadership-soft` |

---

## Template #10: Dashboard Strip (compact mode)

3-column horizontal strip. Use when embedding Brain summary at the top of a README or Notion page.

```html
<section style="max-width:1200px;margin:0 auto;padding:24px;background:var(--card-bg);border:1px solid var(--divider);border-radius:6px">
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px">

    <!-- Col 1: You + Voice -->
    <div>
      <div class="label" style="margin-bottom:6px">{{BRAIN_NAME}}</div>
      <div style="font-family:var(--display);font-size:16px;font-weight:700;line-height:1.2;margin-bottom:10px">{{BRAIN_TAGLINE}}</div>
      <div style="font-size:12px;color:var(--text-secondary);line-height:1.5">{{VOICE_SUMMARY}}</div>
    </div>

    <!-- Col 2: ICP + Offer -->
    <div style="border-left:1px solid var(--divider);border-right:1px solid var(--divider);padding:0 24px">
      <div class="label" style="margin-bottom:6px">Serves</div>
      <div style="font-family:var(--display);font-size:14px;font-weight:700;margin-bottom:10px">{{ICP_NAME}}</div>
      <div class="label" style="margin-bottom:6px">Offers</div>
      <div style="font-size:13px;line-height:1.5">{{OFFER}}</div>
    </div>

    <!-- Col 3: 90-Day Goal + Score -->
    <div>
      <div class="label" style="margin-bottom:6px">90-Day Goal</div>
      <div style="font-size:13px;line-height:1.5;margin-bottom:10px">{{GOAL_90D}}</div>
      <div style="display:flex;gap:12px;align-items:baseline">
        <div style="font-family:var(--display);font-size:28px;font-weight:700">{{AI_VISIBILITY_SCORE}}</div>
        <div class="label">AI Visibility</div>
      </div>
    </div>

  </div>
</section>
```

---

## Accent Line Snippet (inline fragment)

Drop between sections where noted in the base wrapper. Self-contained snippet — no variables:

```html
<div style="display:flex;align-items:center;gap:12px;margin:32px 0">
  <div style="flex:1;height:1px;background:var(--divider)"></div>
  <div style="width:16px;height:2px;background:var(--pp-red)"></div>
  <div style="flex:1;height:1px;background:var(--divider)"></div>
</div>
```

Use at most 3 per Brain. Default positions: after Section 2, after Section 5, after Section 7.

---

## Footer Snippet

Replaces the `{{FOOTER}}` slot in the base wrapper. One variable (`{{REPO_URL}}`) — defaults to the Purely Personal repo.

```html
<footer style="margin-top:64px;padding-top:32px;border-top:1px solid var(--divider);text-align:center">
  <div style="display:inline-flex;align-items:center;gap:8px;margin-bottom:12px">
    <div style="width:24px;height:24px;background:var(--pp-red);border-radius:4px;display:flex;align-items:center;justify-content:center;color:#fff;font-family:var(--display);font-weight:700;font-size:13px">pp</div>
    <div style="font-family:var(--display);font-weight:700;font-size:16px">{{BRAND_NAME}}</div>
  </div>
  <div style="font-size:12px;color:var(--text-muted);font-family:var(--mono)">BUSINESS BRAIN · {{BRAIN_DATE}} · {{BRAND_TAGLINE}}</div>
  <div style="margin-top:12px;font-size:12px;color:var(--text-secondary)">Built with <a href="{{REPO_URL}}" style="color:var(--pp-red);text-decoration:none;border-bottom:1px solid currentColor">purely-personal</a></div>
</footer>
```

Default `{{REPO_URL}}`: `https://github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself`

---

## Variable Legend Summary

| Variable | Where From | Fallback |
|----------|-----------|----------|
| `{{BRAIN_NAME}}` | BUSINESS-BRAIN.md → Operator section | Ask user |
| `{{BRAIN_HEADSHOT}}` | Operator → headshot url | Placeholder avatar SVG from primitives |
| `{{VOICE_TONE}}` | Voice section | `content-library.md` empty-state copy |
| `{{BANNED_PHRASES}}` | Voice section | Default AI-slop list from content-library |
| `{{ICP_NAME}}` | ICP section | Empty state card |
| `{{COMPETITORS}}` | Competitors section | Empty state ("Run /analyze-competitors") |
| `{{BRAND_COLORS}}` | Brand section | Extract from site via `brand-identity-extractor` |
| `{{AI_VISIBILITY_SCORE}}` | AI Visibility section | Empty state ("Run /audit-ai-visibility") |
| `{{PAIN_THEMES}}` | Pain section | Empty state ("Run /pull-reddit-pain") |
| `{{ACTIONS}}` | Hardcoded 5 engine commands | Always present |

---

## Assembly Checklist

Before emitting the final HTML:

- [ ] Base page wrapper wraps all sections
- [ ] All 9 section templates appear in order (or explicit subset requested)
- [ ] Every `{{VARIABLE}}` has been replaced (grep for `{{` before ship)
- [ ] SVG primitives inlined for all engine badges + radial meter
- [ ] Print CSS included in `<style>`
- [ ] Interactive scripts injected if mode = interactive (from `interactive-patterns.md`)
- [ ] No class names conflict across sections
- [ ] Colors pulled from CSS custom properties, not hardcoded per-section
