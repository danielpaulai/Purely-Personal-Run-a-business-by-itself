---
name: linkedin-post-writer
description: Write LinkedIn text posts in the user's voice using one of 3 production-tested Purely Personal templates. Intent-Driven (default), Framework-Heavy (save-bait lists), or Story-Flow (vulnerable narrative). Every post is intent-anchored, voice-matched, anti-hallucination locked, and self-checked against the Invisibility Diagnostic before delivery. Use when writing any LinkedIn text post, drafting batch content, or producing posts for the AI Marketing Employee Project. Triggers on "write a LinkedIn post", "draft a post in my voice", "I need a post about", "framework post", "story post", "narrative post for LinkedIn".
version: 1.0.0
author: daniel-paul
tags: [linkedin, content, voice, ai-marketing-employee, posts, copywriting]
---

# LinkedIn Post Writer

Three production-tested templates for LinkedIn text posts, sourced from Purely Personal's Content Prompts library. Every post is anchored to ONE of 5 strategic intents, written in the user's captured voice, and scored 4/4 on the Invisibility Diagnostic before delivery.

This skill is one of the workflows the **AI Marketing Employee** (set up via `ai-marketing-employee`) runs inside the user's Claude Project. The Voice Profile auto-loads from Project Knowledge.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "write me a LinkedIn post about X" and you get a 4-paragraph fluff piece full of "use" and "open up". sounds like every other AI-generated post on the platform. Generic structure, no intent, no voice fingerprint, no specific ask.

**This skill provides:**
1. **5 strategic intents**. every post anchored to ONE (Educating / Nurturing / Soft Selling / Hard Selling / Engagement) so the structure matches the goal, not just the topic
2. **3 production-tested templates**. bundled as full Notion-extracted prompts, not just frameworks. Each template handles 4-5 intents with intent-specific hooks + body + close
3. **Anti-hallucination locked**. refuses to invent stories/quotes/numbers. Use only what's in Voice Profile or brain dump.
4. **Voice Profile integration**. auto-pulls Vocabulary, Beliefs, Rhythm from the AI Marketing Employee Project Knowledge
5. **4/4 Invisibility Diagnostic auto-check**. every post self-scored before delivery; rewrites failing dimensions
6. **Character-perfect**. 1300-1500 chars exactly (LinkedIn algorithm sweet spot)

**You can replicate this with ChatGPT if you:** memorize all 3 templates × 5 intents × hook patterns × forbidden phrases, manually track character count, manually score against 4 dimensions, manually check against your Voice Profile. This skill does it in 30 seconds.

---

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| Voice Profile | AI Marketing Employee Project Knowledge | STOP. run `voice-profile-builder` first |
| Topic | User input | Ask: "What's the post about?" |
| Content Intent | User input or inferred from topic | Ask: "Educating / Nurturing / Soft Selling / Hard Selling / Engagement?" |
| Brain Dump / Reference | User input or Project Knowledge | If anti-hallucination triggers, refuse to write |

---

## Mode

Detect from context or ask: *"Intent-driven (default), framework-heavy (save-bait list), or story-flow (vulnerable narrative)?"*

| Mode | Bundled prompt | Best for |
|------|-------------|----------|
| `intent-driven` (default) | `scripts/prompts/intent-driven.md` | Most posts. 5 intents, all structures, default for AI Marketing Employee. |
| `framework-heavy` | `scripts/prompts/framework-heavy.md` | Save-bait numbered lists. improved for reposts. Educating / Engagement / Soft/Hard Selling. |
| `story-flow` | `scripts/prompts/story-flow.md` | Vulnerable narrative posts. Nurturing / Soft Selling / Engagement. Requires documented stories. |
| `visual` ★ | Renders the finished post as a LinkedIn-mockup HTML artifact with branded styling | Demos, screenshots, deliverables. Looks like a real LinkedIn post. |

**Default: `intent-driven`**. covers 80% of posts. Switch to `framework-heavy` for save-bait, `story-flow` when there's a real story to tell.

