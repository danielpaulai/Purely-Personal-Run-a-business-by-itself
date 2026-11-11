---
name: voice-profile-builder
description: Build a Voice Profile from the 4 named inputs taught in the AI Employee Challenge (past posts, voice notes, DM/email replies, FAQ). Outputs a structured, paste-ready profile for Claude Projects Knowledge. Use when building or training the AI Marketing Employee, after collecting the 4 inputs, or when a thinner voice extraction needs to be hardened into a Project-ready format. Triggers on "build my voice profile", "AI Marketing Employee voice", "voice profile for Claude Projects", "extract my voice for the challenge", "4-input voice extraction".
version: 1.0.0
author: daniel-paul
tags: [voice, ai-employee-challenge, claude-projects, content, branding]
---

# Voice Profile Builder

The specific 4-input voice extraction method taught in Day 1 / Lesson 2 of the AI Employee Challenge. Built to feed straight into a Claude Project as Knowledge, no reformatting required.

---

## Why This vs `voice-extractor`?

Both extract voice. The differences:

| Aspect | `voice-extractor` (general) | `voice-profile-builder` (this) |
|---|---|---|
| **Inputs accepted** | Any writing samples | Strict 4-input schema (past posts, voice notes, DMs, FAQ) |
| **Output** | Voice Guide (descriptive) | Voice Profile (structured + paste-ready for Claude Projects Knowledge) |
| **Use case** | Brand voice docs, ghostwriter onboarding, team alignment | Powering the AI Marketing Employee Project specifically |
| **Mode default** | `standard` (descriptive guide) | `standard` (Project-ready profile) |
| **Validation** | "Does Version A sound like you?" | Score-test against `invisibility-diagnostic` on a generated sample post |
| **Chains with** | Anything | `ai-marketing-employee`, `first-post-coach`, `invisibility-diagnostic` |

**Use `voice-extractor` when:** building a brand voice guide for a writer / team / agency.

**Use `voice-profile-builder` when:** the user is in the AI Employee Challenge funnel and the output will become Project Knowledge inside Claude.

If unclear, ask: *"Is this voice going into a Claude Project (use voice-profile-builder) or a brand voice document for a team (use voice-extractor)?"*

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Paste your writing and ask "describe my voice". you get vague adjectives ("conversational, direct, witty"). Not actionable. Not paste-able into a Project. Not validated.

**This skill provides:**
1. **Strict 4-input schema**. every profile is built from the same 4 input types, making profiles comparable and improvable over time
2. **Project-ready output**. output is formatted to drop directly into Claude Projects Knowledge without editing
3. **v1-ships mindset**. accepts thin inputs (5 posts + 1 voice note minimum) and flags layer thinness, doesn't refuse to start
4. **Validation against `invisibility-diagnostic`**. generates a sample post in the profile's voice, scores it, fails loud if the profile isn't producing 4/4 posts
5. **Banned-words auto-extraction**. pulls AI tells the user *naturally avoids* + adds them to a "never use" list

---

## The 4 Inputs (Strict Schema)

| # | Input | Captures | Minimum v1 | Recommended |
|---|---|---|---|---|
| 1 | **Past posts they wrote themselves** | Vocabulary + format + rhythm | 5 posts | 20 posts |
| 2 | **Voice note transcripts** | Real rhythm + real beliefs | 1 note (90 sec) | 3 notes |
| 3 | **DM / email replies to clients** | Plain-English explaining voice | 5 replies | 10 replies |
| 4 | **Top FAQ + their answers** | Beliefs + signature phrases + structure | 5 Q+A | 10 Q+A |

**Below minimum:** flag the layer as thin, still produce v1 profile with a "REGENERATE WHEN YOU HAVE MORE [X]" note.

**Above recommended:** diminishing returns. don't add inputs beyond 20 posts / 5 notes / 10 DMs / 10 FAQs.

---

## Mode

Detect from context or ask: *"Quick v1, full Project-ready profile, or full + sample-post validation?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | Vocabulary section only (10 words + 5 banned + 5 phrases). 5-min build. | First pass during Lesson 2 live build |
| `standard` | Full 4-section profile (Vocabulary / Beliefs / Rhythm / Format) | Ready to paste into Claude Projects |
| `validated` (default) | Standard + generates 1 sample post → scores via `invisibility-diagnostic` → confirms 4/4 or flags gap | Production use, the version that earns its keep |

**Default: `validated`**. unless time-constrained (then `quick`). The validation step catches 60% of profiles that look right but produce 1/4 or 2/4 posts when used.

