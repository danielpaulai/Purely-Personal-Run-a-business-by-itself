# Platform Specs — Content Visual Builder

Exact dimensions, safe zones, character limits, and rendering constraints for the 4 platforms. Use this file before cropping, sizing, or truncating anything.

---

## LinkedIn

### Image dimensions

| Asset | Dimensions (px) | Aspect ratio | Notes |
|-------|-----------------|--------------|-------|
| Feed post (landscape) | 1200 × 628 | 1.91:1 | Max 5MB |
| Feed post (square) | 1080 × 1080 | 1:1 | Preferred for carousels |
| Feed post (portrait) | 1080 × 1350 | 4:5 | Tallest allowed — more feed real estate |
| Carousel slide | 1080 × 1350 | 4:5 | PDF format, max 10 MB, max 300 slides |
| Article hero | 1280 × 720 | 16:9 | For LinkedIn Articles |

### Text constraints

| Field | Max chars | Notes |
|-------|-----------|-------|
| Post body | 3,000 | Shows "see more" at ~210 chars on mobile |
| First 210 chars | — | Critical — this is what shows before "see more" |
| Comment | 1,250 | — |
| Headline (profile) | 220 | — |

### Safe zone

Keep critical content ≥48px from every edge. LinkedIn crops unpredictably across mobile/desktop.

### Hook rule

First 1–2 lines must carry the full hook. Readers decide to click "see more" in <2 seconds.

---

## X (Twitter)

### Image dimensions

| Asset | Dimensions (px) | Aspect ratio | Notes |
|-------|-----------------|--------------|-------|
| Single tweet image (landscape) | 1600 × 900 | 16:9 | Best for threads/articles |
| Single tweet image (square) | 1080 × 1080 | 1:1 | Good for standalone posts |
| Single tweet image (portrait) | 1080 × 1350 | 4:5 | Max portrait — more feed space |
| Header | 1500 × 500 | 3:1 | Profile banner |

### Text constraints

| Field | Max chars | Notes |
|-------|-----------|-------|
| Tweet body | 280 | Premium users: 25,000 |
| Thread tweet | 280 each | 5–8 tweets typical thread |
| Quote tweet | 280 + original | — |

### Safe zone

Keep critical content ≥32px from every edge.

### Hook rule

First 40 chars are the preview in timelines. Lead with the punch.

### Thread structure

```
Tweet 1 (hook): curiosity gap + 👇
Tweet 2 (context): setup the problem
Tweet 3-6 (body): numbered steps or points
Tweet 7 (result): the outcome
Tweet 8 (CTA): quote-tweet of T1 + ask for RT
```

---

## Instagram

### Image dimensions

| Asset | Dimensions (px) | Aspect ratio | Notes |
|-------|-----------------|--------------|-------|
| Feed post (square) | 1080 × 1080 | 1:1 | Classic — still default |
| Feed post (portrait) | 1080 × 1350 | 4:5 | Best for feed real estate |
| Reel cover | 1080 × 1920 | 9:16 | Vertical |
| Story | 1080 × 1920 | 9:16 | Keep text in 1080×1440 center safe zone |
| Carousel | 1080 × 1080 or 1080 × 1350 | 1:1 or 4:5 | Max 10 slides per post |

### Text constraints

| Field | Max chars | Notes |
|-------|-----------|-------|
| Caption | 2,200 | First 125 chars = preview before "…more" |
| Bio | 150 | — |
| Hashtags in caption | 30 | Only first ~3 typically useful |

### Safe zone

For stories/reels: keep critical content within 1080×1440 center zone. Top 250px and bottom 250px get UI chrome overlay.

### Gradient rule

Instagram brand uses a gradient `#833AB4 → #FD1D1D → #FCB045`. When rendering Instagram-variant cards, use this gradient as the accent — but sparingly (border or small element, never large fill).

### Invisible spacing

Instagram collapses blank lines in captions. To preserve paragraph spacing, use this invisible character: `⁣` (U+2063). Place one on its own line between paragraphs.

---

## Newsletter

### Image dimensions

