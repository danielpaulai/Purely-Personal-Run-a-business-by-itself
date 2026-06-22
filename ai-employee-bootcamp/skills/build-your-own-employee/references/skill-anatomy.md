# Skill Anatomy
# Tailor Reference — Purely Personal Bootcamp

Every skill the Tailor produces must follow this exact structural anatomy.
This is how the five starter skills are built. Every rewritten skill mirrors this structure.
Do not skip sections. Do not reorder them. Do not truncate.

---

## THE 8-SECTION SKILL STRUCTURE

Every skill file has exactly these sections in this order:

```
1. YAML Frontmatter
2. Skill Header + WHO Block
3. Reference File List
4. Voice Lock (replaces Voice DNA Check)
5. Intake Form
6. Step-by-Step Workflow
7. Delivery Format
8. Quality Gate
```

---

## SECTION 1 — YAML FRONTMATTER

Required fields: `name` and `description`.
The description is the primary trigger mechanism — it determines when the skill fires.

**Structure:**
```yaml
---
name: [skill-name-in-kebab-case]
description: >
  [What the skill does + who it's for + when to trigger it.
   Must name: the participant, their ICP role/industry, their offer type.
   Must include all trigger phrases someone might actually type.
   Target: 80-120 words. Enough to be specific, short enough to load fast.]
---
```

**Trigger phrase requirements:**
Every description must include at minimum:
- 3-5 exact phrases that trigger the skill ("write a post", "DM sequence", etc.)
- The participant's name or brand so the skill self-identifies
- The ICP so the skill is clearly not for everyone
- The output so the user knows what they're getting

**Fitted description example (Caption Writer):**
```yaml
---
name: linkedin-caption-writer
description: >
  Writes scroll-stopping LinkedIn posts in [NAME]'s voice — for [ICP ROLE] in [INDUSTRY]
  who [ICP SITUATION]. Uses [NAME]'s exact Voice DNA: [top 2-3 voice rules in brief].
  Applies direct-response frameworks. Scores 4/4 on the Invisibility Diagnostic.
  Zero AI patterns, zero banned words. Trigger on "write a post", "write a caption",
  "LinkedIn post", "turn this into a post", "write this up", or any idea, result,
  or story [NAME] wants published.
---
```

---

## SECTION 2 — SKILL HEADER + WHO BLOCK

Immediately after the YAML, before any instructions:

```markdown
# [Skill Name] — [PARTICIPANT NAME]
# Fitted by Purely Personal · by Daniel Paul

WHO THIS IS FOR:
[PARTICIPANT NAME] is a [their role/title] who serves [ICP description in 1 sentence].
Their offer: [OFFER NAME] — [one-sentence transformation delivered].
Their unique angle: [UNIQUE ANGLE — what they say that no competitor says].
Their ICP: [role] at [company stage] dealing with [top pain in ICP's own words].
Competitors to avoid sounding like: [Top 3 by name].

One job: [skill's mission statement — rewritten to be specific to this participant].
If the output could have been produced by any [niche] [skill type], rebuild it.
```

---

## SECTION 3 — REFERENCE FILE LIST

Immediately after the WHO Block.
List every reference file this skill reads and what each one contains.

```markdown
Read ALL reference files before writing:
- `/references/voice-dna.md` — [PARTICIPANT]'s voice rules, ICP, banned words, hook archetypes
- `/references/human-writing-standards.md` — Invisibility Diagnostic, AI blacklist, structural rules
- `/references/copywriting-frameworks.md` — 8 frameworks, when to use each, examples
- `/references/design-system.md` — brand tokens for any formatted output
```

If the participant has separate ICP or offer documents, add:
```markdown
- `/references/[participant]-icp.md` — full ICP profile with exact language and objections
- `/references/[participant]-offer.md` — offer details, delivery, proof points, objection scripts
```

Note: if these participant-specific reference files don't exist yet, add to the quality gate:
"Create /references/[participant]-icp.md and -offer.md from the Tailor Briefing."

---

## SECTION 4 — VOICE LOCK

