---
name: content-visual-builder
description: Produce publish-ready visual content cards for LinkedIn, X, Instagram, and Newsletter in the user's voice. Reads BUSINESS-BRAIN.md for voice rules, banned phrases, hook patterns, and positioning. Triggers on "write a post", "make a LinkedIn card", "X thread visual", "newsletter visual", "carousel from this", "4-platform post", "content card", "make this a post", "ship this to LinkedIn", "turn this into content", or any request to produce visual content assets for social/newsletter distribution. Also triggers when someone says "run content machine" or "ship today's content".
---

# Content Visual Builder

Produce publish-ready content cards in four platform styles from a single input. Reads the user's `BUSINESS-BRAIN.md` for voice, hooks, and banned phrases — so the output sounds like them, not like AI.

## How This Skill Works

1. Read `BUSINESS-BRAIN.md` voice section → extract tone, banned phrases, hook patterns
2. Read the user's brief (topic, angle, or brain-dump)
3. Draft post copy that obeys the voice rules
4. Pick the platform template from [references/code-templates.md]
5. Render 1 to 4 platform variants — user's choice
6. Validate against voice rules + platform specs
7. Emit an HTML artifact with the variants side-by-side

**ALWAYS read `BUSINESS-BRAIN.md` BEFORE writing copy.** Generic copy produces generic output — the Brain is what makes this skill work.

## Reference Files

| File | What It Contains | When to Read |
|------|-----------------|--------------|
| [references/code-templates.md] | HTML templates for LinkedIn, X, Instagram, Newsletter post cards | ALWAYS — primary build tool |
| [references/platform-specs.md] | Dimensions, char limits, safe zones, image aspect ratios per platform | When sizing or cropping |
| [references/voice-application.md] | How to apply BUSINESS-BRAIN.md voice rules to each platform's constraints | ALWAYS — before drafting copy |
| [references/design-system.md] | Platform colors, typography, spacing (shared with other PP skills) | When customizing |
| [references/visual-catalog.md] | Catalog of 8 card types: single post, carousel, quote card, stat card, cheatsheet, CTA card, thread preview, newsletter header | When choosing card type |

## The Four Platforms

| Platform | Color | Dimensions | Char limit | Vibe |
|----------|-------|------------|------------|------|
| LinkedIn | `#0A66C2` | 1200×628 (landscape) or 1080×1080 (square) | 3,000 chars | Professional, narrative, long-form |
| X | `#0F1419` | 1600×900 (landscape) or 1080×1080 (square) | 280 chars/post | Punchy, conversational, threadable |
| Instagram | `#833AB4 → #FCB045` (gradient) | 1080×1080 (square) or 1080×1350 (portrait) | 2,200 chars | Visual-first, emoji-friendly, aesthetic |
| Newsletter | `#E8D9C5` (warm cream) | Flexible width | No limit | Editorial, longer-form, quiet |

## The 8 Card Types

1. **Single post card** — one post, one platform
2. **Four-platform grid** — same content, 4 platform renders side-by-side
3. **Carousel** — multi-slide sequence (LinkedIn/Instagram)
4. **Quote card** — pull-quote hero, minimal design
5. **Stat card** — one big number + context
6. **Cheatsheet** — checklist or framework (PDF-exportable)
7. **Thread preview** — X thread tweets stacked vertically
8. **Newsletter header** — email hero card + preview text

## Workflow

### Step 1: Load the Brain
Read `BUSINESS-BRAIN.md` (look in project root, `shared/`, or path provided). If missing, ask user to run `/build-my-brain` first. Do NOT fabricate voice rules.

### Step 2: Extract Voice Essentials
From the Brain, pull:
- Tone description (1–3 sentences)
- Banned phrases (never include in output)
- Hook patterns (5 formulas)
- Example openings (3+ real excerpts)
- Name + ICP (for context)

### Step 3: Understand the Ask
- **Topic:** what is this post about?
- **Angle:** what's the take/contrarian stance?
- **Platform(s):** which of the 4?
- **Card type:** which of the 8?
- If ambiguous: default to single post card on LinkedIn.

### Step 4: Draft Copy
Apply voice rules from [references/voice-application.md]:
- Start with one of the hook patterns from the Brain
- Short sentences. One idea per line.
- Use specifics (numbers, names, amounts) from the Brain's Business Card if relevant
- End with a question (LinkedIn/X) or a bullet list (newsletter)
- Never include any banned phrase

### Step 5: Render the Card
Copy the platform template from [references/code-templates.md]. Fill `{{VARIABLES}}`. Validate against platform specs (char limits, safe zones).

### Step 6: Voice Validation
Before emitting, run this checklist:
- [ ] No banned phrases present
- [ ] Opening matches one of the 5 hook patterns
- [ ] Sentences are short (≤18 words average)
- [ ] Specifics used (no "many", "lots", "several")
- [ ] No em-dashes (unless user's voice rules allow)
- [ ] P.S. present if LinkedIn (Danny's pattern) + ends with question
- [ ] Char count within platform limit

### Step 7: Emit
Single-card mode: one HTML card.
Grid mode: all 4 platforms side-by-side with tab navigation.
Carousel mode: slides + navigation.

## Quick Triggers

| User Says | Generate |
|-----------|----------|
| "make a LinkedIn post about X" | Single card, LinkedIn, post type |
| "4-platform post on X" | Grid mode, all 4 platforms, post type |
| "X thread on Y" | Thread preview, 5–8 tweets |
| "newsletter promo for X" | Newsletter header + 3-paragraph body |
| "quote card: [quote]" | Quote card, LinkedIn default |
| "stat card: [number] [context]" | Stat card, LinkedIn square |
| "cheatsheet on X" | Cheatsheet card, LinkedIn carousel or PDF |
| "run content machine" | Brain-dump → 3 LinkedIn posts + 1 X thread + 1 newsletter |

## Chaining with Other Skills

- **`business-brain-renderer`** ← source of voice rules and positioning
- **`linkedin-profile-optimizer`** → feeds voice data into the Brain
- **`apify-linkedin`** → scrapes real posts to fine-tune voice
- **`de-ai-ify`** → runs on every draft as a final clean pass

## Anti-patterns

- ❌ Never write copy without reading BUSINESS-BRAIN.md first. Generic copy defeats the skill.
- ❌ Never use em-dashes (`—`) unless user's voice rules explicitly allow.
- ❌ Never exceed platform char limits. Truncate or split into thread/carousel.
- ❌ Never mix platform colors inside one card. One card = one platform aesthetic.
- ❌ Never generate 4 platform variants if user asked for 1. Respect scope.
- ❌ Never skip the voice-validation checklist. Ship broken voice = skill looks useless.