| Asset | Dimensions (px) | Aspect ratio | Notes |
|-------|-----------------|--------------|-------|
| Hero image | 1200 × 600 | 2:1 | Above the fold |
| Inline image | ≤640 wide | Flexible | Email clients cap width at 640 |
| Avatar | 200 × 200 | 1:1 | Sender picture |

### Text constraints

| Field | Max chars / words | Notes |
|-------|-------------------|-------|
| Subject line | 30–50 chars optimal | 9 words max for mobile preview |
| Preview text | 85–110 chars | Extends the hook — not a repeat |
| Body | No hard limit | Optimal: 400–1,200 words |
| Paragraph | ≤3 sentences | Email reads short |

### Email client constraints

- Max width: **640px** (wider breaks Gmail/Outlook)
- Font fallback chain: Inter → Helvetica → Arial → sans-serif
- Dark mode: use `prefers-color-scheme: dark` media query or supply dual-tone logos
- Images: always include `alt` text (images blocked by default in Outlook)
- CSS: inline only (external stylesheets stripped by Gmail)

### Safe zone

Keep CTA buttons ≥44px tall for touch targets. Keep all critical text outside the first/last 24px padding.

---

## Character Count Strategy Per Platform

When given the same source copy, apportion as follows:

| Copy length | LinkedIn | X | Instagram | Newsletter |
|-------------|----------|---|-----------|------------|
| Short idea | 1 post ~200 words | 1 tweet | 1 caption ~150 words | Not worth sending |
| Medium idea | 1 post ~300 words | Thread 5 tweets | 1 caption ~300 words | Short email ~400 words |
| Long idea | 1 post ~500 words + comment | Thread 8 tweets | Carousel 5–7 slides | Full email 800–1,200 words |

---

## Visual Consistency Across Platforms

When rendering 4-platform grid, use these constants so the set looks cohesive:

| Element | All platforms |
|---------|---------------|
| User avatar | Same round 64px |
| Display name | Same font (Rethink Sans 700) |
| Handle / URL | Same (mono font) |
| Body font | Inter 400 |
| Link color | Platform primary color |
| Line height | 1.55 |

What changes per platform:

| Element | LinkedIn | X | Instagram | Newsletter |
|---------|----------|---|-----------|------------|
| Card background | `#ffffff` on `#F3F2EF` | `#ffffff` on `#000000` | Gradient border on `#ffffff` | `#E8D9C5` paper |
| Accent color | `#0A66C2` | `#1D9BF0` | Gradient | `#1a1a1a` |
| Border radius | 8px | 16px | 12px | 0 |
| Max width (card render) | 560px | 560px | 540px (square) | 640px |

---

## Truncation Rules

When content exceeds platform limit:

**LinkedIn:** split into post + first comment (up to 1,250 chars extra)
**X:** convert to thread (split at natural paragraph breaks)
**Instagram:** move anything beyond 1,800 chars into a carousel
**Newsletter:** no truncation — longer is fine

Never truncate mid-sentence. Always split at paragraph breaks.

---

## Image Export Rules

| Platform | Format | Max size | DPI | Notes |
|----------|--------|----------|-----|-------|
| LinkedIn | PNG or JPG | 5 MB | 72 | No GIFs in feed (only reactions) |
| X | PNG or JPG | 5 MB | 72 | GIFs OK, max 15 MB |
| Instagram | PNG or JPG | 8 MB | 72 | No PDF carousels |
| Newsletter | PNG or JPG | 500 KB recommended | 72 | Keep image assets under 500 KB — email clients cache aggressively |

---

## Anti-patterns

- ❌ Never render at screen density. Always 1× (72dpi) for feeds.
- ❌ Never rely on custom fonts in newsletter — use system fallbacks.
- ❌ Never put critical content in corners (feeds crop unpredictably).
- ❌ Never use transparent PNGs with dark content on light backgrounds — email dark mode inverts.
- ❌ Never exceed platform char limits. Either truncate at a paragraph break, or split.
- ❌ Never use the same exact caption across 4 platforms. The voice stays; the form adapts.
