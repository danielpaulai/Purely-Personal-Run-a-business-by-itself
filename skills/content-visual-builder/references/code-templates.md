# Code Templates — Content Visual Builder

HTML/CSS templates for the 4 platforms and 8 card types. Copy the template, fill variables, ship. Each template uses the same root CSS custom properties so 4-platform grid mode renders consistently.

---

## Template #0: Base Page Wrapper

Same as `business-brain-renderer` base wrapper. Reuse those CSS custom properties. For single-card mode, wrap in a minimal shell:

```html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Rethink+Sans:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --page-bg:#faf8f4;
  --text-primary:#1a1a1a; --text-secondary:#6b6b6b; --text-muted:#a8a39b;
  --pp-red:#e90d41;
  --platform-linkedin:#0A66C2;
  --platform-x:#0F1419;
  --platform-x-blue:#1D9BF0;
  --platform-instagram-gradient:linear-gradient(135deg,#833AB4,#FD1D1D,#FCB045);
  --platform-newsletter:#E8D9C5;
  --display:'Rethink Sans','Inter',sans-serif;
  --body:'Inter',sans-serif;
  --mono:'JetBrains Mono',Menlo,monospace;
}
body{background:var(--page-bg);margin:0;padding:48px 24px;font-family:var(--body);color:var(--text-primary)}
</style>
</head>
<body>
{{CONTENT}}
</body>
</html>
```

---

## Template #1: LinkedIn Post Card

Standard LinkedIn feed card. Square (1080×1080) when rendered for export.

```html
<article style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #e8e2d8;border-radius:8px;overflow:hidden;font-family:var(--body);box-shadow:0 1px 3px rgba(0,0,0,0.05)">

  <!-- Header -->
  <header style="display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #e8e2d8">
    <div style="width:48px;height:48px;border-radius:999px;background:#f0eeea;flex-shrink:0;overflow:hidden">
      <img src="{{AVATAR_URL}}" alt="{{USER_NAME}}" style="width:100%;height:100%;object-fit:cover">
    </div>
    <div style="flex:1;min-width:0">
      <div style="font-family:var(--display);font-weight:700;font-size:15px;color:var(--text-primary);line-height:1.2">{{USER_NAME}}</div>
      <div style="font-size:12px;color:var(--text-secondary);margin-top:2px">{{USER_TAGLINE}}</div>
      <div style="font-size:11px;color:var(--text-muted);margin-top:1px">{{TIME_AGO}} · 🌎</div>
    </div>
    <div style="width:18px;height:18px;color:var(--platform-linkedin)">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.63-1.85 3.36-1.85 3.59 0 4.25 2.37 4.25 5.45v6.29z"/></svg>
    </div>
  </header>

  <!-- Body -->
  <div style="padding:16px;font-size:14px;line-height:1.6;white-space:pre-wrap;color:var(--text-primary)">{{POST_BODY}}</div>

  <!-- Reactions footer (decorative for card — shows social proof) -->
  <footer style="display:flex;align-items:center;justify-content:space-between;padding:10px 16px;border-top:1px solid #e8e2d8;font-size:12px;color:var(--text-secondary)">
    <span>👍 💡 ❤️ · {{REACTION_COUNT}}</span>
    <span>{{COMMENT_COUNT}} comments · {{SHARE_COUNT}} reposts</span>
  </footer>

</article>
```

---

## Template #2: X (Twitter) Post Card

Dark-mode X card.

```html
<article style="max-width:560px;margin:0 auto;background:#000000;border:1px solid #2f3336;border-radius:16px;overflow:hidden;font-family:var(--body);color:#ffffff">

  <header style="display:flex;align-items:flex-start;gap:12px;padding:12px 16px 4px">
    <div style="width:44px;height:44px;border-radius:999px;background:#2f3336;flex-shrink:0;overflow:hidden">
      <img src="{{AVATAR_URL}}" alt="{{USER_NAME}}" style="width:100%;height:100%;object-fit:cover">
    </div>
    <div style="flex:1;min-width:0">
      <div style="display:flex;align-items:baseline;gap:6px;flex-wrap:wrap">
        <span style="font-weight:700;font-size:15px">{{USER_NAME}}</span>
        <span style="color:#71767b;font-size:14px">@{{USER_HANDLE}}</span>
        <span style="color:#71767b;font-size:14px">·</span>
        <span style="color:#71767b;font-size:14px">{{TIME_AGO}}</span>
      </div>
    </div>
  </header>

  <div style="padding:0 16px 12px;font-size:15px;line-height:1.4;white-space:pre-wrap">{{POST_BODY}}</div>

  <footer style="display:flex;align-items:center;gap:28px;padding:8px 16px 12px;color:#71767b;font-size:13px">
    <span>💬 {{REPLY_COUNT}}</span>
    <span>🔁 {{RETWEET_COUNT}}</span>
    <span>❤️ {{LIKE_COUNT}}</span>
    <span>📊 {{VIEW_COUNT}}</span>
  </footer>

</article>
```

