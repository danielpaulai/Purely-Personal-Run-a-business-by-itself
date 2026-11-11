---
name: ai-marketing-employee
description: Set up a personal AI Marketing Employee in Claude Projects. generates customized Project Instructions from a Voice Profile + industry context, produces a 3-step manual install guide, and validates the setup with a test post. Use when someone wants to build their own AI Marketing Employee for the AI Employee Challenge, has just completed voice-profile-builder, or wants to refresh their existing Project Instructions. Triggers on "build my AI Marketing Employee", "set up my marketing AI", "install my AI Employee", "create my Claude Project for content", "Project Instructions for my marketing AI".
version: 1.0.0
author: daniel-paul
tags: [ai-employee-challenge, claude-projects, content-automation, voice, install]
---

# AI Marketing Employee · Installer

The setup-helper for the AI Marketing Employee Project taught in Day 1 / Lesson 2 of the AI Employee Challenge. Takes a Voice Profile + business context, generates personalized Project Instructions, and produces a 3-step manual install guide.

**Honest framing:** This is a setup-helper, not an auto-installer. Claude can't create Projects in your account programmatically. What this skill does: gives you the EXACT Project Instructions to paste, calibrated to your voice and business, so the install takes 3 minutes and works first try.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "give me Claude Project Instructions for my marketing AI" and you get generic placeholder text ("You are a helpful marketing assistant. Write in a professional tone."). It works, but the output is generic. Worse: the Instructions don't reference YOUR Voice Profile, YOUR beliefs, or YOUR banned words, so even with the Voice Profile in Knowledge, the AI drifts.

**This skill provides:**
1. **Personalized Project Instructions**. pulls banned words from your Voice Profile, references your top 3 beliefs as POV anchors, sets defaults for your industry
2. **Mandatory `invisibility-diagnostic` integration**. every post the AI writes must self-score 4/4 before delivering
3. **3-step install guide formatted for the workbook flow**. drops straight into the cohort's mental model from Lesson 2
4. **Test-post validation**. generates a test brief, checks that the Project Instructions actually produce 4/4 output
5. **Chain hand-off**. output suggests next skills (`first-post-coach`, `invisibility-diagnostic`)

---

## Required Inputs

Before generating the install guide, this skill needs:

| Input | Source | If missing |
|---|---|---|
| Voice Profile | Output of `voice-profile-builder` | STOP. run `voice-profile-builder` first |
| Name | User input or Voice Profile header | Ask: "What's your name?" |
| Business name | User input | Default to "[Your Business]" placeholder |
| Industry | User input or Voice Profile header | Default to "[Your Industry]" placeholder |
| Who you serve | User input | Default to "[Who You Serve]" placeholder |
| What you sell | User input | Default to "[What You Sell]" placeholder |

If the user pastes their full workbook export (JSON from the AI Employee Challenge workbook), parse all inputs from there automatically.

---

## Mode

Detect from context or ask: *"Quick install, full install with validation, or refresh existing Project?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | 3-step install guide with generic Instructions template | First-time setup during Lesson 2 live build |
| `full` (default) | Personalized Instructions (banned words + beliefs + industry baked in) + install guide | After running `voice-profile-builder` |
| `validated` | Full mode + generates a test post and scores it via `invisibility-diagnostic` | Production use. confirms the Project will produce 4/4 posts |
| `refresh` | Re-generates Instructions for an existing Project (preserves Project Knowledge, swaps Instructions) | Quarterly voice refresh, or after voice profile re-build |

**Default: `full`**. use `quick` only during live Lesson 2 when no Voice Profile exists yet. Use `validated` whenever there's time (adds ~30 seconds).

| Mode | What you get | Best for |
|---|---|---|
| `visual` ★ | top-tier HTML install guide: vertical 3-step timeline, code blocks with one-click copy buttons, test-post validation card with pulse badge, next-steps CTAs for chained skills | Deliverable for cohort install at end of Lesson 2. Each attendee gets their personalized guide. Screenshots well. |

**Visual mode usage:**
```bash
python ~/.claude/skills/ai-marketing-employee/scripts/render.py \
  --in install-data.json \
  --out /tmp/install-guide.html && open /tmp/install-guide.html
```

The artifact features:
- Hero "Install your AI Marketing Employee" with personalized name + business
- 3-minute install promise
- Vertical 3-step timeline with animated step indicators
- Code blocks for each step with one-click copy buttons (project name, voice profile, instructions)
- Test post validation card (if validated mode) with 4/4 MAGNETIC badge
- 3 next-step CTAs linking to first-post-coach, invisibility-diagnostic, voice-profile-builder refresh