| Mode | What you get | Best for |
|---|---|---|
| `visual` ★ | top-tier HTML profile: animated word cloud (most-used + banned), belief cards, sentence-rhythm patterns, signature-phrase ticker (marquee), validation badge with sample post | Post-extraction deliverable. Attendees screenshot ("this is my voice captured") and share. Coordinator hands to founder as the final asset. |

**Visual mode usage:**
```bash
python ~/.claude/skills/voice-profile-builder/scripts/render.py \
  --in voice-profile-data.json \
  --out /tmp/voice-profile.html && open /tmp/voice-profile.html
```

The artifact features:
- Hero with founder name
- Animated word cloud (most-used words sized by frequency, banned words crossed out in red)
- 5 belief cards with source citations
- 3 rhythm patterns with real examples
- Horizontal scrolling marquee of signature phrases
- Validation card with sample post + 4/4 badge (if validated mode)
- Thinness flags as warning chips

See `scripts/template.html` for the full implementation.

---

## Usage

```
/voice-profile-builder
  --name "Sarah Chen"
  --industry "coach"
  --input1 "[past posts pasted here]"
  --input2 "[voice note transcript]"
  --input3 "[DM replies]"
  --input4 "[FAQ + answers]"
```

Or with mode:
```
/voice-profile-builder --mode quick
/voice-profile-builder --mode validated
```

If inputs come through chat as a single paste (the common case in the workbook), parse the section headers (`═══ INPUT 1 ═══` etc) automatically.

---

## Context Loading Gates

**Before extracting, validate:**

- [ ] Name (used to title the profile)
- [ ] Industry (used for sample-post validation in `validated` mode)
- [ ] Input 1, at least 5 posts OR 1,500 total words
- [ ] Input 2, at least 90 seconds of transcript (~250 words) OR explicitly flagged as missing
- [ ] Input 3, at least 5 replies OR explicitly flagged as missing
- [ ] Input 4, at least 5 Q+A pairs OR explicitly flagged as missing

**Below-minimum gate:**

If Input 1 has fewer than 5 posts AND fewer than 1,000 total words → STOP. Output:

> *"This is too thin to extract a reliable voice. Add 3 more past posts (even drafts work) and re-run. v1 needs at least 1,000 words of your own writing to produce a profile that doesn't sound like a generic coach/agency/founder."*

If only Input 1 is provided and 2-3-4 are missing → produce a `quick` mode v1 with thinness flags, suggest re-running when more inputs are ready.

---

## Process

### Phase 1. Input Audit

For each of the 4 inputs:
- Word count
- Authenticity check (is it real writing or templated marketing copy?)
- Recency check (are posts from this year, last year, or older?)

Output audit summary:
> *"Inputs: 18 posts (4,200 words, 2024–2025), 2 voice notes (380 words), 7 DM replies (820 words), 8 FAQ (1,100 words). Quality: high. Mode: validated."*

### Phase 2. Vocabulary Extraction

From Inputs 1 + 3 (highest signal):
- **Most-used words**. top 10 content words (exclude common stop words). Include rough frequency: "use (6×), engine (4×), build (12×)"
- **Banned words**. AI tells the user *naturally avoids* across all inputs. Default screen: `use, open up, big, help, path, go deep, handle, improve, solid, whole, fit, brainstorm, model, ecosystem, use, unleash`. If user never used any of these. list them as banned.
- **Signature phrases**. 5 phrases that appear 2+ times across inputs OR are clearly distinctive. Quote the source post number.

### Phase 3. Beliefs Extraction

From Inputs 2 + 4 (richer in opinion):
- Identify 5 non-negotiable opinions
- Use direct quotes where possible
- Reject vague beliefs ("I believe in quality"). only specific, defensible ones
- For each: quote source + 1-line context

### Phase 4. Rhythm Extraction

From Inputs 1 + 2 (best for prose rhythm):
- Identify 3 sentence patterns
- Examples: "1-2 word sentences for emphasis", "Question → answer → twist", "Long setup → short payoff"
- Quote one example per pattern from actual inputs

### Phase 5. Format Extraction

From Input 1 only (post format is post-specific):
- Top 3 opening templates (how posts start)
- Top 3 closing templates (how posts end)
- Quote one example per template

### Phase 6. Validation (`validated` mode only)

1. Compose a sample 150-word LinkedIn post using the extracted profile + a generic topic appropriate to the industry
2. Score the sample against `invisibility-diagnostic`
3. If score ≥ 3/4 → profile is valid, output normally
4. If score < 3/4 → profile is thin. Flag which dimensions failed and recommend specific input additions