---

## Template #3: Instagram Post Card

Square Instagram feed card with gradient border accent.

```html
<article style="max-width:540px;margin:0 auto;background:#ffffff;border-radius:12px;overflow:hidden;font-family:var(--body);position:relative;box-shadow:0 1px 3px rgba(0,0,0,0.05)">

  <!-- Gradient top border -->
  <div style="height:3px;background:var(--platform-instagram-gradient)"></div>

  <header style="display:flex;align-items:center;gap:10px;padding:12px 14px">
    <div style="width:36px;height:36px;border-radius:999px;padding:2px;background:var(--platform-instagram-gradient);flex-shrink:0">
      <div style="width:100%;height:100%;border-radius:999px;background:#ffffff;padding:2px">
        <img src="{{AVATAR_URL}}" alt="{{USER_NAME}}" style="width:100%;height:100%;object-fit:cover;border-radius:999px">
      </div>
    </div>
    <div style="flex:1;font-weight:700;font-size:14px">{{USER_HANDLE}}</div>
    <div style="font-size:20px;color:var(--text-secondary)">⋯</div>
  </header>

  <!-- Square image placeholder (where user's graphic goes) -->
  <div style="aspect-ratio:1;background:{{IMAGE_BG}};display:flex;align-items:center;justify-content:center;padding:40px;text-align:center">
    <div style="font-family:var(--display);font-size:28px;font-weight:700;color:{{IMAGE_TEXT_COLOR}};line-height:1.2">{{IMAGE_HEADLINE}}</div>
  </div>

  <!-- Action row -->
  <div style="display:flex;align-items:center;gap:16px;padding:10px 14px;font-size:22px">
    <span>♥</span>
    <span>💬</span>
    <span>✈</span>
    <span style="margin-left:auto">🔖</span>
  </div>

  <!-- Caption -->
  <div style="padding:0 14px 12px;font-size:14px;line-height:1.5">
    <strong>{{USER_HANDLE}}</strong> <span style="white-space:pre-wrap">{{POST_CAPTION}}</span>
  </div>

  <div style="padding:0 14px 12px;font-size:12px;color:var(--text-muted)">{{TIME_AGO}}</div>

</article>
```

---

## Template #4: Newsletter Header Card

Warm editorial card for newsletter preview or embedded promo.

```html
<article style="max-width:640px;margin:0 auto;background:var(--platform-newsletter);padding:40px 32px;font-family:var(--body);color:var(--text-primary);border-top:4px solid var(--text-primary)">

  <!-- Issue meta -->
  <div style="font-family:var(--mono);font-size:11px;color:var(--text-primary);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:16px">
    {{NEWSLETTER_NAME}} · Issue #{{ISSUE_NUMBER}} · {{DATE}}
  </div>

  <!-- Subject line -->
  <h1 style="font-family:var(--display);font-size:32px;font-weight:700;margin:0 0 12px;line-height:1.15">{{SUBJECT_LINE}}</h1>

  <!-- Preview text -->
  <p style="font-size:16px;color:var(--text-secondary);margin:0 0 24px;line-height:1.5">{{PREVIEW_TEXT}}</p>

  <!-- Divider -->
  <div style="width:40px;height:2px;background:var(--text-primary);margin-bottom:24px"></div>

  <!-- Body excerpt -->
  <div style="font-size:15px;line-height:1.7;color:var(--text-primary);white-space:pre-wrap">{{BODY_EXCERPT}}</div>

  <!-- Read more CTA -->
  <a href="{{READ_MORE_URL}}" style="display:inline-block;margin-top:24px;padding:10px 20px;background:var(--text-primary);color:var(--platform-newsletter);text-decoration:none;font-weight:700;font-size:14px;border-radius:2px">Read full issue →</a>

  <!-- Sign-off -->
  <footer style="margin-top:32px;padding-top:20px;border-top:1px solid rgba(0,0,0,0.1);font-size:13px;color:var(--text-secondary)">
    — {{USER_NAME}} · <a href="{{NEWSLETTER_URL}}" style="color:var(--text-primary);border-bottom:1px solid currentColor;text-decoration:none">{{NEWSLETTER_URL_DISPLAY}}</a>
  </footer>

</article>
```