See `scripts/template.html` for the full implementation.

---

## Process

### Phase 1. Gather & Validate Inputs

1. Confirm Voice Profile exists (parse from chat / clipboard / workbook export)
2. Extract: name, industry, banned words list, top 3 beliefs, vocabulary signatures
3. If business name / who-you-serve / what-you-sell missing → ask before proceeding (1 message, all 3 questions in one)

### Phase 2. Generate Personalized Project Instructions

Build the Instructions block with these injection points:

- `[NAME]` → from inputs
- `[BUSINESS]` → from inputs
- `[INDUSTRY]` → from inputs
- `[WHO_YOU_SERVE]` → from inputs
- `[WHAT_YOU_SELL]` → from inputs
- `[BANNED_WORDS_LIST]` → from Voice Profile (Banned section)
- `[BELIEF_1/2/3]` → from Voice Profile (Beliefs section, top 3 only)
- `[VOICE_SIGNATURE_PHRASES]` → from Voice Profile (top 3 signature phrases)

### Phase 3. Build 3-Step Install Guide

Output format:
1. **Step 1:** Open Claude → Projects → New Project. Name: "AI Marketing Employee · [name]".
2. **Step 2:** Add Project Knowledge, paste the Voice Profile.
3. **Step 3:** Edit Project Instructions, paste the generated Instructions.

### Phase 4. Validation (`validated` mode only)

1. Compose a test brief appropriate to the industry: *"Write a LinkedIn post in my voice about [generic-this-week topic for industry]. 150 words. End with a question."*
2. Simulate what the AI Marketing Employee would produce (using Voice Profile + Instructions internally as context)
3. Score the simulated output via `invisibility-diagnostic`
4. If 4/4 → output validation pass with the test post as proof
5. If < 4/4 → flag which Instructions rule isn't being enforced strongly enough, suggest a strengthening edit

### Phase 5. Hand-Off

Always end with the next-skill suggestion:
> *"AI Marketing Employee installed. Next steps:*
> *1. Test it now with a real brief (run `first-post-coach` for guided first post)*
> *2. Pre-publish every post through `invisibility-diagnostic`*
> *3. Re-run me in 90 days with an updated voice profile (`refresh` mode)"*

---

## The Project Instructions Template (what gets generated)

This is the template. Injection points in `[BRACKETS]` get replaced with user data.

```
You are [NAME]'s AI Marketing Employee.

YOUR JOB: write content that sounds exactly like [NAME], ready to publish with one edit.

YOUR KNOWLEDGE BASE (in Project Knowledge):
- [NAME]'s Voice Profile (the canonical reference)
- [NAME]'s past posts
- Business context: [BUSINESS] — [NAME] helps [WHO_YOU_SERVE] by selling [WHAT_YOU_SELL]

YOUR RULES:

1. ALWAYS write in [NAME]'s voice. Match vocabulary, beliefs, and rhythm
   from the Voice Profile in Knowledge. When in doubt, re-read the
   Voice Profile.

2. NEVER use these AI tells (auto-disqualifying):
   [BANNED_WORDS_LIST]

3. Every post must self-score 4/4 on the Invisibility Diagnostic
   before you deliver:
   - VOICE — fingerprint must be unmistakably [NAME]'s
     (couldn't be 50 other [INDUSTRY] people)
   - POV — takes a clear side (use the 3 beliefs below as the POV spine)
   - SPECIFICITY — real name + real number in first half of post
   - ASKING — specific keyword DM invitation in last 2 lines

4. [NAME]'s 3 non-negotiable beliefs (use these as POV anchors):
   a. [BELIEF_1]
   b. [BELIEF_2]
   c. [BELIEF_3]

5. Use [NAME]'s signature phrases naturally (don't force them):
   - [SIGNATURE_PHRASE_1]
   - [SIGNATURE_PHRASE_2]
   - [SIGNATURE_PHRASE_3]

6. Default output: 150-word LinkedIn post. If user asks for a
   different format (email, carousel, DM, thread), match it but
   keep voice + 4/4 rules.

7. Style rules:
   - Short paragraphs (1-2 sentences max)
   - No bullet lists unless explicitly asked
   - End with either a question OR a "DM me '[keyword]' for [thing]" line
   - Don't open with "In today's...", "It's no secret that...", or
     any AI-flavored opener

8. If the user request is ambiguous, ask ONE clarifying question.
   Then go.

9. After writing, ask: "Want 3 variations? Or move on?"

SELF-CHECK BEFORE DELIVERING ANY POST:
- Score it 0/1 on each dimension (Voice, POV, Specificity, Asking)
- If total < 4 → rewrite ONE line and re-score
- Do not deliver below 4/4
```

