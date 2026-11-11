---
name: linkedin-carousel-builder
description: Build LinkedIn carousels using one of 2 production-tested Purely Personal templates. New Carousel (default. scroll-stopping cover + body + 4 CTA types) or Intent Carousel (5 strategic intents drive cover, flow, and CTA together). Each carousel is voice-matched, technical-terms preserved, and conversion-focused. Use when creating LinkedIn carousels, slide decks for social, or repurposing posts into multi-slide content. Triggers on "build a carousel", "LinkedIn carousel", "turn this into slides", "carousel about", "make a deck for LinkedIn".
version: 1.0.0
author: daniel-paul
tags: [linkedin, carousel, content, voice, ai-marketing-employee, slides]
---

# LinkedIn Carousel Builder

Two production-tested templates for LinkedIn carousels, sourced from Purely Personal's Content Prompts library. Every carousel has a scroll-stopping cover, intent-driven body flow, and conversion-focused CTA. voice-matched to the user.

This skill runs inside the AI Marketing Employee Project. Voice Profile auto-loads from Project Knowledge.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "build me a carousel about X" and you get 10 slides of generic content with a forgettable cover ("5 Tips for X!"), no through-line, and a final slide that says "Follow for more!". exactly like the 4 billion other AI-generated carousels published daily.

**This skill provides:**
1. **5 production-tested cover formulas**. calibrated against high-performing Purely Personal cohort carousels (Personal Achievement, Outcome-without-input, Contrarian, Tool+outcome, Number+promise)
2. **4 carousel flow patterns**. Problem→Solution / change / How-To / Framework. pick one and execute
3. **5 intent-driven variants** (Intent Carousel mode). each intent maps cover formula → body flow → CTA type, so all 3 reinforce each other
4. **4 CTA types**. Educational Follow / Lead Gen Comment / Industry Niche / Proof + CTA, each with formula + visual idea
5. **Technical terminology lock**. keeps client's industry terms exactly ("Voice DNA," "ICP," "EMR integration") instead of generic translations
6. **Slide format strict**. every slide enforced to 6-8 word title + 2-3 sentence body + ONE visual idea, designer-ready

**You can replicate this with ChatGPT if you:** memorize 5 cover formulas, 4 flow patterns, 5 intent mappings, 4 CTA types, anti-hallucination rules, AND remember to apply Voice Profile to every line. This skill does it in 60 seconds.

---

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| Voice Profile | AI Marketing Employee Project Knowledge | STOP. run `voice-profile-builder` first |
| Topic | User input | Ask: "What's the carousel about?" |
| Reference Context | User input or Project Knowledge | If anti-hallucination triggers, refuse to write |
| Number of Slides | User input | Default to 10 if not specified |
| Content Intent (Intent mode only) | User input | Ask: "Which of the 5 intents?" |
| CTA Type (New mode only) | User input or inferred | Default to Educational Follow |

---

## Mode

| Mode | Bundled prompt | Best for |
|------|-------------|----------|
| `new` (default) | `scripts/prompts/new-carousel.md` | Most carousels. Pick cover formula + flow pattern + CTA type independently. |
| `intent` | `scripts/prompts/intent-carousel.md` | When the carousel needs unified strategic intent (cover, flow, CTA all reinforce ONE goal). |
| `visual` ★ | Renders the carousel as a swipeable HTML preview with brand styling | Demos, screenshots, designer handoff. Looks like the final deck. |

**Default: `new`**. more flexibility. Switch to `intent` when the carousel needs to drive a specific action (Hard Selling / Soft Selling).

---

## Usage

```
/linkedin-carousel-builder
  --topic "How to set up an AI Marketing Employee in Claude"
  --slides 10
  --cta-type educational
  --mode new
```

Or natural language:
```
"Build a 10-slide intent carousel for Hard Selling about my GBI Online cohort."
```

---

## Process

