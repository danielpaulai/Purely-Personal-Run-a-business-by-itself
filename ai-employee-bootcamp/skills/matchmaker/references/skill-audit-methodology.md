# Skill Audit Methodology
# Matchmaker Reference, Purely Personal Bootcamp

This file teaches the Matchmaker exactly how to audit any skill.

---

## THE MATCHMAKER'S CORE PRINCIPLE

A skill is a set of instructions that runs on every piece of content or output it produces.
If those instructions don't contain the right context, the output will always be wrong, 
no matter how good the underlying AI is.

Generic in, generic out.

---

## THE 3-LAYER SKILL ANATOMY

### Layer 1, Role & Identity
Who is the AI playing when it runs this skill?
Generic: "You are a LinkedIn content writer."
Fitted: "You are [participant name]'s content system. You know they are a [role]
who serves [specific ICP], leads with [specific angle], and never writes content
that could come from a general marketing account."

**What to check:** Does the skill's role definition include the participant's specific context?

### Layer 2, Knowledge Inputs
What does the skill know before it starts?
Most starter skills say "apply Voice DNA if provided" but don't hardcode what it actually says.
A fitted skill has critical context embedded, not referenced optionally.

**What to check:**
- Does the skill know the participant's ICP by name and situation?
- Does it know their offer name, price point, delivery method?
- Does it know their top 3 competitors?
- Does it know their banned words list?
- Does it know their 3 best proof points?
- Does it know their preferred CTA style?

### Layer 3, Output Rules
What format, length, and constraints govern the output?
Generic: "a LinkedIn post."
Fitted: "a LinkedIn post under 1,300 characters, opening with a one-line hook,
using single-sentence paragraphs, never using bullet lists, ending with a direct
CTA that contains the word [keyword]."

---

## THE GAP TAXONOMY, 6 TYPES WITH SEVERITY RATINGS

### Type 1, Identity Gap (usually Critical)
The skill doesn't know who is running it. No participant name, role, offer, or market position.
**Fix pattern:** Add a WHO block hardcoding name, role, market, offer, ICP, unique angle.

### Type 2, Voice Gap (Critical to Major)
No banned words list. No sentence rhythm guidance. No emotional register specified.
**Fix pattern:** Add a VOICE block with all 8 voice dimensions from Voice DNA.

### Type 3, ICP Specificity Gap (Critical)
The skill knows there is an ICP but doesn't know who they actually are.
ICP is described as a role only, no stage, no situation, no exact language, no objections.
**Fix pattern:** role + company stage + situation + top 3 pains in their words + top 2 objections.

### Type 4, Offer & Proof Gap (Major to Critical)
The skill references "your offer" without knowing what the offer is.
No proof points, results, or testimonials embedded.
**Fix pattern:** offer name + transformation + who it's for + 3 proof points minimum.

### Type 5, Competitive Context Gap (Major)
No competitor names. No saturated topics listed. No differentiation angle embedded.
**Fix pattern:** top 3-5 competitors + what they're known for + topics to avoid + the angle this participant owns.

### Type 6, Output Rules Gap (Minor to Major)
No character count. No line break rules. No CTA format. No emoji rules.
**Fix pattern:** max character count + line structure + CTA format + emoji policy.

---

## HOW TO AUDIT A CUSTOM SKILL

When auditing a skill the participant built themselves:

Step 1: Classify the skill (content / outreach / strategy / prep / analytics)
Step 2: Read against the 3-layer anatomy
Step 3: Cross-reference against all foundation documents
Step 4: Rate severity and rank top 3 fixes by output impact
Step 5: Produce the gap report with Tailor Briefing block

---

## WHAT MAKES A GREAT MATCHMAKER OUTPUT

**Weak gap finding:**
"The DM skill lacks personalisation."

**Strong gap finding:**
"The DM skill's cold opener template uses 'I noticed your recent post' as its
observation hook, but this participant's ICP is enterprise procurement leads
who rarely post on LinkedIn. The hook will fail for 80%+ of their outreach.
The skill needs a non-content-based observation hook (job change, company news,
shared connection, industry event) as the default for this ICP."

Every gap finding must name the specific failure mechanism, explain why it matters
for THIS participant's ICP, and point to the exact fix.