---

## Template #5: Four-Platform Grid

Renders all four cards side-by-side. Use for showing the same content adapted to each platform.

```html
<main style="max-width:1200px;margin:0 auto;padding:32px">

  <!-- Header -->
  <div style="margin-bottom:32px;text-align:center">
    <div class="label" style="font-size:11px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:var(--text-secondary);margin-bottom:8px">Same message, four platforms</div>
    <h1 style="font-family:var(--display);font-size:28px;font-weight:700;margin:0">{{CAMPAIGN_TITLE}}</h1>
  </div>

  <!-- Tab navigation (optional — renders all 4 at once below) -->
  <div style="display:flex;gap:4px;justify-content:center;margin-bottom:24px;padding:4px;background:#ffffff;border:1px solid #e8e2d8;border-radius:999px;max-width:fit-content;margin-left:auto;margin-right:auto">
    <button data-tab="linkedin" style="padding:6px 16px;border:0;background:var(--platform-linkedin);color:#fff;border-radius:999px;font-size:13px;font-weight:500">LinkedIn</button>
    <button data-tab="x" style="padding:6px 16px;border:0;background:transparent;color:var(--text-primary);border-radius:999px;font-size:13px;font-weight:500">X</button>
    <button data-tab="instagram" style="padding:6px 16px;border:0;background:transparent;color:var(--text-primary);border-radius:999px;font-size:13px;font-weight:500">Instagram</button>
    <button data-tab="newsletter" style="padding:6px 16px;border:0;background:transparent;color:var(--text-primary);border-radius:999px;font-size:13px;font-weight:500">Newsletter</button>
  </div>

  <!-- 2x2 grid of platform cards -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
    <div data-platform="linkedin">{{LINKEDIN_CARD}}</div>
    <div data-platform="x">{{X_CARD}}</div>
    <div data-platform="instagram">{{INSTAGRAM_CARD}}</div>
    <div data-platform="newsletter">{{NEWSLETTER_CARD}}</div>
  </div>

</main>
```

---

## Template #6: Quote Card

Big pull-quote on clean background. Platform color as accent. Used for shareable graphics.

```html
<article style="max-width:1080px;aspect-ratio:1;margin:0 auto;padding:80px 72px;background:#ffffff;border:1px solid #e8e2d8;border-radius:12px;display:flex;flex-direction:column;justify-content:space-between;font-family:var(--body);position:relative;box-shadow:0 1px 3px rgba(0,0,0,0.05)">

  <!-- Top: brand mark + platform indicator -->
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div style="font-family:var(--mono);font-size:12px;color:var(--text-muted);letter-spacing:0.08em;text-transform:uppercase">{{USER_NAME}}</div>
    <div style="font-size:14px;color:var({{PLATFORM_VAR}});font-weight:700">{{PLATFORM_NAME}}</div>
  </div>

  <!-- Big quote -->
  <div style="margin:auto 0">
    <div style="color:var({{PLATFORM_VAR}});opacity:0.15;font-size:120px;line-height:0.5;font-family:var(--display)">"</div>
    <p style="font-family:var(--display);font-size:48px;font-weight:700;line-height:1.2;margin:0 0 24px;color:var(--text-primary)">{{QUOTE}}</p>
  </div>

  <!-- Attribution -->
  <div style="display:flex;align-items:center;gap:14px;padding-top:24px;border-top:1px solid #e8e2d8">
    <div style="width:48px;height:48px;border-radius:999px;overflow:hidden">
      <img src="{{AVATAR_URL}}" style="width:100%;height:100%;object-fit:cover">
    </div>
    <div>
      <div style="font-family:var(--display);font-weight:700;font-size:18px">{{USER_NAME}}</div>
      <div style="font-size:13px;color:var(--text-secondary)">{{ATTRIBUTION}}</div>
    </div>
  </div>

</article>
```