### Phase 7. Self-Critique

Before final output:
- [ ] Are extracted phrases ACTUALLY from the inputs (quoted), or am I inferring?
- [ ] Did I avoid generic vocabulary that any human writes ("the", "we", "is")?
- [ ] Are the 5 beliefs SPECIFIC and DEFENSIBLE, not platitudes?
- [ ] Are rhythm examples from real inputs, or invented?
- [ ] If validated mode: did the sample post hit 3/4 or higher?

If any check fails: regenerate that section before final output.

---

## Output Structure (paste-ready for Claude Projects Knowledge)

```markdown
# Voice Profile · [Name]
## Built from [N posts] + [N voice notes] + [N DMs] + [N FAQ] · [date]

---

## VOCABULARY

### 10 most-used words
- engine (12× across inputs)
- system (9×)
- build (8×)
- [...]

### Banned (the AI tells you never use)
leverage, unlock, game-changing, empower, journey, dive deep, navigate,
optimize, robust, holistic, synergy, ideate, paradigm, ecosystem

### 5 signature phrases
- "Here's the thing" — appears in posts 3, 7, 14
- "That's the move" — closes posts 2, 9, 11
- [...]

---

## BELIEFS · the 5 non-negotiables

1. **Most personal brand advice is wrong.** Source: FAQ Q4 — "I don't believe
   in personal brand. I believe in personal documentation."
2. **Volume is for people without judgment.** Source: Voice note 1, minute 1:34.
3. [...]

---

## RHYTHM · 3 patterns

### Pattern 1: 1-2 word sentences for emphasis
Example (post 7): "Then she fired me. Worth it."

### Pattern 2: Question → declarative answer → twist
Example (post 3): "Why did it work? Because we stopped pretending. And we
finally said the price out loud."

### Pattern 3: [...]

---

## FORMAT · 3 openings + 3 closings

### Opening templates
1. "Last [day] I [action]." — post 2, 7, 11
2. "I just [action that sounds vulnerable]." — post 4, 9
3. "[Number] [units] ago, [setup]." — post 1, 6

### Closing templates
1. "DM me '[keyword]' for [thing]." — post 2, 4, 7, 11
2. "[Single declarative sentence].
   [Question]." — post 3, 9
3. "[...]" — [...]

---

## VALIDATION (if validated mode)

Sample post generated using this profile:
> "[150-word sample post]"

Scored against invisibility-diagnostic:
- Voice: 1
- POV: 1
- Specificity: 1
- Asking: 1
- TOTAL: 4/4 ✓

This profile is producing 4/4 posts. Ship it.

---

## USAGE INSTRUCTIONS

1. Copy this entire Voice Profile (above the line)
2. Open Claude → Projects → New Project (or existing "AI Marketing Employee")
3. Click "Edit Knowledge" → paste this as a new knowledge file
4. Save the Project

Every future post written inside this Project will match this voice.

---

## THINNESS FLAGS (if any)

⚠ Voice notes layer: only 1 note (180 words). Add 2 more — that's where beliefs and rhythm live.
⚠ FAQ layer: thin (3 Q+A). Add 5 more to sharpen the Beliefs section.

Re-run this skill when you have more inputs.
```

---

## Examples

### Example 1 · Strong Inputs (Coach)

**Inputs provided:**
- 22 LinkedIn posts (5,400 words, 2024–2025)
- 4 voice notes (~750 words transcribed)
- 12 DM replies to clients
- 9 FAQ + answers

**Output excerpt:**
```
# Voice Profile · Sarah Chen
## Built from 22 posts + 4 voice notes + 12 DMs + 9 FAQ · 2026-05-21

VOCABULARY
- 10 most-used: client (38×), system (24×), build (22×), fire (11×),
  pricing (17×), structure (15×), pause (8×), audit (12×), Tuesday (6×),
  proof (9×)
- Banned: leverage, unlock, game-changing, empower, journey, dive deep,
  navigate, optimize, robust, holistic, synergy
- Signature phrases:
  - "Pause the [thing]" (5×) — appears posts 3, 7, 11, 14, 19
  - "That's not the problem" (4×) — posts 2, 8, 12, 18
  - "Tuesday I" (3×) — posts 1, 9, 15

BELIEFS
1. Most coaches teach mindset before sales — backwards.
   Source: FAQ Q2: "If you can't sell, mindset is a luxury."
2. Pricing is the leverage point most coaches never touch.
   Source: Voice note 2, 2:14: "I've never had a client whose problem
   wasn't pricing. Never."
3. Firing a client is a strategic act.
   Source: Post 7: "I fired my best client last quarter. Best
   business decision I made in 18 months."
[...]
```