---

## Usage

```
/linkedin-post-writer
  --topic "I told a client to stop posting daily"
  --intent nurturing
  --brain-dump "[paste your brain dump or 'use Project Knowledge']"
  --mode story-flow
```

Or natural language inside the AI Marketing Employee Project:
```
"Write a story-flow post in my voice about the time I told a client to stop posting daily."
```

---

## Process

### Phase 1. Validate inputs

1. Check Voice Profile exists in Project Knowledge. If not → STOP, suggest `voice-profile-builder`.
2. Confirm intent (ask if ambiguous).
3. Confirm sufficient reference material to avoid hallucination (for Story-Flow specifically: require documented story).

### Phase 2. Select bundled prompt

Read the appropriate prompt file:
- `intent-driven` → `scripts/prompts/intent-driven.md`
- `framework-heavy` → `scripts/prompts/framework-heavy.md`
- `story-flow` → `scripts/prompts/story-flow.md`

The bundled prompt is the canonical Purely Personal template. Follow it exactly. including hook formulas, post structures, writing standards, and AI pattern avoidance.

### Phase 3. Write the post

Apply the bundled prompt with:
- The user's Voice Profile loaded as voice reference
- The provided topic and intent
- The brain dump as the only allowed source of stories/numbers/names
- Character target: 1300-1500

### Phase 4. Self-check against Invisibility Diagnostic (mandatory)

Before delivering, internally score the post 0-4 using `invisibility-diagnostic` logic:
- **Voice (1pt):** Could 50 others have written this? If yes, the Voice Profile didn't shape it enough.
- **POV (1pt):** Does it take a clear side?
- **Specificity (1pt):** Real name + real number in first half?
- **Asking (1pt):** Specific keyword DM invitation in last 2 lines?

If < 4/4 → rewrite the weakest dimension and re-score (max 2 rewrites). If still < 4/4, deliver with a note flagging which dimension is thin and why.

### Phase 5. Deliver

Just the post. No preamble. Mark character count at the bottom.

If `visual` mode: also render the LinkedIn-mockup HTML artifact via `scripts/render.py`.

---

## Output Structure (text mode)

```
[The post — 1300-1500 chars exactly]

---
[Author name] · [Industry] · [intent] · Variation: [mode]
Char count: 1487
Invisibility Diagnostic: 4/4 ✓ (Voice ✓ · POV ✓ · Specificity ✓ · Asking ✓)
```

## Output Structure (visual mode)

Single HTML artifact featuring:
- LinkedIn-style post mockup with author photo placeholder
- The full post text rendered as it appears on LinkedIn
- Live character counter
- 4-dimension diagnostic score visualization (animated)
- Brand-locked Purely Personal styling (dark mode, paper grid bg)
- "Ship it" button mockup at 4/4

See `scripts/render.py` + `scripts/template.html`.

---

## Examples

### Example 1. Intent-driven · Nurturing (default mode)

**Input:** Topic: "I told a coaching client to pause her mindset content." Intent: Nurturing.

**Output (sample):**
```
I told a client last week to stop posting.

She'd been posting daily for 6 months. Mindset content. The kind everyone else writes.

11 likes total. Zero leads.

The problem wasn't her schedule.

It was that nothing she wrote sounded like her. She'd been performing "expert" so long she forgot what she actually believed.

We rebuilt her voice profile in 5 minutes. Set up her AI Marketing Employee in Claude. One Project. Voice locked.

By Tuesday she shipped her first post in her real voice. First inbound DM in 4 months. Booked the call.

Real talk: voice isn't decoration. It's the foundation.

If you're posting and nothing's landing — it's not your schedule. It's not the algorithm. It's that you sound like everyone else.

Fix that once. Keep it forever.

DM me 'voice' for the worksheet I gave her.

---
Daniel Paul · AI Trainer · nurturing · Variation: story-flow
Char count: 1421
Invisibility Diagnostic: 4/4 ✓
```