### Phase 1. Validate inputs
1. Voice Profile present?
2. Topic + reference context sufficient?
3. Slide count specified (default 10)?
4. (Intent mode) Intent chosen?
5. (New mode) Cover formula + flow pattern + CTA type decided?

### Phase 2. Load bundled prompt
- `new` → `scripts/prompts/new-carousel.md`
- `intent` → `scripts/prompts/intent-carousel.md`

### Phase 3. Draft Cover Slide
Use one of the 5 cover formulas (New mode) OR the intent-specific cover formula (Intent mode). Verify:
- 4-8 word title
- 8-15 word subtitle
- Visual idea readable at thumbnail size
- Could ONLY have been written by this client

### Phase 4. Draft body slides
Follow one of the 4 flow patterns (New mode) OR the intent-specific flow (Intent mode). Each slide:
- 6-8 word title
- 2-3 sentence content (10-15 words each)
- ONE clear visual idea
- Bridging transition to next slide

### Phase 5. Draft CTA Slide
Pick CTA type (or use intent-mapped CTA). Apply formula:
- Educational Follow / Lead Gen Comment / Industry Niche / Proof + CTA

### Phase 6. QA check (8 questions)
1. Could the client ONLY have created this?
2. Cover stops scroll in <1 sec?
3. Every slide title 6-8 words?
4. Every body slide 2-3 sentences max?
5. Carousel follows ONE flow pattern consistently?
6. CTA is ONE clear ask with specific keyword?
7. All technical terms preserved as client uses them?
8. Would client publish without editing?

### Phase 7. Deliver
Markdown-formatted carousel ready for designer (or directly into Canva/Figma).

If `visual` mode: render swipeable HTML preview.

---

## Output Structure (text mode)

```
CAROUSEL: [Topic]
INTENT: [chosen, if intent mode]
FLOW PATTERN: [A/B/C/D, if new mode]
SLIDES: [N]

---

SLIDE 1 — COVER
Title: [...]
Subtitle: [...]
Visual: [...]

SLIDE 2 — [body label]
Title: [...]
Content: [...]
Visual: [...]

[... slides 3 through N-1 ...]

SLIDE N — CTA
Title: [...]
Content: [...]
Visual: [...]

---
QA: 8/8 ✓
Voice match: ✓
Technical terms preserved: ✓
```

## Output Structure (visual mode)

Single HTML artifact featuring:
- Swipeable slide preview (Aceternity-style horizontal scroll)
- Cover slide rendered as thumbnail mockup
- Slide counter (1/10, 2/10, etc.)
- Slide-by-slide flow visualization
- Visual idea descriptions per slide
- Brand-locked Purely Personal styling

See `scripts/render.py` + `scripts/template.html`.

---

## Examples

### Example 1. New mode · 10-slide · Educational CTA

**Input:** Topic: "How to set up an AI Marketing Employee in Claude." Slides: 10. Flow: How-To. CTA: Educational.

**Output:**
```
SLIDE 1 — COVER
Title: I Trained Claude To Write Like Me (5+ Calls Booked in 1 Week)
Subtitle: The exact 3-step process I use to install my AI Marketing Employee
Visual: Founder selfie + Claude logo with "writing in your voice" overlay

SLIDE 2 — The problem
Title: Most AI Content Sounds Like Everyone Else
Content: 4 billion AI posts published daily. Same models, same prompts, same vocabulary. Your fingerprint is missing.
Visual: Sea of identical posts, one highlighted

[... slides 3-9 covering the 3-step install + voice profile + invisibility diagnostic ...]

SLIDE 10 — CTA
Title: Want More Like This?
Content: Follow Daniel Paul for AI workflows that sound like YOU. New post every Tuesday.
Visual: Profile photo + follow button mockup
```

### Example 2. Intent mode · Hard Selling · 10-slide

**Input:** Topic: "GBI Online cohort opens June 12." Intent: Hard Selling. Slides: 10.

**Output:** Cover formula: "Want [Outcome] in [Timeframe]?" → Body flow: Problem → Benefits → Proof → Urgency → CTA Type: DM keyword.

