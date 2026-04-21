# Visual Catalog — Content Visual Builder

The 8 card types this skill can produce, specified structurally. Pick the right card for the platform, topic, and purpose.

---

## Card Type 1 — Single Post Card

**Template:** `code-templates.md` → Template #1 / #2 / #3 / #4 (one per platform)
**Dimensions:** Platform-native (LinkedIn 560px wide, X 560px, Instagram 540px, Newsletter 640px)

### Purpose
One platform. One post. The most common output. Use when the user says "make a LinkedIn post" or "draft a tweet."

### When to use
- Standard content shipment
- Demo render before posting
- Screenshot for sharing in Slack/DMs

### Variables
`{{USER_NAME}}`, `{{USER_TAGLINE}}`, `{{AVATAR_URL}}`, `{{POST_BODY}}`, `{{TIME_AGO}}`, engagement counts (decorative).

### Anti-patterns
- ❌ Never render identical content across 4 platforms — use Card Type 2 (Four-Platform Grid) for that.
- ❌ Never include hashtags on LinkedIn / X / Newsletter. Instagram only.

---

## Card Type 2 — Four-Platform Grid

**Template:** `code-templates.md` → Template #5
**Dimensions:** 1200px wide canvas, 2×2 grid of platform cards

### Purpose
Show the same core message adapted to 4 platforms. Use for cross-posting demos and workshop "here's what it produces" moments.

### When to use
- User says "same post, all 4 platforms"
- Workshop demos
- Campaign launches across channels

### Variables
`{{CAMPAIGN_TITLE}}`, `{{LINKEDIN_CARD}}`, `{{X_CARD}}`, `{{INSTAGRAM_CARD}}`, `{{NEWSLETTER_CARD}}`

### Rule
Same core CLAIM across all 4. Adjust form (hook style, length, CTA) per platform. Never duplicate verbatim — each card must be platform-native.

### Anti-patterns
- ❌ Never copy-paste the LinkedIn post to all 4 cards. Rewrite per platform.
- ❌ Never use emoji inconsistently (IG: moderate; LinkedIn/X hooks: zero; Newsletter: sparing).

---

## Card Type 3 — Carousel

**Template:** Platform-specific slide stack (LinkedIn PDF-style, Instagram swipeable)
**Dimensions:** 1080×1350 per slide, 5–10 slides

### Purpose
Multi-slide teaching content. Turn one insight into a sequenced visual narrative.

### When to use
- Topic needs 5+ concrete points
- Frameworks with steps
- Before/after stories
- Checklists

### Slide structure
```
Slide 1: Hook + promise ("Swipe to see 5 X →")
Slide 2–N: One idea per slide, big number, short body
Final slide: CTA (save / comment / DM)
```

### Anti-patterns
- ❌ Never exceed 10 slides. People swipe away.
- ❌ Never put multiple ideas on one slide.
- ❌ Final slide without a specific ask is a wasted slot.

---

## Card Type 4 — Quote Card

**Template:** `code-templates.md` → Template #6
**Dimensions:** 1080×1080 square (or 1080×1350 portrait)

### Purpose
One pull-quote rendered as a shareable graphic. Usually from the user's own content or a verbatim from their audience pain themes.

### When to use
- A post has one banger line
- A LinkedIn reply deserves a standalone graphic
- Pain theme verbatim (the "my best posts were from 2022 in the car" moment)

### Variables
`{{QUOTE}}`, `{{USER_NAME}}`, `{{ATTRIBUTION}}`, `{{PLATFORM_VAR}}` (for platform accent color)

### Anti-patterns
- ❌ Don't render full posts as quote cards. One sentence, max two.
- ❌ Don't use quote cards for claims without specifics. "You need to post consistently" is too vague; "12 hours a month or your pipeline dies" is a quote card.

---

## Card Type 5 — Stat Card

**Template:** `code-templates.md` → Template #7
**Dimensions:** 1080×1080 square

### Purpose
One giant number + context. The Hormozi-style $ or % or time stat that stops the scroll.

### When to use
- A milestone number from the Brain's Business section
- A proof stat ($0, 2hr/wk, 47 skills)
- An audit finding ("62% of AI content in SaaS sounds identical")

### Variables
`{{CATEGORY_LABEL}}`, `{{BIG_NUMBER}}`, `{{CONTEXT_LINE}}`, `{{EXPLANATION}}`, `{{PLATFORM_VAR}}`

### Rule
The big number must be scannable from 10 feet away on a phone. 200px display font, thick weight.

