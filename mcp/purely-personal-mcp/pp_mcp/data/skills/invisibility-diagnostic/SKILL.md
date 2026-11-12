---
name: invisibility-diagnostic
description: Score any social post 0-4 on the Invisibility Diagnostic (Voice, POV, Specificity, Asking) and return a one-line fix per missing dimension. Use when scoring social posts, auditing content, before publishing anything, or grading another writer's work. Triggers on "score this post", "is this invisible", "diagnose my post", "rate my content", "why isn't this getting engagement", or pasted social copy with "what do you think?".
version: 1.0.0
author: daniel-paul
tags: [content, audit, voice, scoring, social-media]
---

# Invisibility Diagnostic

Score any social post on 4 dimensions in 30 seconds. Return total, tier, and a one-line fix per missing dimension.

Run it on every post before you publish. The point is the pre-publish edit.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "is this post good?" and you get vague flattery ("Great post! It's clear and engaging."). Ask "score it out of 10" and you get inconsistent numbers with no methodology. Ask "what should I fix?" and you get 15 suggestions with no priority. None of it produces a 4/4 post on the next attempt.

**This skill provides:**
1. **Single deterministic scoring system**. 4 dimensions, 1 point each, max 4. Same post = same score every time.
2. **One-line fixes, not 15 suggestions**. exactly what to change in one line to add the missing point.
3. **Tier labeling that maps to outcomes**. 0-1 invisible, 2 noise, 3 visible, 4 magnetic. You know if it's worth publishing.
4. **Four fixed binary tests**. Voice, POV, Specificity and Asking each score 0 or 1, so results are repeatable, not opinion.
5. **Worked examples** across industries show what a pass and a fail look like.

**You can replicate this with ChatGPT if you:** Memorize the 4 dimensions, train yourself to score consistently across 200+ reps, build a fix library per dimension × industry, and never let yourself drift toward subjective "I liked it." This skill enforces the discipline.

---

## The 4 Dimensions

| # | Dimension | The 1-point test | Why it matters |
|---|---|---|---|
| 1 | **Voice** | Could 50 others in this niche have written this? *No = 1pt. Yes = 0.* | Without a fingerprint, the post is interchangeable. Interchangeable = scrolled. |
| 2 | **POV** | Does it take a clear side, or just explain? *Side = 1pt. Explain = 0.* | Explaining content earns reads but no remember. Sides earn replies. |
| 3 | **Specificity** | Real name + real number in the first half? *Yes = 1pt. No = 0.* | "Sarah · 67%" beats "a client · a lot." Specificity is the proof in the post. |
| 4 | **Asking** | Specific keyword DM invitation in last 2 lines? *Yes = 1pt. No = 0.* | "Hope this helps" never closed a deal. "DM me 'engine' for the doc" closes 3/week. |

## Scoring Tiers

| Score | Tier | What it means |
|---|---|---|
| **0–1** | Invisible | Algorithm + humans both scroll. Don't publish. |
| **2** | Background noise | Maybe a like from your mum. Worth a one-line edit. |
| **3** | Visible | Earns reads, occasional comment. Publishable. |
| **4** | Magnetic | The post that gets the DM. Ship it. |

---

## Mode


| Mode | What you get | Best for |
|------|-------------|----------|
| `score-only` | Numerical score + tier label. No suggestions. | Bulk scoring (homework review across 50+ posts) |
| `score-with-fix` (default) | Full score breakdown + one-line fix per missing dimension | Pre-publish check on a single post |
| `score-rewrite-rescore` | Score → rewrite to 4/4 → score the rewrite to confirm | When the user wants the finished post, not just feedback |

**Default: `score-with-fix`**. fastest path from "draft I'm not sure about" to "draft I can ship.**


---

## Process

### Phase 1. Read & Tokenize

1. Strip platform formatting (LinkedIn line breaks, emoji noise)
2. Identify first half vs second half (by character count, not line count)
3. Identify the last 2 lines

### Phase 2. Score Each Dimension

For each of the 4 dimensions:
- Apply the binary test (see table above)
- Score 0 or 1
- Capture the *reason* (which gets used in the fix line)

### Phase 3. Calculate & Tier

- Total: 0-4
- Tier: invisible / noise / visible / magnetic (see table)

### Phase 4. Generate Fix Lines (`score-with-fix` mode)

