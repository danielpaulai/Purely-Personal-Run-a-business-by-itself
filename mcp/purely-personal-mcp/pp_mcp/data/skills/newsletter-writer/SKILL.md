---
name: newsletter-writer
description: >
  Writes a complete weekly newsletter in the participant's exact voice: a 400-600 word
  email with 5 sections (Hook, This Week's Lesson, One Framework, This Week's Win, One Ask)
  plus 3 subject line options, scored 4/4 on the Invisibility Diagnostic. ALWAYS use this
  skill when the user says "write my newsletter", "newsletter this week", "email to my
  list", "weekly email", "write a newsletter about", "this week's email", or shares any
  topic or lesson they want turned into an email to their list. Also handles cold lists:
  when the user says "my list has gone cold", "I haven't emailed in months", or
  "reactivate my subscribers", run Reactivation Mode instead of the weekly format.
  Do not write a newsletter
  or list email directly without running this skill. NOT for LinkedIn posts — use
  linkedin-caption-writer for that. Part of the Purely Personal system by Daniel Paul.
---

# Newsletter Writer — Purely Personal
# by Daniel Paul · Purely Personal

Read ALL reference files before writing a single word:
- `/references/voice-dna.md` — Daniel's voice rules, ICP, banned words, hook archetypes
- `/references/human-writing-standards.md` — Invisibility Diagnostic, AI blacklist, structural rules
- `/references/copywriting-frameworks.md` — direct-response frameworks, subject line formulas
- `/references/email-craft.md` — house email method: email types, curiosity subject formulas, PS rules, cadence, reactivation
- `/references/design-system.md` — brand colors for any visual headers
- `/references/visual-standards.md`: the visual output standard (environment detection, HTML+GSAP stack, motion rules, visual gate)

One job: write a weekly email so good the subscriber thinks "this is the best newsletter I read this week."

Not a content dump. Not a blog post in email format.
A conversation — from one specific human to one specific reader.
The reader should finish it and immediately want to forward it to someone.

---

## WHERE THIS SKILL SITS

**Reads from:** BUSINESS-BRAIN.md · the monthly strategy document if one exists in this project — pull this week's topic and pillar from it instead of asking · recent LinkedIn posts in this project when the user wants to repurpose one into this week's email
**Hands off to:** linkedin-caption-writer to excerpt this week's lesson as a LinkedIn post
Tell the user the next step in one line after delivering.

---

## STEP 0 — CONTEXT CHECK (always first, never skipped)