### Anti-patterns
- ❌ Never use small or percentage-heavy stats ("17.3%"). Round numbers or exact-but-memorable.
- ❌ Never include 2+ numbers on a stat card. One number, one idea.

---

## Card Type 6 — Cheatsheet

**Template:** `code-templates.md` → Template #9
**Dimensions:** 1080×1350 portrait (PDF-exportable for lead magnets)

### Purpose
A numbered list, framework, or checklist rendered as a printable/screenshotable asset. Used for LinkedIn "save this" posts or lead magnets.

### When to use
- 5–10 item framework
- Pre-flight checklist
- Step-by-step process summary
- Lead magnet downloadable

### Variables
`{{CHEATSHEET_TITLE}}`, `{{CHEATSHEET_SUBTITLE}}`, `{{CHEATSHEET_ITEMS}}` (numbered items)

### Anti-patterns
- ❌ Never exceed 10 items. Beyond that is an essay, not a cheatsheet.
- ❌ Never omit the numbered circles — they're the visual rhythm.
- ❌ Never skip the URL/handle in footer — this is a brand-distribution asset.

---

## Card Type 7 — Thread Preview (X)

**Template:** `code-templates.md` → Template #8
**Dimensions:** 560px wide variable height (stacked tweets)

### Purpose
Preview an X thread before publishing. Stacked vertical view of all tweets so user sees the full arc.

### When to use
- X thread drafting
- Reviewing a thread before publishing
- Demo asset showing thread structure

### Variables
`{{USER_NAME}}`, `{{USER_HANDLE}}`, `{{TWEET_COUNT}}`, `{{THREAD_TWEETS}}`

### Rule
Every tweet shows its index (`1/7`, `2/7`, etc.) and the vertical connector line, except the last tweet which closes the chain.

### Anti-patterns
- ❌ Never render a thread without the indexing visible.
- ❌ Never mix reply-style tweets with a numbered thread.

---

## Card Type 8 — Newsletter Header

**Template:** `code-templates.md` → Template #4
**Dimensions:** 640px wide (email-safe)

### Purpose
Email newsletter hero — subject line, preview text, body excerpt, CTA button. Usually exported as HTML for pasting into Beehiiv / ConvertKit / Substack.

### When to use
- Weekly newsletter issues
- Launch announcements
- Digest emails

### Variables
`{{NEWSLETTER_NAME}}`, `{{ISSUE_NUMBER}}`, `{{DATE}}`, `{{SUBJECT_LINE}}`, `{{PREVIEW_TEXT}}`, `{{BODY_EXCERPT}}`, `{{READ_MORE_URL}}`

### Email-safe rules
- Max width 640px
- Inline CSS only
- System font fallbacks (no custom fonts that block email-client rendering)
- All images ≤500KB with alt text

### Anti-patterns
- ❌ Never rely on external stylesheets (stripped by Gmail).
- ❌ Never use CSS grid or flexbox in ways Outlook can't parse. Use `<table>`-based layouts if high fidelity required.
- ❌ Never skip preview text.

---

## Choice Tree

Use this to pick the right card:

```
User says: "make a [thing]"

  ├─ "post" / "tweet" / "IG post" / "newsletter"
  │    → Card Type 1 (Single Post Card)
  │
  ├─ "all platforms" / "4 platforms" / "cross-post"
  │    → Card Type 2 (Four-Platform Grid)
  │
  ├─ "carousel" / "slides" / "swipe"
  │    → Card Type 3 (Carousel)
  │
  ├─ "quote card" / "quote graphic" / "pull quote"
  │    → Card Type 4 (Quote Card)
  │
  ├─ "stat card" / "big number" / "proof graphic"
  │    → Card Type 5 (Stat Card)
  │
  ├─ "cheatsheet" / "framework" / "checklist"
  │    → Card Type 6 (Cheatsheet)
  │
  ├─ "thread preview" / "X thread visual"
  │    → Card Type 7 (Thread Preview)
  │
  └─ "newsletter header" / "email hero"
       → Card Type 8 (Newsletter Header)
```

---

## Global Quality Bar (all card types)

Every card must:
- [ ] Pass voice validation (no banned phrases from Brain)
- [ ] Fit platform dimensions exactly (no scrollbars)
- [ ] Include brand corner mark (user's handle OR pp brand)
- [ ] Use engine colors correctly if engine-tagged
- [ ] Have print CSS for PDF export
- [ ] Load fonts from Google Fonts CDN (not bundled assets)

If any check fails: rewrite or regenerate. Never ship a half-working card.