Platform variable map:

| Platform | `{{PLATFORM_VAR}}` | `{{PLATFORM_NAME}}` |
|----------|--------------------|--------------------|
| LinkedIn | `--platform-linkedin` | `LinkedIn` |
| X | `--platform-x` | `X` |
| Instagram | `--platform-instagram-gradient` (use `background` not `color`) | `Instagram` |
| Newsletter | `--platform-newsletter` | `Newsletter` |

---

## Template #7: Stat Card

One giant number + context. 1080×1080 square.

```html
<article style="max-width:1080px;aspect-ratio:1;margin:0 auto;padding:72px;background:#ffffff;border:1px solid #e8e2d8;border-radius:12px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;font-family:var(--body);box-shadow:0 1px 3px rgba(0,0,0,0.05)">

  <!-- Category label -->
  <div style="font-family:var(--mono);font-size:14px;color:var(--text-secondary);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:24px">{{CATEGORY_LABEL}}</div>

  <!-- Big number -->
  <div style="font-family:var(--display);font-size:200px;font-weight:700;line-height:0.9;color:var({{PLATFORM_VAR}});letter-spacing:-0.03em;margin-bottom:16px;font-feature-settings:'tnum'">{{BIG_NUMBER}}</div>

  <!-- Context -->
  <div style="font-family:var(--display);font-size:28px;font-weight:700;line-height:1.2;margin-bottom:32px;max-width:720px">{{CONTEXT_LINE}}</div>

  <!-- Explanation -->
  <p style="font-size:18px;line-height:1.5;color:var(--text-secondary);max-width:560px;margin:0">{{EXPLANATION}}</p>

  <!-- Footer brand -->
  <div style="position:absolute;bottom:32px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:8px">
    <div style="width:20px;height:20px;background:var(--pp-red);border-radius:4px"></div>
    <span style="font-family:var(--mono);font-size:12px;color:var(--text-muted)">{{USER_NAME}}</span>
  </div>

</article>
```

---

## Template #8: Thread Preview (X)

Stacked view of an X thread — preview what a full thread will look like.

```html
<article style="max-width:560px;margin:0 auto;background:#000000;border:1px solid #2f3336;border-radius:16px;overflow:hidden;font-family:var(--body);color:#ffffff">

  <!-- Header (same as X post) -->
  <header style="display:flex;align-items:flex-start;gap:12px;padding:12px 16px 4px">
    <div style="width:44px;height:44px;border-radius:999px;background:#2f3336;flex-shrink:0;overflow:hidden">
      <img src="{{AVATAR_URL}}" style="width:100%;height:100%;object-fit:cover">
    </div>
    <div style="flex:1">
      <div style="display:flex;align-items:baseline;gap:6px">
        <span style="font-weight:700;font-size:15px">{{USER_NAME}}</span>
        <span style="color:#71767b;font-size:14px">@{{USER_HANDLE}}</span>
      </div>
      <span style="color:#71767b;font-size:13px">Thread · {{TWEET_COUNT}} tweets</span>
    </div>
  </header>

  <!-- Stacked tweets -->
  <div style="padding:4px 0">
    {{THREAD_TWEETS}}
  </div>

</article>
```

### Thread Tweet Sub-Template (repeat N times)

```html
<div style="padding:8px 16px 16px 72px;border-left:2px solid #2f3336;margin-left:34px;position:relative;font-size:15px;line-height:1.4;white-space:pre-wrap">
  <span style="position:absolute;left:0;top:8px;font-family:var(--mono);font-size:11px;color:#71767b;letter-spacing:0.08em">{{TWEET_INDEX}}/{{TWEET_COUNT}}</span>
  {{TWEET_TEXT}}
</div>
```

Last tweet in the thread omits the `border-left` to close the chain cleanly.

---

## Template #9: Cheatsheet Card