### Example 2 · Thin Inputs (E-commerce founder)

**Inputs provided:**
- 6 LinkedIn posts (1,200 words)
- 0 voice notes (skipped)
- 0 DMs (skipped)
- 3 FAQ + answers

**Output (with thinness flags):**
```
# Voice Profile · Marcus Webb (v1 · thin)
## Built from 6 posts + 0 voice notes + 0 DMs + 3 FAQ · 2026-05-21

VOCABULARY
- 10 most-used: founder (8×), SKU (6×), launch (5×), customer (9×),
  margin (4×), [...]
- Banned: [defaults — no user-specific banned words confidently identified]
- Signature phrases: [only 2 reliably extracted — re-run when you have more]
  - "Almost cut" (2×) — posts 3, 5
  - "Founder math" (2×) — posts 1, 4

BELIEFS (thin — only 2 confidently extracted)
1. Founder voice beats brand voice. Source: Post 3.
2. Margin is a story problem before it's a cost problem. Source: FAQ Q1.

⚠ THINNESS FLAGS:
- Voice notes layer: MISSING. Add at least 1 voice note (90 sec).
  Beliefs section will stay thin without it.
- DMs layer: MISSING. Add 5 client DM replies. Vocabulary will stay thin.
- FAQ layer: thin (3). Add 4-5 more for sharper Beliefs section.

Validation score on sample post: 2/4 (Voice ✓, POV ✓, Specificity ✗, Asking ✗)
→ The thinness of input layers is producing weak Specificity. Add Voice
  notes (where you talk about real moments) to fix.

Re-run this skill in 24 hours when you've added the missing inputs.
```

### Example 3 · `quick` mode (live build during Lesson 2)

**Inputs provided:** 5 LinkedIn posts only (1,300 words)

**Output:**
```
# Voice Profile · Priya Sharma (v1 · quick)

VOCABULARY ONLY (other sections require Inputs 2-4)

- 10 most-used: agency (14×), team (8×), creator (7×), AI (12×),
  workflow (6×), founder (9×), fired (4×), built (11×), output (5×),
  meeting (7×)
- Banned: leverage, unlock, game-changing, empower, journey, dive deep,
  optimize, robust, holistic, synergy, ideate
- Signature phrases:
  - "We fired" (3×) — posts 1, 3, 5
  - "Output [tripled/doubled/N×]" (3×) — posts 1, 4, 5
  - "Founder-led" (2×) — posts 2, 4

NEXT: re-run in `validated` mode after recording a voice note and
pasting 5 DM replies. The 3 missing input layers are why this is
vocabulary-only.
```

---

## Chains With Other Skills

| Upstream | How |
|---|---|
| User input via `workbook` | Workbook collects the 4 inputs and passes them as a single paste to this skill |

| Downstream | How |
|---|---|
| `ai-marketing-employee` | Uses this profile as Project Knowledge during the 3-step install |
| `invisibility-diagnostic` | Validated mode uses this skill to score the sample post |
| `first-post-coach` | Loads this profile to coach the user toward 4/4 posts in their voice |

**Suggested chain after output:**
> *"Profile built. Next: run `ai-marketing-employee` to install it as a Claude Project, or paste the profile into your existing Project Knowledge."*

---

## Limitations

- **Won't fix bad input.** Garbage in = generic profile out. The minimum-input gate exists for a reason.
- **Won't validate against the user's perception.** The profile might score 4/4 on sample posts but still feel "off" to the user. That's an Input 2 (voice note) problem. add more rambling.
- **Won't extract beliefs from polished marketing copy.** If Input 1 is all edited LinkedIn posts and no voice notes, the Beliefs section will be weak.
- **Won't cross domains.** A profile built from B2B SaaS writing won't translate to consumer fitness content. Build separate profiles per domain.

---

## Pro Tips

1. **Always include at least one voice note.** Even 60 seconds. It's the single highest-use input for the Beliefs and Rhythm layers.
2. **DMs from clients > emails > formal copy.** Authenticity rank.
3. **If your "signature phrases" feel generic. your inputs are too polished.** Re-collect from raw Slack messages.
4. **Re-run quarterly.** Your voice drifts. The profile is a snapshot. refresh it.
5. **Don't edit the output before pasting into Claude.** The structure is calibrated. Editing weakens it.

---

*Built for Day 1 / Lesson 2 of the AI Employee Challenge. Differentiated from voice-extractor by output format and Claude Projects integration.*