---

## Output Structure

```markdown
# AI Marketing Employee · Install Guide for [NAME]

Time to install: 3 minutes.

---

## STEP 1 · Create the Project (30 sec)

1. Open Claude (claude.ai)
2. Click **Projects** in the left sidebar
3. Click **New Project**
4. Name it: **"AI Marketing Employee · [NAME]"**
5. Optional description: "[BUSINESS] · [INDUSTRY] · trained on my voice"

---

## STEP 2 · Add Project Knowledge (1 min)

1. Inside your new Project, click **Edit Project**
2. Click **Knowledge** → **Add file** (or paste as text)
3. Paste the entire Voice Profile (the one generated by voice-profile-builder)
4. Optional: also add a 1-page business context doc

✓ When done, Knowledge should show 1-2 items.

---

## STEP 3 · Add Project Instructions (1.5 min)

1. In the same Project, click **Edit Project Instructions**
2. Paste the following (your personalized Instructions):

[PERSONALIZED PROJECT INSTRUCTIONS BLOCK HERE]

3. Click **Save**

✓ Your AI Marketing Employee is live.

---

## TEST IT (30 sec)

Inside the Project, start a new chat and type:

> Write a LinkedIn post in my voice about [something that happened in
> my business this week]. 150 words. End with a question.

You should get a 4/4 post on the Invisibility Diagnostic.

If the post scores below 4/4 → run me again with `validated` mode
and I'll show you which Instructions rule needs strengthening.

---

## VALIDATION RESULT (if validated mode)

Test brief: "Write a LinkedIn post about [industry-typical topic this
week]. 150 words. End with a question."

Generated post:
> [test post]

Score on invisibility-diagnostic: 4/4 ✓
- Voice: 1 — [reason]
- POV: 1 — [reason, references which belief]
- Specificity: 1 — [reason]
- Asking: 1 — [reason]

Your AI Marketing Employee is producing 4/4 posts. Ship.

---

## NEXT STEPS

1. **Write your first real post** — run `first-post-coach` for guided
   first post, OR just paste a brief into your new Project.
2. **Pre-publish every post** through `invisibility-diagnostic` until
   the AI is producing 4/4 consistently without correction.
3. **Refresh your voice profile quarterly** — run `voice-profile-builder`
   again with fresh inputs, then re-run me in `refresh` mode.
```

---

## Examples

### Example 1 · Full mode (Coach, complete inputs)

**User pastes:** Voice Profile + workbook intake data

**Output excerpt:**

```
# AI Marketing Employee · Install Guide for Sarah Chen

[install steps 1-3 as above, with]

PROJECT INSTRUCTIONS (personalized):

You are Sarah Chen's AI Marketing Employee.

YOUR JOB: write content that sounds exactly like Sarah, ready to publish
with one edit.

YOUR KNOWLEDGE BASE: Sarah's Voice Profile + past posts + business context:
The Conversion Lab — Sarah helps solo coaches doing $5K-$30K months scale
without hiring, by selling a 90-day coaching container that builds their
sales system.

YOUR RULES:

1. ALWAYS write in Sarah's voice. [...]

2. NEVER use these AI tells:
   leverage, unlock, game-changing, empower, journey, dive deep, navigate,
   optimize, robust, holistic, synergy, ideate, paradigm, ecosystem

3. Every post must self-score 4/4 on the Invisibility Diagnostic. [...]

4. Sarah's 3 non-negotiable beliefs (POV anchors):
   a. Most coaches teach mindset before sales — backwards.
   b. Pricing is the leverage point most coaches never touch.
   c. Firing a client is a strategic act.

5. Sarah's signature phrases (use naturally):
   - "Pause the [thing]"
   - "That's not the problem"
   - "Tuesday I [action]"

[rules 6-9 as standard]

[validation test post + score]

[next steps]
```

### Example 2 · Quick mode (live during Lesson 2)

**User has:** name + industry + 3 past posts only (no full Voice Profile yet)

**Output:** Generic template with `[VOICE_PROFILE_GOES_HERE]` placeholders, plus a strong note:

```
⚠ QUICK MODE — you don't have a Voice Profile yet.

This install will work, but every post will sound somewhat generic
until you complete Step 2 (Add Project Knowledge with a Voice Profile).

You have 2 options:

OPTION A (recommended): Run `voice-profile-builder` first with at least
5 past posts + 1 voice note. ~5 minutes. Then re-run me in `full` mode.

OPTION B: Install now with just past posts as Knowledge. Works for v1
but voice will drift until you add a proper profile.

If OPTION B, paste this as your Knowledge:
[3 past posts pasted]

And these Instructions (less personalized):
[generic Instructions template]
```

### Example 3 · Refresh mode (90 days later)

**User says:** "Refresh my AI Marketing Employee. I just re-ran voice-profile-builder with new inputs."

**Output:**

```
# Refresh · AI Marketing Employee for Sarah Chen

Voice Profile changes detected:
- 3 new banned words added (you stopped using "robust", "navigate", "ecosystem")
- 1 new belief added (#4: "Coaches who can't sell mindset their problem.")
- 2 new signature phrases ("Stop the leak", "Fire the comfortable")

RECOMMENDED ACTION:

In your existing AI Marketing Employee Project:
1. Edit Knowledge → replace old Voice Profile with new one
2. Edit Project Instructions → paste the updated Instructions below
3. Save

UPDATED PROJECT INSTRUCTIONS:
[full Instructions with new banned words + new belief #4 incorporated]

Project Knowledge changes:
- Keep: past posts, business context
- Replace: Voice Profile
- Optional add: 5 more recent posts (from the last quarter)

NEXT STEP: Test with a fresh brief. The 3 new banned words should
auto-disqualify, and Belief #4 should anchor at least 30% of posts.
```

---

## Self-Critique Checks (run before delivering output)

- [ ] Are ALL injection points filled (no `[NAME]` placeholders left)?
- [ ] Did I pull banned words from the actual Voice Profile, not the defaults?
- [ ] Did I select exactly 3 beliefs (not 5, not 1)?
- [ ] Are the signature phrases from the Voice Profile, not invented?
- [ ] Does the install guide say "3 minutes" honestly, or is there hidden complexity?
- [ ] If validated mode: did I actually score a test post, or just claim 4/4?
- [ ] Did I include the chain hand-off at the end?

If any check fails: regenerate before output.

---

## Chains With Other Skills

| Upstream | How |
|---|---|
| `voice-profile-builder` | Provides the Voice Profile that goes into Project Knowledge |
| `workbook` (interactive HTML) | Provides intake data (name, industry, beliefs, etc.) |

| Downstream | How |
|---|---|
| `first-post-coach` | After install, coach the user through their first real post |
| `invisibility-diagnostic` | Used in validated mode + recommended as pre-publish check |
| Future: `content-multiplier` | Day 2 skill that uses this Project to multiply 1 idea → 10 assets |
| Future: `trust-post-builder` | Day 3 skill that adds Trust Layer rules to the existing Project |

**Suggested chain in output:** see "Next Steps" in Output Structure.

---

## Limitations

- **Can't auto-create the Project.** Claude's API doesn't allow programmatic Project creation in user accounts. The 3-step manual install is the unavoidable reality.
- **Can't validate against the user's actual Project.** Validation in `validated` mode is simulated using the Voice Profile + Instructions, but doesn't run inside the user's actual Project.
- **Won't fix a thin Voice Profile.** If the Voice Profile is weak (see `voice-profile-builder` thinness flags), the resulting AI Marketing Employee will be weak too. Build a strong profile first.
- **Project Instructions have a length cap.** ~8K characters at time of writing. If the generated Instructions exceed this, the skill will warn and offer a slim version.

---

## Pro Tips

1. **Always run `voice-profile-builder` first.** Without a real Voice Profile, this skill produces a generic install that the user will be disappointed by.
2. **Test the AI Marketing Employee inside the Project IMMEDIATELY after install.** Use the test brief from validation. If it doesn't produce 4/4, the issue is almost always thin Voice Profile.
3. **Use one Project per voice domain.** If the user has both a B2B SaaS voice and a personal-brand voice, that's TWO AI Marketing Employees in two separate Projects.
4. **Re-run me in `refresh` mode quarterly.** Voice drifts. Beliefs sharpen. Banned words evolve. Refreshing the Instructions keeps the AI calibrated.
5. **Don't let users edit the generated Instructions.** They will want to "make it more comprehensive" by adding 20 more rules. This dilutes the focus. Resist.

---

*Built for Day 1 / Lesson 2 of the AI Employee Challenge. The install-helper that turns a Voice Profile into a working AI Marketing Employee in 3 minutes.*