Checklist or framework in a printable card. Use for lead-magnet-style giveaways rendered as 1080×1350 portrait.

```html
<article style="max-width:1080px;aspect-ratio:4/5;margin:0 auto;padding:72px 64px;background:#faf8f4;border:1px solid #e8e2d8;border-radius:12px;font-family:var(--body);color:var(--text-primary);display:flex;flex-direction:column">

  <!-- Header -->
  <div style="margin-bottom:32px">
    <div style="font-family:var(--mono);font-size:12px;letter-spacing:0.1em;text-transform:uppercase;color:var(--pp-red);margin-bottom:8px">Cheatsheet</div>
    <h1 style="font-family:var(--display);font-size:44px;font-weight:700;margin:0 0 12px;line-height:1.1">{{CHEATSHEET_TITLE}}</h1>
    <p style="font-size:17px;color:var(--text-secondary);margin:0">{{CHEATSHEET_SUBTITLE}}</p>
  </div>

  <!-- Items -->
  <div style="flex:1;display:flex;flex-direction:column;gap:16px">
    {{CHEATSHEET_ITEMS}}
  </div>

  <!-- Footer -->
  <div style="display:flex;justify-content:space-between;align-items:center;padding-top:24px;border-top:1px solid #e8e2d8;margin-top:32px">
    <div style="display:flex;align-items:center;gap:10px">
      <div style="width:24px;height:24px;background:var(--pp-red);border-radius:4px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px">pp</div>
      <span style="font-family:var(--display);font-weight:700;font-size:14px">{{USER_NAME}}</span>
    </div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text-muted)">{{CHEATSHEET_URL}}</div>
  </div>

</article>
```

### Cheatsheet Item Sub-Template (numbered)

```html
<div style="display:flex;gap:16px;align-items:flex-start">
  <div style="width:32px;height:32px;border-radius:999px;background:var(--pp-red);color:#fff;display:flex;align-items:center;justify-content:center;font-family:var(--display);font-weight:700;font-size:14px;flex-shrink:0">{{NUM}}</div>
  <div>
    <div style="font-family:var(--display);font-weight:700;font-size:18px;margin-bottom:4px">{{ITEM_TITLE}}</div>
    <div style="font-size:15px;line-height:1.5;color:var(--text-secondary)">{{ITEM_BODY}}</div>
  </div>
</div>
```

---

## Variable Map

| Variable | Source | Fallback |
|----------|--------|----------|
| `{{USER_NAME}}` | `BUSINESS-BRAIN.md` → Operator | Ask |
| `{{USER_TAGLINE}}` | Brain → Operator tagline | — |
| `{{USER_HANDLE}}` | Brain → LinkedIn handle | Derive from name |
| `{{AVATAR_URL}}` | Brain → headshot | Placeholder avatar SVG |
| `{{POST_BODY}}` | Generated draft | — |
| `{{TIME_AGO}}` | `now()` | `"1h"` |
| `{{REACTION_COUNT}}` / `{{LIKE_COUNT}}` | Decorative | Random 40–180 |
| `{{COMMENT_COUNT}}` | Decorative | Random 4–22 |
| `{{RETWEET_COUNT}}` | Decorative | Random 3–15 |
| `{{VIEW_COUNT}}` | Decorative | Random 1.2k–40k |
| `{{PLATFORM_VAR}}` | Per-platform lookup | Required |
| `{{PLATFORM_NAME}}` | Per-platform lookup | Required |
| `{{CAMPAIGN_TITLE}}` | User input for 4-platform grid | Ask |

Decorative counts exist so the card renders realistically in preview mode. Never display them as real analytics — they are mockup-only.

---

## Assembly Checklist

- [ ] All `{{VARIABLES}}` replaced (grep `{{` before ship)
- [ ] Post body copy validated against voice rules (banned phrases absent, hook pattern match)
- [ ] Character count under platform limit
- [ ] Safe zones respected (critical content ≥32–48px from edges)
- [ ] Emoji usage matches platform norms (none in X hooks, moderate on Instagram, zero on LinkedIn hooks)
- [ ] P.S. present on LinkedIn cards, ending with a question
- [ ] Avatar loads or placeholder renders cleanly
- [ ] Printable if cheatsheet — `@media print` CSS included