Replaces the generic "Voice DNA Check" from the starter skills.
In a fitted skill, the participant's voice is the default. No fallback.

```markdown
## VOICE LOCK

This skill writes in [PARTICIPANT]'s voice. Always. No fallback. No override.

Voice rules (non-negotiable):
1. [Rule 1 — specific, not generic. e.g. "Short sentences. Under 10 words when making a point."]
2. [Rule 2 — e.g. "Never start a sentence with 'I'. Rotate openers."]
3. [Rule 3 — e.g. "Every claim needs a number or a name. No vague proof."]
4. [Rule 4 — e.g. "Write for one person. Never 'many founders' or 'most people'."]
5. [Rule 5 — e.g. "CTA always names the action, the keyword, and the outcome."]

Banned words (remove from every output before delivery):
[Exact banned list — minimum 10 words/phrases]

Sentence rhythm: [description — e.g. "Short declarative. Medium explanation. Short punch."]
Energy level: [1-5 with their level — e.g. "3/5 — direct and confident, not hyped"]
CTA format: [their exact format — e.g. "DM me [KEYWORD] and I'll send [SPECIFIC THING]"]

If any output violates these rules — rewrite before delivering.
```

---

## SECTION 5 — INTAKE FORM

The intake form collects only what changes per session.
Everything known from the Tailor Briefing is pre-filled. Never ask for it again.

**What to pre-fill (from Tailor Briefing):**
- Participant name and role
- ICP definition
- Offer name and transformation
- Proof points
- Competitors
- Voice rules and banned words

**What to ask per session:**
- The specific topic, idea, post, prospect, or use case for this session
- Any new proof point that's more specific than the standing ones

**Format:**
```markdown
## INTAKE

[PARTICIPANT]'s context is locked. One thing needed before writing:

╔══════════════════════════════════════════════════════╗
║  [PARTICIPANT NAME] — [SKILL NAME]                   ║
╚══════════════════════════════════════════════════════╝

1  TODAY'S [POST / DM / NEWSLETTER / CALL / STRATEGY SESSION]
   [Specific prompt for what changes each session]
   [One example of what good input looks like]

2  NEW PROOF POINT? (optional)
   Standing proof points:
   · [Proof point 1 from Tailor Briefing — specific with numbers]
   · [Proof point 2]
   · [Proof point 3]
   Replace or add if something more recent or specific is available.
```

---

## SECTION 6 — STEP-BY-STEP WORKFLOW

The core instruction set. Every starter skill has numbered steps.
Fitted skills keep the same steps but replace all generic placeholders with specific context.

**Rules for rewriting workflow steps:**
- Every step that references "your ICP" becomes "[PARTICIPANT]'s ICP: [specific description]"
- Every step that references "your offer" becomes "[OFFER NAME]"
- Every step that references "your voice" becomes "[PARTICIPANT]'s voice rules from Section 4"
- Research steps must name the specific niche and competitors to research
- Framework selection steps must note which frameworks work best for this participant's style
- Writing steps must reference the Voice Lock from Section 4

**The workflow structure that must be preserved in every skill:**

Content Strategy:
STEP 1 — INTAKE → STEP 2 — DEEP RESEARCH → STEP 3 — POSITIONING → STEP 4 — AUDIENCE PSYCHOLOGY → STEP 5 — PILLARS → STEP 6 — COMPETITOR STUDY → STEP 7 — 90-DAY PLAN → STEP 8 — QUICK WINS

LinkedIn Caption Writer:
STEP 1 — VOICE LOCK CHECK → STEP 2 — INTAKE → STEP 3 — RESEARCH DECISION → STEP 4 — FRAMEWORK SELECTION → STEP 5 — HOOK SELECTION → STEP 6 — WRITE BODY → STEP 7 — WRITE CTA + P.S. → STEP 8 — INVISIBILITY DIAGNOSTIC → STEP 9 — DE-AI-IFY

DM Sequence Writer:
STEP 1 — VOICE LOCK → STEP 2 — INTAKE → STEP 3 — PROSPECT RESEARCH → STEP 4 — PROFILE AUDIT → STEP 5 — WRITE SEQUENCE (Messages 1-5)

