# Content Library — Business Brain Renderer

Pre-written copy, empty states, fallbacks, and writing standards. Every string that the renderer outputs without user input comes from this file. **Never fabricate content at render time — pull from here.**

---

## Empty-State Copy

When a Brain section is missing data, render the section card with empty-state copy. Each empty state has: (1) a short explanation, (2) a slash-command CTA, (3) an expected-time estimate.

### Voice Card — Empty

```
Title: "Voice isn't set yet"
Body: "Run the extraction to pull your writing style from your last 30 posts."
CTA: /extract-my-voice
Time: ~2 minutes
```

### Business Card — Empty

```
Title: "Business profile isn't filled in"
Body: "Paste your website URL and we'll extract your offer, positioning, and pricing."
CTA: /extract-my-business
Time: ~90 seconds
```

### ICP Card — Empty

```
Title: "You haven't named your ideal client"
Body: "Answer three questions and we'll build a named persona with pain, desire, and objections."
CTA: /define-my-icp
Time: ~3 minutes
```

### Competitor Matrix — Empty

```
Title: "No competitors analyzed yet"
Body: "Paste three competitor URLs. We'll pull their positioning and show you the gaps to own."
CTA: /analyze-competitors
Time: ~4 minutes
```

### Brand Card — Empty

```
Title: "Brand identity not extracted"
Body: "We'll pull your color palette, fonts, and visual voice from your site automatically."
CTA: /extract-brand-identity
Time: ~60 seconds
```

### AI Visibility — Empty

```
Title: "You haven't been audited yet"
Body: "See how ChatGPT, Perplexity, and Claude answer when someone asks for you."
CTA: /audit-ai-visibility
Time: ~5 minutes
```

### Pain Themes — Empty

```
Title: "No audience intel pulled yet"
Body: "We'll scrape Reddit and forums for your ICP's real complaints — verbatim."
CTA: /pull-reddit-pain
Time: ~3 minutes
```

---

## Empty State Card Template

When rendering an empty state, use this card shape (drops into any section slot):

```html
<div style="padding:32px 24px;text-align:center;background:var(--sub-card-bg);border:1px dashed var(--divider-strong);border-radius:4px">
  <div class="label" style="color:var(--text-muted);margin-bottom:8px">{{SECTION_NUMBER}} · {{SECTION_NAME}}</div>
  <h3 style="font-family:var(--display);font-size:18px;font-weight:700;margin:0 0 6px">{{EMPTY_TITLE}}</h3>
  <p style="font-size:13px;color:var(--text-secondary);margin:0 0 16px;max-width:440px;margin-left:auto;margin-right:auto">{{EMPTY_BODY}}</p>
  <div style="display:inline-flex;align-items:center;gap:8px;padding:8px 14px;background:var(--pp-red);color:#fff;border-radius:4px;font-size:13px;font-weight:500;font-family:var(--mono)">
    {{CTA}} <span style="opacity:0.7">· {{TIME}}</span>
  </div>
</div>
```

---

## Default Banned Phrases (fallback when Voice section missing or incomplete)

If the user hasn't defined banned phrases, seed from this baseline AI-slop list. Show these as default so the renderer is never visually empty:

```
—              (em-dash)
unlock
delve
supercharge
game-changer
elevate
seamless
revolutionary
cutting-edge
leverage
synergy
it's not just X, it's Y
```

**Rule:** if user has defined banned phrases, use ONLY user's list. Never merge with defaults. The defaults are fallback, not enhancement.

---

## Default Hook Patterns (fallback for Voice section)

If user hasn't specified hook patterns, show these research-backed defaults (same pattern sourced across Dan Koe / Justin Welsh / Nicolas Cole analysis):

```
1. The stat hook      → "93% of [X] never [Y]. Here's why."
2. The contrarian     → "Everyone says [common advice]. They're wrong because [reason]."
3. The personal       → "I spent [time] trying [thing]. Here's what actually worked."
4. The list promise   → "[N] [things] that [desired outcome]."
5. The question       → "What if [common assumption] was backwards?"
```

Label these as "Default patterns — replace with your own" in the UI so users know they're placeholder.

---

## Default Voice Rules (fallback)

If user hasn't specified voice rules:

```
1. Write like you talk. Conversational beats polished.
2. One idea per sentence. No compound complexity.
3. Specifics beat generalities. "12 clients" beats "many clients".
4. No hedging. Cut "maybe", "perhaps", "I think".
5. End on a verb or a question. Never trail off.
```

---

## Empty Example Posts (fallback)

If user hasn't shared example posts, render one card with:

```
"Your example posts go here. Run /extract-my-voice to auto-pull from your recent LinkedIn."
```

Do not invent fake example posts. Ever.

---

## Empty ICP (fallback persona)

If user needs a prompt to imagine their ICP, these are standard starter profiles by industry. **Never render these as the user's actual ICP — only suggest them in the empty-state CTA flow.**

| Industry | Starter ICP |
|----------|-------------|
| SaaS | "Founder at $500k–$5M ARR, sells B2B, 1–5 person team, does their own marketing." |
| Agency | "Boutique service owner, 2–10 employees, $300k–$2M revenue, stuck at capacity." |
| Coaching | "Coach, 1–3 years in, $5k–$25k/month, still selling 1:1, wants productized offer." |
| Course Creator | "Educator, audience 5k–50k, one course live, ~$10k/month, wants to scale without a launch." |
| Freelancer | "Solo operator, client work 80% of time, burnt out, wants recurring revenue." |

---

## Voice Standards (applied to all renderer copy — labels, CTAs, empty states)

### Tone

Confident, warm, direct. Never corporate. Never cute. Never hype.

### Length

Every string in this library is as short as it can be while carrying its weight. If a button says more than 4 words, rewrite it.

### Banned Phrases (the renderer itself must never output these)

The renderer's OWN copy must be clean, even if the user's Brain data isn't. These are banned from every label, CTA, empty state, and placeholder in this file:

- em-dashes (`—`) — use a period or comma
- "unlock" — use "open", "reveal", "access"
- "delve" — use "dig in", "look at"
- "supercharge" — use "speed up", "boost"
- "seamless" — use "clean", "simple", "quiet"
- "elevate" — use "raise", "lift"
- "game-changer" — just describe the change
- "leverage" (as verb) — use "use"
- "it's not just X, it's Y" — pick one
- "journey" (for product experience) — use "process", "flow"
- "ecosystem" (for feature set) — use "stack", "tools"

### Punctuation

- Oxford comma: yes
- Serial semicolons: no
- Exclamation marks: no (except in the Actions Panel badge "TAKE ACTION")
- Ellipses: no
- Smart quotes: yes (`"`, `'`) — never straight quotes in rendered copy

---

## Label Canonicals

Every section uses these exact labels. Do not reword across renders.

| Section | Label |
|---------|-------|
| 01 | VOICE |
| 02 | BUSINESS |
| 03 | IDEAL CLIENT |
| 04 | COMPETITORS |
| 05 | BRAND IDENTITY |
| 06 | AI VISIBILITY |
| 07 | AUDIENCE PAIN |
| 08 | — (Actions Panel uses "TAKE ACTION" badge instead) |

Sub-labels inside sections:

| Context | Label |
|---------|-------|
| Voice → banned chips | "Banned phrases" |
| Voice → rules list | "Voice rules" |
| Voice → hooks | "Hook patterns" |
| Voice → examples | "Example openings" |
| Business → offer | "Offer" |
| Business → positioning | "Positioning" |
| Business → price | "Pricing" |
| Business → goal | "90-Day Goal" |
| Business → metric | "Key Metric" |
| ICP → where | "Hangs out at" |
| ICP → pain | "Pain" |
| ICP → desire | "Desire" |
| ICP → objection | "Objection" |
| Comp → name | "Competitor" |
| Comp → their | "Their angle" |
| Comp → gap | "Gap to own" |
| Brand → colors | "Color palette" |
| Brand → typography | "Typography" |
| Brand → voice | "Visual voice" |
| AI → score | "Visibility Score" |
| AI → gaps | "Queries where you don't rank" |

---

## Action Labels (Actions Panel)

These are fixed. Do not reword, do not reorder, do not replace.

| # | Engine | Label | Command |
|---|--------|-------|---------|
| 1 | Marketing | Ship This Week's Content | `/marketing-engine` |
| 2 | Sales | Research + Outreach | `/sales-engine` |
| 3 | Operations | Triage + SOPs | `/operations-engine` |
| 4 | Cash | Pull + Forecast | `/cash-engine` |
| 5 | Leadership | Morning Brief | `/leadership-engine` |