Look for the participant's context, in this priority order:
1. **BUSINESS-BRAIN.md** in Project Knowledge or attached to the chat — the single source of truth. If present, its Voice DNA, ICP, offer, proof, sign-off, and design tokens OVERRIDE every default in this skill's references folder.
2. If no brain: individual foundation documents (Voice DNA, ICP, Brand Positioning, Messaging House, Rule of 1, Business in a Box) — use them the same way.
3. If neither: use the bundled references (Daniel Paul's defaults) and label the output header: `DEFAULT VOICE — personalize by adding your BUSINESS-BRAIN.md to this project`.

Resolve these variables now and use them everywhere below:
- [NAME] = participant's name (default: Daniel Paul)
- [SIGN-OFF] = from Voice DNA section (default: "Until next week, Daniel" for newsletters, plain "[NAME]" elsewhere)
- [CTA-DEFAULT] = primary CTA from the Offer section
Never ship a default where a participant value exists.

---

## STEP 1 — INTAKE

Ask ALL in ONE message if not already provided:

```
╔══════════════════════════════════════════════════════╗
║  PURELY PERSONAL — NEWSLETTER WRITER                 ║
║  by Daniel Paul                                      ║
╚══════════════════════════════════════════════════════╝

Before I write this week's email — 4 things:

1  THIS WEEK'S TOPIC OR LESSON
   What's the main idea? A lesson learned, mistake made,
   framework that worked, thing you noticed in the market.
   Rough notes are perfect — raw beats polished every time.

2  THIS WEEK'S WIN
   One real result. Yours or a client's. Specific.
   "Client booked 3 calls from one post."
   "Rewrote my headline — profile views up 4x in a week."
   This is what makes the newsletter feel alive.
   No new win this week? Say "none" — there's a fallback
   (see Section 4). A win is never invented.

3  THE ACTIONABLE TAKEAWAY
   What does the reader DO differently after reading this?
   One specific action, process, or question they can use today.

4  THE ONE ASK
   What should they do after reading?
   Reply / DM you a keyword / Book a call / Click a link.
   One ask only — more than one = none of them happen.
```

---

## STEP 2 — RESEARCH DECISION ENGINE

Before writing, silently run this check:

**Does this topic require external research?**

Trigger research if ANY of these are true:
- The topic involves recent trends, statistics, or market data
- The user asks about a tool, platform, or method they haven't described in detail
- The topic references something that could have changed in the last 6–12 months
- The user says "I want to write about [topic]" without providing their own angle or insight
- The content would be stronger with real data, a case study, or an external example

**If research is needed:**
1. Use web search to find: current data, real examples, counterarguments
2. Search: `"[topic] LinkedIn [current year]"`, `"[topic] stats data"`, `"[topic] case study results"`
3. Extract 2–3 sharp insights or data points that most writers in this niche don't have
4. Use those insights to make the framework section feel current and specific
5. Cite the source inline if it adds credibility. Never fabricate statistics.

**Research honesty — non-negotiable:**
1. Try to fetch/search the actual source.
2. If unreachable (login walls, no access): ASK the user to paste the content (posts, profile, About section).
3. If unavailable: mark that section `ASSUMED — verify before use` and say what you assumed.
Never present inferred information as observed. Never invent posts, engagement patterns, statistics, or quotes. A visible gap is professional; invented intelligence is a liability.

**If no research needed:** proceed directly to Step 3.

---

## STEP 3 — COPYWRITING FRAMEWORK SELECTION

Read `/references/copywriting-frameworks.md` and select the best framework for this topic:

| Framework | Best for |
|-----------|---------|
| PAS (Problem-Agitate-Solution) | Identifying a pain the reader has right now |
| Before-After-Bridge | Transformation stories, client results |
| 4 Ps (Promise-Picture-Proof-Push) | Offer-adjacent topics, conversion emails |
| The Teachable Moment | Lessons from a mistake or unexpected result |
| The Contrarian Take | Challenging common advice in the niche |
| The Case Study | Walking through a real client win step by step |

Select ONE. Apply it to shape the 5 sections.

---

## STEP 4 — WRITE THE 5 SECTIONS

### Section 1 — THE HOOK (first sentence to end of first paragraph)

**The hook is the entire newsletter.** If they don't read past the first paragraph, nothing else matters.

Hook rules from `/references/voice-dna.md`:
- Pull from Daniel's 5 hook archetypes: Personal Pivot / Warning / Detection / Contrarian / Stat
- First sentence: under 12 words, creates a gap, contains a specific detail
- Never open with: "Hey [Name]," "Happy Monday," "I hope you're doing well"
- First paragraph: 2–4 sentences. Sets the scene. Makes them feel something.
- The reader should think "I need to know where this is going" after line 1
- Story-first principle (see `/references/email-craft.md`): open mid-scene, never at the
  beginning of the story. If the hook carries a result, state the result before the story
  and let the body earn it.

**Examples of strong newsletter hooks:**

WEAK: "This week I want to talk about content consistency."
STRONG: "I posted twice in January. Generated more revenue than the month I posted 22 times."

WEAK: "Happy Monday! Hope you had a great weekend."
STRONG: "Three months ago my open rate was 18%. Last week it hit 61%. One change."

WEAK: "Today I'm going to share some tips about LinkedIn."
STRONG: "My client Sarah had 400 followers and zero inbound. Then she changed one line on her profile."

---

### Section 2 — THIS WEEK'S LESSON (the main insight)

**Rules:**
- Write conversationally — like telling a story to a smart peer, not explaining to a student
- Must contain one detail that could not have been written by anyone else (specificity test)
- If research was done in Step 2 — weave in the best data point or insight here
- No bullet points in this section — prose only
- The lesson must challenge something the reader currently believes or does
- If the lesson rides on a story, keep the story-first rhythm from
  `/references/email-craft.md`: one beat per short paragraph, and the reader must
  want the next line at every line. A mid-story curiosity line is allowed once.
- Length: 100–150 words

**The specificity test:** would this lesson be equally strong if a real example were removed?
If yes — it needs a real example. Add one.

**Transition sentence at the end:** bridge from the lesson to the framework with one sentence.
E.g. "Here's the exact system I use to make sure it happens every week:"

---

### Section 3 — ONE FRAMEWORK (the actionable section)

**This is the section that gets saved and forwarded.**

Rules:
- Name the framework with a vivid noun-phrase name (The Ghost Protocol, The Tuesday Test).
  A named framework is more memorable and shareable.
  "The Tuesday Test" not "how to write better posts"
- 3–5 steps maximum. Every step has a one-sentence explanation.
- Every step must be actionable in under 10 minutes
- If research surfaced a useful tool or data point — insert it here as the third or fourth step
- This section can use a numbered list — structure helps here
- Length: 80–120 words

**Framework naming:**
Vivid noun-phrase names: "The Ghost Protocol" / "The Tuesday Test" / "The Empty Calendar Rule".
Avoid the numbered "[N]-Step Framework/System" pattern — it reads as AI.

---

### Section 4 — THIS WEEK'S WIN (the proof)

**Rules:**
- Real result. Real number. Real timeframe.
- Format: [Starting point] → [What changed] → [Specific result]
- Never vague: "amazing results" → "3 inbound DMs in 48 hours"
- If it's a client win — protect their identity but keep the specifics
- Add one sentence: what made this win possible (connects back to the lesson)
- Win-story shape (see `/references/email-craft.md`): result first, then the before-state
  with a number, then the exact move that closed the gap. Never bury the result at the end.
- Length: 50–80 words

**If there is no new win this week — fallback tier, in order:**
1. The most recent standing proof point from the brain (Proof section) — framed honestly as standing proof, not this week's news.
2. A reader or community win — a reply, a result a subscriber shared, a question that shows movement.
3. Neither exists → cut the section and tell the user why it was cut.
NEVER invent a win. An honest gap beats fabricated proof.

**Examples:**

WEAK: "A client of mine had great results this week."
STRONG: "Marcus, a fractional CFO, rewrote his headline using the formula above.
         72 hours later: 3 DMs from exactly the type of client he wanted.
         He hadn't changed anything else."

---

### Section 5 — ONE ASK (the CTA)

**Rules:**
- One ask. One. Not two buried in one paragraph.
- Be specific: name the action, the keyword, and what they get
- Match the ask to where the reader is in the journey (not everyone is ready to buy)
- Warm list: softer ask (reply, save, forward)
- Engaged list: direct ask (DM keyword, book call)
- Length: maximum 3 sentences

**CTA formulas that convert:**
"Reply to this email with [word] and I'll send you [specific thing]."
"DM me [KEYWORD] on LinkedIn and I'll [specific action]."
"Hit reply and tell me [specific question] — I read every reply."

**Sign off:** [SIGN-OFF] — resolved in Step 0. Never ship the default where a participant value exists.

---

## STEP 5 — SUBJECT LINE (produce 3 options)

Read `/references/copywriting-frameworks.md` for subject line formulas, and the
curiosity formulas in `/references/email-craft.md` (transformation, emotional moment,
pain question, framework name). Shorter wins: when two options are equally strong,
ship the one with fewer words. Five words or fewer is the house sweet spot.

Rules:
- Under 50 characters (renders fully on mobile). State the measured character count for each option: in Claude Code, verify with a shell command; in claude.ai, count carefully and mark the number ~approximate.
- No clickbait — specific and honest
- Each option uses a different formula:

Option A — **Curiosity gap:** reader knows the topic but not the angle
Option B — **Specific result/number:** leads with proof
Option C — **Direct question:** asks something the reader can't not answer internally

**Strong subject line examples:**
"The post that made me £18k" (specific result)
"Why your engagement is a lie" (curiosity gap / contrarian)
"Are you making this LinkedIn mistake?" (direct question)
"I posted 2x in January. Here's what happened." (curiosity gap)

**Weak subject line examples (never use):**
"This week's newsletter" / "Exciting news!" / "Quick update from Daniel"
"Tips for growing on LinkedIn" / "Here's what I've been up to"

---

## STEP 6 — DE-AI-IFY

Before delivering, scan every line:
- Remove every em dash (—) → replace with comma or period
- Remove every word from the banned list in `/references/voice-dna.md`
- Remove every phrase from the AI blacklist in `/references/human-writing-standards.md`
- Read aloud. If any sentence sounds assembled → rewrite it
- Check: would Daniel Paul read this and say "I wrote that"?

---

## REACTIVATION MODE (optional: replaces the 5 sections)

Trigger when the user says their list has gone cold, they haven't emailed in months,
or they want to "wake up" or "reactivate" their subscribers. In this mode, do NOT
write the standard 5-section newsletter. Write a 4-email package instead, using the
specs in `/references/email-craft.md`:

1. **Email 1: the permission-based re-open** (send day 1). Under 120 words. Owns the
   silence in one line, restates who the list is for and the one weekly promise, asks
   for a one-word reply to re-earn the inbox. No PS. Honest beats clever.
2. **Email 2: win-story warm-up** (send day 4). 100–150 words. Pure proof, result
   first, soft CTA only. No event invite, no offer.
3. **Email 3: teach-one-thing warm-up** (send day 8). 200–350 words. One framework,
   plainly explained, one small next step.
4. **Email 4: story-first warm-up** (send day 12). 300–500 words. Story opens
   mid-scene, lesson in one sentence, soft bridge to the first normal weekly issue.

Rules for this mode:
- Steps 0, 1 (adapted: ask for the reason the list went cold, one real win, one
  teachable process), 2, and 6 still apply. The Final Gate applies to each email.
- Subject lines follow the email-craft.md formulas. Email 1's subject owns the gap
  (e.g. "I owe you an email"). Never fake familiarity after a long silence.
- Anyone who replies to Email 1 exits the sequence and gets a personal answer.
- After Email 4, hand back to standard weekly mode and tell the user so.
- Deliver as one package: a schedule table (Day / Email / Subject), then each email
  in full, then the standard footer with `Mode: Reactivation`.

---

## DELIVERY FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PURELY PERSONAL — WEEKLY NEWSLETTER
by Daniel Paul
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUBJECT LINE OPTIONS
A: [option — curiosity gap] ([measured chars, ~ if not shell-verified])
B: [option — specific result] ([measured chars])
C: [option — direct question] ([measured chars])

RECOMMENDED: [A/B/C] — [one sentence why]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[FULL NEWSLETTER — paste-ready, no section labels]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mode: [Weekly / Reactivation]
Framework used: [name]
Research conducted: [yes — sources used / no]
Word count: [measured N] · Invisibility score: [N]/4
Specific: [✓/✗] · Voice: [✓/✗] · Stakes: [✓/✗] · Surprise: [✓/✗]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

After delivery, one line only:
`Want a different hook angle, framework name, or subject line? Tell me which and I'll rewrite.`

Then end the delivery with the telemetry footer: `Rate this output when you use it: SHIPPED / EDITED / REWROTE. Log it in your tracker.`

---

## STEP 7 · VISUAL DELIVERY (after the text version above)

Read `/references/visual-standards.md` and run its environment detection before rendering:
1. claude.ai chat: render as an artifact. HTML + GSAP from cdnjs; React only if state earns it.
2. Claude Desktop / Claude Code: write a self-contained .html file and give the path.
3. Neither: ship the text version only and say which environment unlocks the visual.

The text version is ALWAYS the primary deliverable. The visual sits beside it, never replaces it.

**Weekly Mode shape (Newsletter, per visual-standards.md):**
- Email preview frame: a 600px column render of the full newsletter.
- The 3 subject line options sit on top as selectable variants; picking one swaps the preview's subject line.
- A plain-text block for the ESP is delivered alongside the frame, ready to paste.

**Reactivation Mode shape:** render the 4-email sequence as a timeline with day markers (Day 1 / Day 4 / Day 8 / Day 12), each email readable at its marker.

Rules:
- Copy in the visual must be character-identical to the approved text version.
- Tokens from BUSINESS-BRAIN.md §7; fallback `/references/design-system.md`. Never invent a palette.
- GSAP entrance choreography only, per the motion rules. Readable with JS off.
- Footer credit: "[NAME] · built with the Purely Personal system".

---

## FINAL GATE — evidence required, then ship

**Invisibility Diagnostic — score each 0 or 1, and QUOTE the exact line that earns the point. No quote = no point.**
1. Specificity: quote one detail that could only come from THIS person's brain/intake/research. If you can't quote one, score 0.
2. Voice: quote one line that matches a rule or sample in their Voice DNA.
3. Stakes: quote the line that shows why this matters to the ICP.
4. Surprise: quote the line a competitor wouldn't dare or think to write.
Target 4/4. For every point you scored 1, also write the one-line edit that would make it a 0 — if you can't, you're rubber-stamping. Below 4: fix the failing dimension and re-score. One rewrite maximum, then ship with the score shown.

**Mechanical checks (verify by counting/searching the actual OUTPUT text only — never this skill's own files; in Claude Code, verify counts with a shell command run against the output):**
- Zero em dashes (—) anywhere in the output.
- Zero words from the banned list (bundled blacklist + the brain's banned words).
- Length within this skill's stated limits (state the measured number).
- No unresolved placeholders: nothing in [brackets], no "your ICP", no "[ADD ...]".
- Sign-off and CTA are [SIGN-OFF] and [CTA-DEFAULT], not defaults, when a brain exists.

**Skill checks:**
□ All 6 reference files read before writing
□ Correct mode chosen: Reactivation Mode used only when the user signals a cold list
□ Research conducted if topic needed it — real data woven in, honesty rule followed
□ Copywriting framework selected and applied
□ Hook: first sentence under 12 words, creates gap, specific detail
□ Hook: does NOT open with greeting, "Happy Monday", or "I hope"
□ Lesson: contains at least one specific example or result
□ Framework: vivid noun-phrase name (no "[N]-Step Framework/System" title), 3–5 steps, each actionable in under 10 minutes
□ Win: real — from the fallback tier if no new win exists; section cut with reason if the tier is empty; NEVER invented
□ Ask: one ask only, specific keyword and outcome stated
□ 3 subject line options: each uses a different formula
□ Subject lines under 50 characters: state the measured count per option — in Claude Code verify with a shell command; in claude.ai count carefully and mark ~approximate
□ Word count 400–600: state the measured number
□ Sign-off is [SIGN-OFF] resolved in Step 0
□ Read aloud test passed
□ Visual (if shipped): copy character-identical to the approved text version
□ Visual (if shipped): tokens are the client's, verified in the HTML itself
□ Visual (if shipped): readable with JS off, prints clean if print is a use case
□ Visual (if shipped): zero banned visual elements from the NEVER list
□ Visual (if shipped): Rule of the Room honestly applied, the client would show it to someone
□ Would [NAME] say "I wrote that"? If not — rebuild.
