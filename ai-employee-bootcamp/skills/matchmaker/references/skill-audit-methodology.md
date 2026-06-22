# Skill Audit Methodology
# Matchmaker Reference — Purely Personal Bootcamp

This file teaches the Matchmaker exactly how to audit any skill — not just the five
starter skills. Use this methodology when a participant wants to apply the Matchmaker
to their own custom skills or any other skill they've built.

---

## THE MATCHMAKER'S CORE PRINCIPLE

A skill is a set of instructions that runs on every piece of content or output it produces.
If those instructions don't contain the right context, the output will always be wrong —
no matter how good the underlying AI is.

Garbage in, garbage out is the technical version.
Generic in, generic out is the marketing version.

The Matchmaker's job is to find every place where a skill will produce generic output
for THIS participant — and name what specific context is missing.

---

## THE 3-LAYER SKILL ANATOMY

Every skill has three layers. The Matchmaker audits all three.

### Layer 1 — Role & Identity
Who is the AI playing when it runs this skill?
Generic: "You are a LinkedIn content writer."
Fitted: "You are [participant name]'s content system. You know they are a
[role] who serves [specific ICP], leads with [specific angle], and never
writes content that could come from a general marketing account."

**What to check:**
Does the skill's role definition include the participant's specific context?
Or is it a generic writer who could be anyone?

### Layer 2 — Knowledge Inputs
What does the skill know before it starts?
This is the most common gap. Most starter skills say "apply Voice DNA if provided"
but don't hardcode what the Voice DNA actually says.

A fitted skill has the critical context embedded — not referenced optionally.

**What to check:**
- Does the skill know the participant's ICP by name and situation — not just "your ICP"?
- Does it know their offer name, price point, delivery method?
- Does it know their top 3 competitors and what those competitors say?
- Does it know their banned words list?
- Does it know their 3 best proof points?
- Does it know their preferred CTA style?

### Layer 3 — Output Rules
What format, length, and constraints govern the output?
Generic skills produce "a LinkedIn post" or "a DM sequence."
Fitted skills produce "a LinkedIn post under 1,300 characters, opening with
a one-line hook, using single-sentence paragraphs, never using bullet lists,
ending with a direct CTA that contains the word [keyword]."

**What to check:**
Does the skill have the participant's specific output rules?
Or are the output rules so generic they could apply to anyone?

---

## THE GAP TAXONOMY — 6 TYPES WITH SEVERITY RATINGS

Use this taxonomy to classify every gap found. Not all gaps are equal.
Rate each gap: Critical (will break the output every time) / Major (degrades quality significantly)
/ Minor (small inconsistency, fixable with light editing).

### Type 1 — Identity Gap (usually Critical)
The skill doesn't know who is running it.
No participant name, role, offer, or market position embedded.
Every single output is off-brand by default.

**Signs:** The skill's opening role definition uses only generic terms.
No reference to the participant's specific position, methodology, or market.

**Fix pattern:** Add a WHO block at the top of the skill that hardcodes:
name, role, market, offer, ICP, unique angle, competitive position.

---

### Type 2 — Voice Gap (Critical to Major depending on extent)
Covered in full in `voice-icp-standards.md`.

**Signs:** No banned words list. No sentence rhythm guidance.
No emotional register specified. Generic "write conversationally" as the only direction.

**Fix pattern:** Add a VOICE block that includes all 8 voice dimensions.
Pull directly from Voice DNA document.

---

### Type 3 — ICP Specificity Gap (Critical)
The skill knows there is an ICP but doesn't know who they actually are.

**Signs:** ICP is described as a role only ("founders," "coaches," "consultants").
No stage of business, no situation, no exact language, no objections documented.

**Fix pattern:** Add an ICP block that includes:
role + company stage + situation + top 3 pains in their own words + top 2 objections.

---

### Type 4 — Offer & Proof Gap (Major to Critical depending on skill)
The skill doesn't know what it's ultimately selling toward.
Critical for: DM Sequence Writer, Sales Call Prep.
Major for: Caption Writer, Newsletter Writer.
Minor for: Content Strategy (content doesn't always sell directly).

**Signs:** The skill references "your offer" without knowing what the offer is.
No proof points, results, or testimonials embedded.

**Fix pattern:** Add an OFFER block:
offer name + what transformation it delivers + who it's for + proof points (3 minimum).

---

### Type 5 — Competitive Context Gap (Major)
The skill doesn't know the participant's competitive landscape.

**Signs:** No competitor names referenced. No saturated topics listed.
No differentiation angle embedded.

**Fix pattern:** Add a COMPETITIVE CONTEXT block:
top 3-5 competitors by name + what they're known for + topics to avoid + the
angle this participant owns that competitors don't.

---

### Type 6 — Output Rules Gap (Minor to Major depending on platform)
The skill's output format doesn't match the participant's actual publishing standards.

**Signs:** No character count specified (when the platform has limits).
No line break rules. No CTA format specified. No emoji rules. No structural constraints.

**Fix pattern:** Add an OUTPUT RULES block:
max character count + line structure + CTA format + emoji policy + platform-specific rules.

---

## HOW TO AUDIT A CUSTOM SKILL (not one of the 5 starters)

When a participant wants to apply the Matchmaker to a skill they've built themselves,
follow this exact sequence:

### Step 1 — Classify the skill
What is this skill's job? Is it:
- A content creation skill (posts, captions, newsletters, carousels)?
- An outreach/sales skill (DMs, emails, connection requests)?
- A strategy skill (content plans, positioning, offer development)?
- A prep skill (call prep, meeting briefs, research summaries)?
- An analytics/review skill (scoring, auditing, analysing existing output)?

The skill's job determines which gaps matter most.
An outreach skill with no Offer & Proof data is critical. Same gap in a strategy skill is minor.

### Step 2 — Read the skill against the 3-layer anatomy
Work through Layer 1 (Role), Layer 2 (Knowledge Inputs), Layer 3 (Output Rules).
Document every gap you find using the 6-type taxonomy above.

### Step 3 — Cross-reference against all foundation documents
Run the same 6-dimension audit as for the starter skills:
Voice / ICP / Offer / Industry & Competitor / Proof & Credibility / Formatting & Rules.

### Step 4 — Rate severity and rank by impact
Not every gap needs to be fixed immediately.
Rate each gap (Critical / Major / Minor) and rank the top 3 fixes by output impact.

### Step 5 — Produce the gap report
Same format as the starter skill reports.
End with the Tailor Briefing block so the participant can immediately act on the findings.

---

## WHAT MAKES A GREAT MATCHMAKER OUTPUT

The Matchmaker's report is valuable in direct proportion to its specificity.

**Weak gap finding:**
"The DM skill lacks personalisation."

**Strong gap finding:**
"The DM skill's cold opener template uses 'I noticed your recent post' as its
observation hook — but this participant's ICP is enterprise procurement leads
who rarely post on LinkedIn. The hook will fail for 80%+ of their outreach.
The skill needs a non-content-based observation hook (job change, company news,
shared connection, industry event) as the default for this ICP."

The difference: the strong version names the specific failure mechanism,
explains why it matters for THIS participant's ICP, and points to the exact fix.

That is the standard for every gap finding in every Matchmaker report.
