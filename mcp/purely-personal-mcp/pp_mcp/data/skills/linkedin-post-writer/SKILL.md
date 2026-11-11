---
name: linkedin-post-writer
description: Write LinkedIn text posts in the user's voice using one of 3 Purely Personal templates. Intent-Driven (default), Framework-Heavy (save-bait lists), or Story-Flow (vulnerable narrative). Every post is intent-anchored, voice-matched, anti-hallucination locked, and self-checked against the Invisibility Diagnostic before delivery. Use when writing any LinkedIn text post, drafting batch content, or producing posts for the AI Marketing Employee Project. Triggers on "write a LinkedIn post", "draft a post in my voice", "I need a post about", "framework post", "story post", "narrative post for LinkedIn".
version: 1.0.0
author: daniel-paul
tags: [linkedin, content, voice, ai-marketing-employee, posts, copywriting]
---

# LinkedIn Post Writer

Three templates for LinkedIn text posts, sourced from Purely Personal's Content Prompts library. Every post is anchored to ONE of 5 strategic intents, written in the user's captured voice, and scored 4/4 on the Invisibility Diagnostic before delivery.

This skill is one of the workflows the **AI Marketing Employee** (set up via `ai-marketing-employee`) runs inside the user's Claude Project. The Voice Profile auto-loads from Project Knowledge.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "write me a LinkedIn post about X" and you get a 4-paragraph fluff piece full of "leverage" and "unlock". sounds like every other AI-generated post on the platform. Generic structure, no intent, no voice fingerprint, no specific ask.

**This skill provides:**
1. **5 strategic intents**. every post anchored to ONE (Educating / Nurturing / Soft Selling / Hard Selling / Engagement) so the structure matches the goal, not just the topic
2. **3 templates**. bundled as full prompts, not just frameworks. Each template handles 4-5 intents with intent-specific hooks + body + close
3. **Anti-hallucination locked**. refuses to invent stories/quotes/numbers. Use only what's in Voice Profile or brain dump.
4. **Voice Profile integration**. auto-pulls Vocabulary, Beliefs, Rhythm from the AI Marketing Employee Project Knowledge
5. **4/4 Invisibility Diagnostic auto-check**. every post self-scored before delivery; rewrites failing dimensions
6. **Character-perfect**. 1300-1500 chars (about 200-250 words), the program standard

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
| `intent-driven` (default) | `prompts/intent-driven.md` | Most posts. 5 intents, all structures, default for AI Marketing Employee. |
| `framework-heavy` | `prompts/framework-heavy.md` | Save-bait numbered lists. improved for reposts. Educating / Engagement / Soft/Hard Selling. |
| `story-flow` | `prompts/story-flow.md` | Vulnerable narrative posts. Nurturing / Soft Selling / Engagement. Requires documented stories. |

**Default: `intent-driven`**. covers 80% of posts. Switch to `framework-heavy` for save-bait, `story-flow` when there's a real story to tell.

---

## Process

### Phase 1. Validate inputs

1. Check Voice Profile exists in Project Knowledge. If not → STOP, suggest `voice-profile-builder`.
2. Confirm intent (ask if ambiguous).
3. Confirm sufficient reference material to avoid hallucination (for Story-Flow specifically: require documented story).

### Phase 2. Select bundled prompt

Read the appropriate prompt file:
- `intent-driven` → `prompts/intent-driven.md`
- `framework-heavy` → `prompts/framework-heavy.md`
- `story-flow` → `prompts/story-flow.md`

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


---

## Output Structure (text mode)

```
[The post — 1300-1500 chars exactly]

---
[Author name] · [Industry] · [intent] · Variation: [mode]
Char count: 1487
Invisibility Diagnostic: 4/4 ✓ (Voice ✓ · POV ✓ · Specificity ✓ · Asking ✓)
```

## Examples

> **Illustrative only.** The names, numbers and results in the examples below are invented to show the format. Never reuse them. In real output use only facts from the operator's Business Brain or from the request, and leave a detail out rather than make one up.

### Example 1. Intent-driven · Nurturing (default mode)

**Input:** Topic: "I told a coaching client to pause her mindset content." Intent: Nurturing.

**Output (sample):**
```
I told a client last week to stop posting.

She had posted every day for six months. Mindset content, the kind everyone else writes. Eleven likes in total and no leads.

Her schedule was fine. Nothing she wrote sounded like her. She had performed "expert" for so long she forgot what she believed.

We rebuilt her voice profile in five minutes and put it in one Claude Project.

By Tuesday she published a post in her own voice. The first inbound DM in four months arrived that afternoon.

If your posts are not landing, read the last five out loud and count how many a stranger could have written.

Fix that once and keep it.

DM me "voice" and I will send you the worksheet I gave her.

---
(Illustrative sample, shortened. Real output is 1300-1500 characters, uses only facts from the Business Brain, and is scored with score_post.)
```

### Example 2. Framework-heavy · Educating

**Input:** Topic: "How to set up an AI Marketing Employee in Claude." Intent: Educating.

**Output:** [a 1300-1500 char numbered framework post following Variation A. 7-10 numbered steps, parallel structure, "(Save this + Repost if useful ♻️)" engagement marker, signature closing, P.S.]

### Example 3. Story-flow · Soft Selling

**Input:** Topic: "A client story with a measured result taken from the operator's own notes." Intent: Soft Selling.

**Output:** [a 1300-1500 char change story with "You have two choices today" close]

---

## Limitations

- **Won't invent stories.** If brain dump lacks documented stories for Story-Flow mode, the skill will refuse and ask for input.
- **Won't bypass the 4/4 check.** Posts that consistently fail 4/4 indicate a thin Voice Profile. run `voice-profile-builder` again with more inputs.
- **Won't write outside 1300-1500 chars.** This is the LinkedIn sweet spot. Don't request shorter (use Twitter) or longer (use newsletter).

---

## Pro Tips

1. **Default to `intent-driven` mode.** It's the most balanced. Only switch when you need a specific tone (Framework-Heavy for tactical, Story-Flow for emotional).
2. **Story-Flow requires real stories.** Don't try to fake one. The anti-hallucination rules will refuse to write.
3. **Use the same DM keyword across a campaign.** "voice" / "engine" / "workflow". pick one and reuse for 5-10 posts. Builds inbound discoverability.
4. **Run the post through the `de_ai_ify` tool as a second pass** if you suspect AI tells slipped through.
5. **The P.S. is the most-read line on LinkedIn.** Never waste it on a summary. Make it ONE clear idea.

---

## Quality Checklist (built into Phase 4)

- [ ] 1300-1500 chars exactly
- [ ] Hook is under 12 words and starts with I/You/If/When/quote
- [ ] Intent is consistent throughout (cover, body, close all match)
- [ ] No forbidden AI phrases (leverage, unlock, navigate, elevate, etc.)
- [ ] One specific named person + one specific number in first half
- [ ] P.S. present, ≤15 words, ONE clear idea
- [ ] 4/4 on Invisibility Diagnostic
- [ ] Could ONLY have been written by this client (Voice Profile match)

---
## Use in the Purely Personal connector


After the draft: Score with score_post, then polish_post and de_ai_ify. Turn the idea into a carousel with write_carousel or a cheatsheet with write_cheatsheet, or spread it across platforms with amplify_post.