### Example 3. Intent mode · Engagement · 10-slide

**Input:** Topic: "Why most personal brand advice is wrong." Intent: Engagement.

**Output:** Cover formula: "I Stopped [Common Practice] (Here's What Happened)" → Body flow: Wrong belief → Truth → Proof → Meaning → CTA Type: Follow + Niche.

---

## Chains With Other Skills

| Upstream | How |
|---|---|
| `voice-profile-builder` | Required. Voice Profile in Project Knowledge |
| `ai-marketing-employee` | Required. runs inside the Project |
| `linkedin-post-writer` | Can take a 4/4 post as input → expand into carousel |

| Downstream | How |
|---|---|
| `linkedin-cheatsheet-builder` | Same insights could become a cheatsheet. offer as next step |
| `invisibility-diagnostic` | Score each slide title individually for cover/CTA quality |

**Suggested chain after output:**
> *"Carousel built. Next: hand to designer (markdown is Canva-ready), OR run `linkedin-cheatsheet-builder` to turn the same insights into a saveable cheatsheet, OR run `linkedin-post-writer` to draft the text post that accompanies the carousel."*

---

## Limitations

- **Won't design slides.** Output is structured copy + visual descriptions. Designer (or Canva) builds the visuals.
- **Won't carousel without Voice Profile.** Same as post-writer. voice is required.
- **Won't mix intents (Intent mode).** Carousel must have ONE intent. Mixing dilutes the conversion.
- **Won't exceed 14 slides.** LinkedIn carousel best practice is 8-14. Beyond that, attention drops.

---

## Pro Tips

1. **Default to 10 slides.** Sweet spot for completion rate.
2. **Pair carousels with text posts.** Use `linkedin-post-writer` to draft the accompanying text post (50-100 chars) that goes in the post body when you upload the carousel.
3. **Cover slide is 80% of performance.** If the cover doesn't stop scroll, the other 9 slides don't matter.
4. **Reuse one CTA keyword across a campaign.** "voice" / "workflow" / "engine". same word on 5-10 carousels builds discoverability.
5. **Designer handoff:** the markdown output is paste-ready into Canva. The "Visual:" line per slide is the design brief.

---

## Quality Checklist (built into Phase 6)

- [ ] Cover stops scroll in <1 sec
- [ ] Cover title 4-8 words, subtitle 8-15 words
- [ ] Every body slide: 6-8 word title, 2-3 sentence content
- [ ] Flow pattern (or intent flow) is consistent
- [ ] CTA is ONE clear ask with specific keyword
- [ ] Technical terms preserved exactly
- [ ] Voice match: client could publish without editing

---

## Canva AI handoff

After generating the carousel content, append the Canva AI design prompt from `scripts/prompts/canva-carousel.md` to the output. The user copies the slide content into the `[PASTE CAROUSEL COPY HERE]` block, pastes the whole prompt into Canva AI, and gets a fully designed 5-7 slide carousel in under 5 minutes.

The Canva prompt is brand-locked to Purely Personal (red #e90d41, off-white #f7f7f8, near-black #0a0a0a, Rethink Sans + Inter + JetBrains Mono). It produces:
- Slide 1, dark cover with red accent
- Slides 2 to N-1, light body slides with red-underlined titles
- Slide N, red CTA background

Always emit this prompt as a separate "Copy Canva AI prompt" block at the bottom of the carousel output. Same pattern as `weekly-content-engine`.

---

## Bundled Files

```
~/.claude/skills/linkedin-carousel-builder/
├── SKILL.md
└── scripts/
    └── prompts/
        ├── new-carousel.md       (canonical Notion prompt 6)
        ├── intent-carousel.md    (canonical Notion prompt 7)
        └── canva-carousel.md     (premium designer prompt for Canva AI handoff)
```

---

*Built from Purely Personal's Content Prompts library. Calibrated against high-performing cohort carousels across 7 industries. Canva AI handoff shared with `weekly-content-engine`.*