For each dimension that scored 0:
- Generate ONE LINE fix specific to this post + (if provided) industry
- Fix must be additive, not destructive (don't rewrite the post. add the missing element)

### Phase 5. Rewrite & Re-score (`score-rewrite-rescore` mode only)

- Apply all fixes
- Output rewritten post
- Re-run Phase 2-3 to confirm 4/4
- If still < 4, flag for human review

---

## Output Structure

### `score-with-fix` mode (default):

```
SCORE: 2/4 — Background noise

DIAGNOSIS:
✗ Voice: 0 — Reads like generic "tips" content. Could be 50 coaches.
✓ POV: 1 — Takes a side on volume vs voice.
✗ Specificity: 0 — No named example or number in first half.
✓ Asking: 1 — "DM 'workflow'" is clear.

TO GET TO 4/4 (2 edits, one line each):

VOICE FIX:
  Replace opening with a first-person moment: "Last Tuesday I told a coaching
  client to stop posting. She'd posted daily for 6 months. 11 likes total."

SPECIFICITY FIX:
  Add one number to the second sentence: "Most coaching clients I see waste
  6 to 9 months on volume before they fix voice."

PROJECTED SCORE AFTER FIXES: 4/4 — Magnetic
```

### `score-only` mode (bulk):

```
SCORE: 2/4 — Background noise
Voice: 0 | POV: 1 | Specificity: 0 | Asking: 1
```

### `score-rewrite-rescore` mode:

```
ORIGINAL SCORE: 2/4 — Background noise
[diagnosis as above]

REWRITTEN POST (4/4):
"[full rewritten post]"

REWRITE SCORE: 4/4 — Magnetic ✓
Voice: 1 | POV: 1 | Specificity: 1 | Asking: 1

CHANGES MADE:
- Added first-person opening (voice +1)
- Added named example "coaching client + 6 months + 11 likes" (specificity +1)
- Preserved POV + asking (no change)
```

---

## Examples

> **Illustrative only.** The names, numbers and results in the examples below are invented to show the format. Never reuse them. In real output use only facts from the operator's Business Brain or from the request, and leave a detail out rather than make one up.

### Example 1: Coach. Invisible (0/4)

**Input:**
> "5 mindset shifts that will change your coaching practice this year. Number 1 is the biggest one most coaches miss. Are you ready to open up your full potential? Comment below!"

**Output:**
```
SCORE: 0/4 — Invisible

DIAGNOSIS:
✗ Voice: 0 — Could be any coach. AI tells present ("transform", "unlock", "full potential").
✗ POV: 0 — No side taken. Pure tease.
✗ Specificity: 0 — No name, no number, no concrete moment.
✗ Asking: 0 — "Comment below" is not a specific keyword DM invitation.

TO GET TO 4/4 (4 edits, one line each):

VOICE FIX: Replace AI vocabulary. "5 mindset shifts that will transform" → "5 things I tell every coaching client in week 1."

POV FIX: Pick a side. Replace "biggest one most coaches miss" with a contrarian: "Most coaches teach mindset before sales. That's backwards."

SPECIFICITY FIX: Add a real moment in line 2: "I told Marcus last week — pause the mindset work. We have to fix his pricing first."

ASKING FIX: Replace "Comment below" with: "DM me 'sequence' for the 5 prompts I use."

PROJECTED SCORE AFTER FIXES: 4/4 — Magnetic
```

### Example 2: Agency. Magnetic (4/4)

**Input:**
> "We fired our top creator last week. $14K/month. We replaced him with one AI workflow that took 4 hours to set up. Output tripled. Margins doubled. The hard part wasn't the AI. it was admitting the workflow we'd built around a human had been the bottleneck all along. DM me 'workflow' for the doc."

**Output:**
```
SCORE: 4/4 — Magnetic ✓

DIAGNOSIS:
✓ Voice: 1 — Clear founder voice. Direct, declarative, no AI vocabulary.
✓ POV: 1 — Takes a side: humans were the bottleneck, not the missing tool.
✓ Specificity: 1 — "$14K/month", "4 hours", "tripled", "doubled" — four numbers in first half.
✓ Asking: 1 — "DM me 'workflow' for the doc" — specific keyword + specific deliverable.

NO FIXES NEEDED. Publish.
```

### Example 3: E-commerce. Background noise (2/4)

**Input:**
> "We just launched our new collection. 12 SKUs, all designed in-house. Free shipping this week. Use code LAUNCH at checkout."

**Output:**
```
SCORE: 2/4 — Background noise

DIAGNOSIS:
✗ Voice: 0 — Reads like a Shopify announcement template. No founder fingerprint.
✗ POV: 0 — Pure product announcement. No "here's why this matters."
✓ Specificity: 1 — "12 SKUs", "LAUNCH" code — numbers and a specific.
✓ Asking: 1 — Discount code = a specific ask, even if transactional.

TO GET TO 4/4 (2 edits, one line each):

VOICE FIX: Open with founder POV: "We almost cut this collection in half last month. Glad we didn't — here's why."

POV FIX: Add a take in line 2 or 3: "Most brands launch what's safe. We launched what we'd actually wear. Two of the SKUs would have been killed by a normal product team."

PROJECTED SCORE AFTER FIXES: 4/4 — Magnetic
```

### Example 4: B2B SaaS. Visible (3/4)

**Input:**
> "Three weeks ago we ran an experiment. We took the SDR follow-up sequence. 7 emails, all written by humans, and replaced it with one AI agent trained on our best closer's voice. Open rate jumped from 22% to 64%. Reply rate from 4% to 19%. The agent doesn't sleep. We're rethinking the role."

**Output:**
```
SCORE: 3/4 — Visible

DIAGNOSIS:
✓ Voice: 1 — Founder-direct. Concrete experimental framing.
✓ POV: 1 — Implicit take ("we're rethinking the role") — humans are being challenged.
✓ Specificity: 1 — Real numbers (22 → 64, 4 → 19), specific structure (7 emails, 1 agent).
✗ Asking: 0 — No DM keyword or invitation in the last 2 lines.

TO GET TO 4/4 (1 edit):

ASKING FIX: Add as the final line: "DM me 'agent' if you want the system prompt we trained it on."

PROJECTED SCORE AFTER FIX: 4/4 — Magnetic
```

### Example 5: Fitness. Invisible (1/4)

**Input:**
> "Consistency is the key to fitness success. Many people start with great intentions but lose motivation within 30 days. Here are 5 strategies to stay consistent!"

**Output:**
```
SCORE: 1/4 — Invisible

DIAGNOSIS:
✗ Voice: 0 — Generic fitness coach voice. AI tell ("key to success").
✗ POV: 0 — No side. Pure tease for the "5 strategies".
✓ Specificity: 1 — "30 days" — one number, just barely.
✗ Asking: 0 — Implied "read on" but no specific invitation.

TO GET TO 4/4 (3 edits):

VOICE FIX: First person, present tense. "I just dropped a client. 14 months. They never missed a session. Wrong reason."

POV FIX: Take a contrarian side: "Consistency isn't the goal. Specificity is. Consistent at the wrong thing is just expensive."

ASKING FIX: End with: "DM me 'specific' for the 1-page audit I send all new clients."

PROJECTED SCORE AFTER FIXES: 4/4 — Magnetic
```

---

## Self-Critique Checks (run before delivering output)

- [ ] Did I score each dimension with a binary 0/1, not a fractional 0.5?
- [ ] Are my one-line fixes ADDITIVE (add to the post) or DESTRUCTIVE (rewrite the post)?
- [ ] Did I avoid suggesting "use better keywords" or other vague fixes?
- [ ] Is each fix specific to THIS post, not generic advice?
- [ ] If `score-rewrite-rescore` mode, did the rewrite actually hit 4/4 when re-scored?
- [ ] If industry was provided, did I use industry-specific reference language in fixes?

If any check fails: regenerate that section before output.

---

## Limitations

**This skill does NOT:**
- Score for *correctness*. factually wrong posts still score 4/4 if the format is right
- Score for *tone match*. a post can be 4/4 and still feel off-brand
- Score for *platform fit*. same scoring across LinkedIn, X, Instagram (use platform-specific style guides separately)
- Catch *manipulative* content. engagement-bait can score 4/4

**Best used for:** Founder-voice content where the goal is inbound DMs and qualified conversations.

---

## Pro Tips

1. **Run it BEFORE publishing, not after**. most people run it after and feel bad. The point is the pre-publish edit.
2. **Score your last 10 posts in one batch**. find your weakest dimension. That's your training focus for the next month.
3. **Track your average over time**. A rising average across your last 20 posts shows the voice work is landing.
4. **The Asking dimension is the cheapest to fix**. most invisible posts gain 1 point just by adding a specific DM keyword.
5. **The Voice dimension is the hardest to fix without a voice profile**. if you keep scoring 0 on voice, run `voice-profile-builder` first.

---

## Quality Checklist (for any 4/4 post)

- [ ] Reads naturally aloud (test it)
- [ ] First line could ONLY have been written by you (or someone who knows you well)
- [ ] One real name + one real number in the first half
- [ ] Takes a side a competitor in the room might disagree with
- [ ] Ends with a specific keyword + a specific deliverable
- [ ] No AI tells (leverage, unlock, game-changing, empower, journey, dive deep)
- [ ] 1300-1500 characters (the program standard for LinkedIn text posts, about 200-250 words)

---
## Use in the Purely Personal connector


After the draft: Fix gaps with polish_post and de_ai_ify; review a batch with review_homework.