Newsletter Writer:
VOICE LOCK CHECK → STEP 1 — INTAKE → STEP 2 — RESEARCH DECISION → STEP 3 — FRAMEWORK SELECTION → STEP 4 — WRITE 5 SECTIONS → STEP 5 — SUBJECT LINES → STEP 6 — INVISIBILITY DIAGNOSTIC → STEP 7 — DE-AI-IFY

Sales Call Prep:
STEP 1 — INTAKE → STEP 2 — PROSPECT RESEARCH → STEP 3 — CALL BRIEF (Sections 1-9)

Never remove or reorder steps. Add participant context into each step. Never add new steps that break the flow.

---

## SECTION 7 — DELIVERY FORMAT

Every starter skill has a fixed delivery format block showing exactly how output is presented.
Fitted skills keep the same format but update the header to show the participant's name.

**Generic:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PURELY PERSONAL — YOUR POST
by Daniel Paul
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Fitted:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[PARTICIPANT NAME] — [OUTPUT TYPE]
[Participant's brand or company name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The metadata line below the output must also be updated to reflect participant's standards:
```
Framework: [name] · Hook: [archetype] · [char count] chars
Score: [N]/4 — Voice [✓/✗] POV [✓/✗] Specific [✓/✗] Asking [✓/✗]
Voice check: [PARTICIPANT]'s rules applied ✓
Banned words: none detected ✓
```

---

## SECTION 8 — QUALITY GATE

Every starter skill ends with a checkbox quality gate.
Fitted skills keep all original checks AND add participant-specific checks at the end.

**Original checks:** keep all of them unchanged.

**Participant-specific checks to append:**
```
PARTICIPANT-SPECIFIC CHECKS:
□ Voice: matches [PARTICIPANT]'s Voice DNA — [key rule verified]
□ ICP: written specifically for [ICP ROLE] at [COMPANY STAGE]
□ Language: uses ICP's own words — not a paraphrase of their problem
□ Offer: output connects to or points toward [OFFER NAME]
□ Sounds nothing like: [COMPETITOR 1], [COMPETITOR 2], [COMPETITOR 3]
□ Proof: [PARTICIPANT]'s standing proof points available and woven in where relevant
□ Banned: [TOP 3 BANNED WORDS] — confirmed absent
□ CTA: follows [PARTICIPANT]'s format — [their specific CTA style]
□ Scrub 1: zero em dashes (—) — scan full output, rewrite any sentence containing one
□ Scrub 2: zero banned words — checked against references/scrub.md full list
□ Scrub 3: zero banned openers, transitions, meta-commentary
□ Scrub 4: zero banned closers, sentence enders, dramatic pauses
□ Scrub 5: no banned rhetorical devices, contrast patterns, or fake credibility phrases
□ Scrub 6: no AI structural patterns — three-part structure, Hook-Bridge-Value-CTA prison broken
□ Scrub 7: specificity passed — no vague scale language, no uncited stats, no generic examples
□ Scrub 8: tonal patterns checked — no relentless positivity, no conflict avoidance, no over-inclusivity
□ Scrub 9: no formatting tells — emoji, hashtags, line breaks feel human not algorithmic
□ Final test: would [PARTICIPANT] read this output and say "I wrote that"?
   If no — identify which check failed and rebuild that section only.
```

---

## MINIMUM VIABLE FITTED SKILL CHECKLIST

Before delivering any rewritten skill, verify:

□ YAML description names the participant, their ICP, and their offer
□ WHO block is filled with specific context — no generic placeholders
□ Reference files include scrub.md (9-scrub system, 50-section blacklist) alongside participant's own docs
□ Voice Lock has specific rules from their Voice DNA — not "write conversationally"
□ Intake form is pre-filled — only asks for session-specific unknowns
□ Every workflow step has specific context replacing generic placeholders
□ Delivery format header shows participant's name and brand
□ Quality gate includes participant-specific checks plus both scrub checks at the end
□ No instance of "your ICP", "your offer", "your audience" remains anywhere
□ The skill could not be installed by a different participant without editing