Short description for each (used in hover tooltip in interactive mode):

| Engine | Tooltip |
|--------|---------|
| Marketing | "Drafts 3 LinkedIn posts, 1 X thread, 1 newsletter — in your voice" |
| Sales | "Finds 10 prospects + drafts outreach aligned to your ICP" |
| Operations | "Triages inbox, writes SOPs from your patterns" |
| Cash | "Pulls Stripe, forecasts 90 days, flags anomalies" |
| Leadership | "Summarizes the last 7 days across every engine" |

---

## Meta Strings (small, often-reused)

| Context | String |
|---------|--------|
| Doc title | "{Name} — Business Brain" |
| Footer brand | "Purely Personal" |
| Footer URL | "purelypersonal.ai" |
| Save indicator (interactive) | "Saved" |
| Saving indicator (interactive) | "Saving..." |
| PDF export button | "Export PDF" |
| Copy link button | "Copy Link" |
| Share to LinkedIn | "Share" |
| Edit toggle (interactive) | "Edit" |
| Edit toggle active | "Done" |

---

## Headline Templates (per section)

The headline for each section uses the user's name — these are the exact patterns:

| Section | Headline template |
|---------|-------------------|
| Cover | `{{BRAIN_NAME}}` (just the name) |
| Voice | `How {{BRAIN_NAME}} Writes` |
| Business | `What {{BRAIN_NAME}} Sells` |
| ICP | `Who {{BRAIN_NAME}} Serves` |
| Competitors | `Who {{BRAIN_NAME}} Competes With` |
| Brand | `How {{BRAIN_NAME}} Looks` |
| AI Visibility | `How AI Sees {{BRAIN_NAME}}` |
| Pain Themes | `What Your People Are Actually Saying` |
| Actions | `Run Your AI C-Suite` |

If `{{BRAIN_NAME}}` is missing, fall back to "this business" ("What this business sells", etc.).

---

## Tone Sampler for Empty States

When writing new empty states (not listed above), match this exact tone:

**Good:**
> "You haven't named your ideal client. Answer three questions and we'll build a named persona with pain, desire, and objections."

**Bad (too corporate):**
> "Please configure your ICP to unlock downstream capabilities across our integrated content and sales pipeline."

**Bad (too cute):**
> "Uh oh! Your ICP is feeling lonely 😔 Let's give them a home!"

**Bad (too long):**
> "Before we can help you write posts that convert, we really need to understand who your audience is, what they care about, what they're struggling with, and what they desire — this is the foundation of everything."

Rule: a specific instruction + one sentence of "why" + a CTA. 2–3 sentences total, max.

---

## Placeholder Copy (only for dev/preview — never ship)

If you need placeholder content for a preview render (e.g. a workshop demo with no real Brain), use these explicit placeholders. They must be visually obvious so no one mistakes them for real data:

```
{{BRAIN_NAME}}      → "Your Name"
{{BRAIN_TAGLINE}}   → "Your one-line positioning"
{{OFFER}}           → "Your one-line offer statement"
{{ICP_NAME}}        → "Your Ideal Client, Role + Context"
{{COMP_NAME}}       → "Competitor A" / "Competitor B" / "Competitor C"
{{COMP_POSITIONING}} → "What they say on their homepage"
{{COMP_GAP}}        → "Where you can win against them"
```

These are obviously placeholder — they look empty even when filled. That's the point. Real renders should never reach the eye with these values present.

---

## Anti-patterns

- ❌ **Never render "Lorem ipsum"** or any classic placeholder prose. Use the explicit empty-state cards.
- ❌ **Never fabricate user data** to make a card look full. Empty state > fake data.
- ❌ **Never merge user-defined lists with defaults.** If the user provides 2 banned phrases, show exactly 2 — don't pad to 5 from the default list.
- ❌ **Never break canonical labels.** "Voice" is always "VOICE" in a label context. Never "Writing Style" or "Tone of Voice".
- ❌ **Never let the renderer's own copy drift into AI slop.** If you're about to write "seamlessly integrate with your ecosystem" — stop, rewrite.