### Example 2. Framework-heavy · Educating

**Input:** Topic: "How to set up an AI Marketing Employee in Claude." Intent: Educating.

**Output:** [a 1300-1500 char numbered framework post following Variation A. 7-10 numbered steps, parallel structure, "(Save this + Repost if useful ♻️)" engagement marker, signature closing, P.S.]

### Example 3. Story-flow · Soft Selling

**Input:** Topic: "Mehsum Sayani's 1.9M impressions in 4 months." Intent: Soft Selling.

**Output:** [a 1300-1500 char change story with "You have two choices today" close]

---

## Chains With Other Skills

| Upstream | How |
|---|---|
| `voice-profile-builder` | Required. Voice Profile must exist in Project Knowledge |
| `ai-marketing-employee` | Required. this skill runs INSIDE the Project that AI Marketing Employee set up |

| Downstream | How |
|---|---|
| `invisibility-diagnostic` | Auto-called in Phase 4 to score before delivery |
| `first-post-coach` | If user is in Game 1 mode, route through First Post Coach instead |
| Future: `content-multiplier` (Day 2) | Takes the post output and multiplies into 5 posts + carousel + DMs |

**Suggested chain after output:**
> *"Post written and scored 4/4. Next: paste into your scheduler, OR run `linkedin-carousel-builder` to turn this idea into a carousel, OR run `content-multiplier` to multiply into a week of content."*

---

## Limitations

- **Won't invent stories.** If brain dump lacks documented stories for Story-Flow mode, the skill will refuse and ask for input.
- **Won't bypass the 4/4 check.** Posts that consistently fail 4/4 indicate a thin Voice Profile. run `voice-profile-builder` again with more inputs.
- **Won't write outside 1300-1500 chars.** This is the LinkedIn sweet spot. Don't request shorter (use Twitter) or longer (use newsletter).
- **Won't write multiple posts per call.** ONE post per invocation. For batch, run multiple times or use `content-multiplier`.

---

## Pro Tips

1. **Default to `intent-driven` mode.** It's the most balanced. Only switch when you need a specific tone (Framework-Heavy for tactical, Story-Flow for emotional).
2. **Story-Flow requires real stories.** Don't try to fake one. The anti-hallucination rules will refuse to write.
3. **Use the same DM keyword across a campaign.** "voice" / "engine" / "workflow". pick one and reuse for 5-10 posts. Builds inbound discoverability.
4. **Run the post through `de-ai-ify` as a second pass** if you suspect AI tells slipped through.
5. **The P.S. is the most-read line on LinkedIn.** Never waste it on a summary. Make it ONE clear idea.

---

## Quality Checklist (built into Phase 4)

- [ ] 1300-1500 chars exactly
- [ ] Hook is under 12 words and starts with I/You/If/When/quote
- [ ] Intent is consistent throughout (cover, body, close all match)
- [ ] No forbidden AI phrases (use, open up, handle, improve, etc.)
- [ ] One specific named person + one specific number in first half
- [ ] P.S. present, ≤15 words, ONE clear idea
- [ ] 4/4 on Invisibility Diagnostic
- [ ] Could ONLY have been written by this client (Voice Profile match)

---

## Bundled Files

```
~/.claude/skills/linkedin-post-writer/
├── SKILL.md                    (this file)
└── scripts/
    ├── render.py               (JSON → LinkedIn-mockup HTML for visual mode)
    ├── template.html           (visual artifact template)
    └── prompts/
        ├── intent-driven.md    (canonical Notion prompt 11)
        ├── framework-heavy.md  (canonical Notion prompt 12)
        └── story-flow.md       (canonical Notion prompt 13)
```

---

*Built from Purely Personal's Content Prompts library (Notion). Production-tested across coach, agency, e-commerce, B2B, SaaS, fitness, real-estate cohorts. One of the daily-driver workflows of the AI Marketing Employee.*
