---
name: content-strategy
description: >
  Builds a complete LinkedIn content strategy for any client — positioning, 5–6 ownable
  content pillars, live competitor research, audience language mapping, and a 90-day
  post-by-post plan the client can execute the next morning. ALWAYS use this skill when
  the user says "content strategy", "content pillars", "build my strategy", "create a
  content plan", "90-day plan", "what should I post" (as a direction question about their
  content overall), or needs to define their LinkedIn positioning from scratch. Do not
  sketch pillars or content plans directly without running this skill. NOT for writing a
  single post — "what should I post today" about one post → linkedin-caption-writer.
  Part of the Purely Personal system by Daniel Paul.
---

# Content Strategy — Purely Personal
# by Daniel Paul · Purely Personal

Read ALL reference files before running research or writing:
- `/references/voice-dna.md` — Daniel's ICP snapshot, what good positioning looks like
- `/references/human-writing-standards.md` — what world-class content looks like
- `/references/copywriting-frameworks.md` — how to think about content intent and structure
- `/references/design-system.md` — brand tokens for the strategy header and the Step 9 visual
- `/references/creator-systems.md` — the five content systems behind the biggest solo creators: the topic-by-format grid, the four content angles, the pillar-to-micro cascade, the depth-niche test, and 2026 cadence data. Steps 5 and 7 depend on it.
- `/references/visual-standards.md` · environment detection, the HTML+GSAP stack, motion and design rules, the Strategy document shape, and the visual quality gate. Step 9 depends on it.

## WHERE THIS SKILL SITS

**Reads from:** BUSINESS-BRAIN.md · the client's intake answers and live research
**Hands off to:** the weekly operating rhythm (Step 7): newsletter-writer for the weekly pillar piece · linkedin-carousel-builder and linkedin-cheatsheet-builder for the visual cuts · linkedin-caption-writer for the daily topics, one at a time
Tell the user the next step in one line after delivering.

One job: a strategy so specific and grounded in the client's real niche that they read the pillars
and think "this is exactly what I've been trying to say — just clearer than I could say it."

**The standard for every pillar:**
Generic pillar names are noise.
"Thought leadership" is not a content pillar.
"LinkedIn tips" is not a content pillar.
"Personal brand growth" is not a content pillar.

A content pillar is a specific claim, audience problem, or angle that only this client
can own in this niche right now. It should make competitors uncomfortable.

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

If client information isn't provided, ask ALL in ONE message:

```
╔══════════════════════════════════════════════════════╗
║  PURELY PERSONAL — CONTENT STRATEGY                 ║
║  by Daniel Paul                                      ║
╚══════════════════════════════════════════════════════╝

7 things to build a strategy you can actually execute:

1  WHO ARE YOU?
   Name + role + what you do.
   "Sarah — former Head of Product at [company],
    now fractional CPO for Series A startups."

2  WHAT DO YOU SELL AND WHO BUYS IT?
   Your core offer. The specific problem it solves.
   The specific person who buys it — role, stage, situation.

3  WHAT SHOULD LINKEDIN DO FOR YOU?
   Get inbound leads / Build authority / Land speaking /
   Attract talent / Raise investment / Something else?
   Be specific about the outcome you need in 90 days.

4  YOUR UNIQUE ANGLE OR LIVED EXPERIENCE
   What do you know that others in your niche don't?
   What background gives you an unusual perspective?
   What contrarian belief do you hold about your industry?
   This is the most important question. Take your time.

5  YOUR 3 BEST CLIENT RESULTS
   Specific outcomes. Numbers where possible.
   "Helped a client go from 0 to 12 inbound calls/month in 8 weeks."
   These become your proof points — the foundation of authority.

6  YOUR TOP 3 COMPETITORS OR PEERS ON LINKEDIN
   Who are they? What are their LinkedIn profile URLs?
   What do they do well? Where do they fall short?

7  WHAT HAVE YOU TRIED ALREADY?
   Any content you've posted? What worked? What didn't?
   What topics felt natural? What felt forced?
```

---

## STEP 2 — DEEP RESEARCH PROTOCOL

**This step is non-negotiable. Never skip it silently. Never replace it with assumed knowledge without saying so.**

**Research honesty — non-negotiable:**
1. Try to fetch/search the actual source.
2. If unreachable (login walls, no access): ASK the user to paste the content (posts, profile, About section).
3. If unavailable: mark that section `ASSUMED — verify before use` and say what you assumed.
Never present inferred information as observed. Never invent posts, engagement patterns, statistics, or quotes. A visible gap is professional; invented intelligence is a liability.

Run ALL of the following searches before building the strategy:

**Search 1 — Niche saturation scan:**
`"[niche] LinkedIn creators" OR "[niche] LinkedIn content" [current year]`
Question to answer: What angles are overused? What are the top creators talking about constantly?
Document: top 3 saturated topics to avoid.

**Search 2 — Audience pain mapping:**
`"[target audience role] challenges [current year]" OR "[target audience] LinkedIn`
`"[target role] frustrations" OR "[target role] community discussions"`
Question to answer: What exact language does the ICP use to describe their problems?
Document: 5–8 exact phrases the audience uses — not paraphrases.

**Search 3 — Competitor content gaps:**
Visit top 3 competitor LinkedIn profiles. Review their last 20 posts.
Question to answer: What topics are they NOT covering? What questions do their followers ask
that they never answer well?
Document: 3 specific gaps this client can own.

*If the Apify connector is available in this session:* use the
`apify--linkedin-profile-scraper` actor (or the profile-posts equivalent) to pull the
top 3 competitors' recent posts — cap 20 posts per competitor, nothing beyond that.
Before running, state in one line what will be scraped and why, e.g. "Pulling the last
20 public posts from [competitor 1–3] to map their content gaps." Scraped posts count
as observed data.

*Fallback branch (no Apify, or LinkedIn auth walls — both are normal, expect them):*

| Problem | What to do |
|---------|------------|
| Apify connector not installed | Ask the user to paste 3–5 recent posts per competitor. Proceed from there. |
| Actor runs but profile is blocked or empty | Same — ask for pastes. |
| Nothing available at all | Mark the Competitor Study `ASSUMED — based on positioning/website only`, build it from their website and public positioning, and say so plainly in the report. |

Never fabricate post history or engagement to fill the gap. A zero-Apify user gets the
full strategy — just from pasted or assumed competitor data, clearly labelled.

**Optional X evidence lane, only when requested:**

Keep the LinkedIn Actor above as the default. If the user requests public X
post or audience evidence, read `/references/xquik-actors.md` before any
Actor call. It adds both Xquik routes without replacing LinkedIn research.

**Search 4 — Trending angles:**
`"[niche] [year] trends" OR "what's changing in [niche]"`
Question to answer: What is shifting in this industry right now that most creators are ignoring?
Document: 1–2 forward-looking angles nobody is talking about yet.

**Research output:** Summarise findings in 4 bullets before proceeding. This grounds the entire strategy in real intelligence.

---

## STEP 3 — POSITIONING STATEMENT

Write a 2-paragraph positioning statement (100 words total).

**Paragraph 1 — The specific person:**
Who is this? What do they do? What makes their angle different from every other person
in this niche? The positioning statement must make a competitor reading it think
"they're going after the exact audience I'm ignoring."

**Paragraph 2 — Why follow them:**
Why would the target audience follow this specific person over anyone else talking about
this topic? The answer must be rooted in their lived experience, their contrarian belief,
or their specific proof — not in generic credentials.

**Positioning statement test:**
Could this same positioning statement apply to the top competitor in the niche?
If yes — it's not specific enough. Rewrite.

---

## STEP 4 — AUDIENCE PSYCHOLOGY SNAPSHOT

Not demographics. Psychology.

**Current situation:** What are they experiencing right now — specifically?
(Not "they want to grow" but "they've been posting 3x/week for 4 months and have 800 followers
and zero inbound leads and are questioning whether LinkedIn works for their niche at all.")

**Core frustration:** The specific thing they can't figure out. In their exact words.
(Pull from the audience language research in Step 2.)

**Desired outcome:** What do they actually want at the end of this journey?
(Specific: "Wake up on Monday with 3 calls already booked from people who found them.")

**Trigger moment:** What makes them search for a solution today specifically?
(The event that tips them from "thinking about it" to "doing something about it.")

**Buying objection:** The one thing that would stop them from working with this person even
if they wanted to. Address this in the content strategy from day one.

---

## STEP 5 — THE 5–6 CONTENT PILLARS

Each pillar requires ALL of the following. No exceptions.

```
PILLAR [N]: [NAME — 3–5 words, ownable, specific]
─────────────────────────────────────────────────
What this pillar owns:
[One sentence — the specific claim, angle, or territory this pillar holds]

Content intent:
[Educate / Build trust / Generate leads / Thought leadership / Entertainment]

Why this client can own it:
[Their specific lived experience, proof, or angle that makes this pillar theirs]

What competitors are doing with this topic:
[What they're saying that's saturated — and what gap is left]

Research finding that informed this pillar:
[Specific data point or audience phrase from Step 2 research]

3 post ideas to start immediately:
1. [Topic + hook angle — enough detail to write the post tomorrow]
2. [Topic + hook angle]
3. [Topic + hook angle]
```

**Calibration — your pillars must be THIS specific:**
For a fractional-CFO client: PILLAR: "The Series B Blind Spot" — the financial reporting gaps that quietly kill Series B raises. Ownable because only she can claim it: it comes from her dataset of 40 companies she has taken through diligence, not from opinion. Sample post angles: (1) "The 3 line items every Series B investor checks first — and the one 80% of my 40 clients had wrong." (2) "Your Series A deck got you funded. The same deck structure will sink your B — here's why." (3) "I watched a £4M raise die over a cap table tab. The 20-minute fix that would have saved it."
A pillar a competitor could paste into their own strategy is not a pillar. It's a category.

**Pillar validation tests (run every pillar through these):**

✓ Could a competitor use this same pillar name? If yes — it's not specific enough.
✓ Is there a post idea in this pillar that could go viral because it's counterintuitive?
✓ Does the client have a real story, result, or opinion they can anchor this pillar to?
✓ Does this pillar connect to the ICP's core frustration identified in Step 4?
✓ Is at least one post in this pillar explicitly conversion-focused (asks for a lead or a reply)?

If any pillar fails more than one test — rewrite before proceeding.

**Depth-niche test (second gate, run after the 5 checks above pass):**
From `/references/creator-systems.md` System 4. Score each pillar on four checks:
1. Search test: when the ICP describes this problem in their own words (Step 2 phrases), is this client the obvious answer?
2. Referral sentence test: a stranger can repeat it in one sentence. "She's the one who [outcome] for [person]." No "and", no "but also".
3. Say-no test: the pillar visibly excludes some plausible buyers. Excludes nobody = attracts nobody.
4. Depth test: the client could publish weekly on it for a year without repeating, because it sits on lived experience, a dataset, or a body of client work.
4/4 = power position, keep. 3/4 = fix the failing check. 2 or below = it's a category, not a niche. Go one level narrower (add a specific person, stage, or moment) and re-test.

---

## STEP 6 — COMPETITOR CONTENT STUDY

For each of the top 3 competitors from intake and research:

```
COMPETITOR: [name]
LinkedIn: [URL if available]

What they do well:
[Specific strength — hook style, post format, engagement driver]

What they consistently miss:
[Specific gap — the question their audience asks that they never answer well]

What this client should do differently:
[Specific positioning move that creates clear differentiation]
```

---

## STEP 7 — 90-DAY CONTENT PLAN

**Deliver exactly this structure — completeness is checkable against it:**
- Month 1: 16 fully specified topics (4 per week, each with a hook angle).
- Months 2–3: explicit pillar-rotation schedules with a named theme per week, plus Week 5 fully specified (4 topics with hook angles) as the template for the rest.

**Month 1 — Foundation (Weeks 1–4) — FULLY SPECIFIED, GRID-GENERATED**
Goal: establish the pillars, build trust, prove the ICP is being spoken to directly.
Post mix: 70% education/trust, 20% proof, 10% CTA.
Focus pillar: the one that most closely mirrors the ICP's core frustration.

Generate the 16 topics mechanically. Do not brainstorm them:
1. Build the topic-by-format grid (`/references/creator-systems.md` System 1): rows = the Step 5 pillars, columns = the five angles (Actionable / Analytical / Aspirational / Anthropological / Proof). Fill every cell with a post concept at the depth of the worked mini-grid in that file.
2. A 5-pillar grid yields 25+ concepts. Select the 16 strongest cells for Month 1 and bank the rest as the client's idea library for Months 2–3.
3. Each week's 4 topics follow the angle balance rule (System 2): 2 actionable/analytical, 1 aspirational/proof, 1 anthropological.
4. Label every topic with its pillar and angle: `[Pillar 2 · Anthropological]`. An unlabelled topic is an unfinished topic.

Week 1: [4 grid cells, each with hook angle + pillar/angle label, one per day Mon/Wed/Thu/Fri]
Week 2: [4 grid cells with hook angles + labels]
Week 3: [4 grid cells with hook angles + labels]
Week 4: [4 grid cells with hook angles + labels] — include one conversion post at end of week
Total: 16 topics, each written so the client could draft the post tomorrow.

**Month 2 — Authority (Weeks 5–8) — PILLAR ROTATION + WEEK 5 SPECIFIED**
Goal: establish a point of view, publish the contrarian takes, build social proof.
Post mix: 50% education, 30% proof/case studies, 20% CTA.

Week 5: [FULLY SPECIFIED — 4 topics with hook angles, same depth as Month 1]
Week 6: [Pillar rotation: which pillars, in what order + one-line week theme]
Week 7: [Pillar rotation + one-line week theme]
Week 8: [Pillar rotation + one-line week theme]

**Month 3 — Conversion (Weeks 9–12) — PILLAR ROTATION SCHEDULE**
Goal: convert attention into leads. Direct asks, explicit CTAs, offer-adjacent content.
Post mix: 40% education, 30% proof, 30% direct conversion.

Week 9: [Pillar rotation + one-line week theme, conversion intent noted]
Week 10: [Pillar rotation + one-line week theme, conversion intent noted]
Week 11: [Pillar rotation + one-line week theme, conversion intent noted]
Week 12: [Pillar rotation + one-line week theme, conversion intent noted]

At the start of each new month, the client re-runs this skill's Step 7 (or feeds the week theme into linkedin-caption-writer) to expand the rotation into full topics.

**The weekly operating rhythm: how the plan runs inside the suite**
Every strategy ships with this rhythm (pillar-to-micro cascade, `/references/creator-systems.md` System 3). One deep piece per week, cut into everything else. Adapt days to the client's calendar, keep the sequence:

```
MON  Run newsletter-writer on this week's focus pillar → the pillar piece (deep dive, carries the CTA)
TUE  Run linkedin-carousel-builder on the pillar piece's framework → document carousel post
WED  Run linkedin-caption-writer on the strongest standalone point → text post (angle-labelled)
THU  Run linkedin-cheatsheet-builder on the checklist/steps → cheatsheet post OR second caption-writer post
FRI  Run linkedin-caption-writer on the story or contrarian point → anthropological/aspirational text post
DAILY  15 minutes: reply to every comment within the first hour, comment on 3–5 ICP posts
```

Why this shape (System 5 data): 3–5 posts/week is the 2026 sweet spot, document carousels are the top-performing format, formats rotate automatically (same format twice in a row suppresses reach), and text posts carry the story angles. Links go in the first comment or a DM keyword, never the post body.

---

## STEP 8 — QUICK WINS (start this week)

Three actions this week before the 90-day plan begins:

**Quick Win 1:** Profile change (under 30 minutes)
[Specific change — one sentence. Exact copy to update the headline if needed.]

**Quick Win 2:** First post to publish (this week)
[Specific topic + hook angle + which pillar it belongs to]

**Quick Win 3:** One engagement action to do daily (10 minutes per day)
[Specific: comment on [type of post] using [specific approach] to build niche visibility]

---

## STEP 9 · THE STRATEGY VISUAL (standard whenever the environment allows)

The full text strategy from the Delivery Format is ALWAYS delivered. The visual sits beside it, never instead of it. Follow `/references/visual-standards.md` end to end.

**Environment detection first:**
1. **claude.ai chat**: render as an interactive HTML artifact with GSAP loaded from cdnjs (`https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`, plus ScrollTrigger when the page scrolls through sections).
2. **Claude Desktop / Claude Code**: write one self-contained file `strategy-[client-slug].html`, GSAP via the same cdnjs script tag, and give the path.
3. **Neither**: deliver the text strategy and say in one line which environment unlocks the visual.

**Shape (the Strategy document shape in visual-standards.md):** an animated one-pager or horizontal GSAP deck with these sections:
- Hero: the positioning promise as the single biggest statement on the page.
- Pillar cards: one card per pillar (name, what it owns, one proof line), staggered in with fade-up entrances.
- Month-1 topic grid: the 16 topics as a real grid (weeks as rows), every cell carrying its pillar + angle chips from Step 7. Not a bulleted list wearing a border.
- Weekly operating rhythm: the Mon to Fri skill schedule as a horizontal timeline band.
- Key numbers count up on entry (16 topics, 90 days, posts per week, the client's proof-point numbers): gsap.to() on textContent with snap.

**Motion and design rules come from visual-standards.md:** entrance choreography only (fade-up 20-40px, 0.06-0.12s stagger, ease "power3.out"), each section animates once at 70% viewport, content fully readable with JavaScript disabled. Tokens from the brain's design section if present, else `/references/design-system.md`. One accent color, typographic-first, no banned visual elements. Copy in the visual must be character-identical to the approved strategy text: same pillar names, same topic lines, same numbers. No paraphrasing during layout.

---

## DELIVERY FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PURELY PERSONAL — CONTENT STRATEGY
[Client Name] · Built by Daniel Paul
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESEARCH SUMMARY
[4 bullet findings from Step 2]

POSITIONING STATEMENT
[2 paragraphs]

AUDIENCE PSYCHOLOGY SNAPSHOT
[5 sections from Step 4]

CONTENT PILLARS
[5–6 pillars, all fields complete]

COMPETITOR CONTENT STUDY
[3 competitors from Step 6]

90-DAY CONTENT PLAN
[Month 1: 16 grid-generated topics with hook angles + pillar/angle labels /
 Months 2–3: pillar rotations + themes, Week 5 fully specified]

WEEKLY OPERATING RHYTHM
[The Mon–Fri skill schedule from Step 7: which suite skill runs on which day,
 pillar piece first, cascade after, daily 15-minute engagement block]

QUICK WINS — START THIS WEEK
[3 actions]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then deliver the Step 9 visual (or name the environment that unlocks it), and point to the next step: feed Week 1's first topic into linkedin-caption-writer.

Then end the delivery with the telemetry footer: `Rate this output when you use it: SHIPPED / EDITED / REWROTE. Log it in your tracker.`

---

## FINAL GATE — evidence required, then ship

The strategy document is client-facing prose. It passes the same bar as a published post.

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
□ Step 0 context resolved (brain / foundation docs / labelled default)
□ All 5 reference files read before building
□ All 7 intake answers received before research
□ All 4 searches conducted — real findings documented; anything unverifiable marked ASSUMED
□ Positioning statement: specific to this person, fails the competitor test
□ Audience snapshot: uses exact phrases from research — not paraphrases
□ 5–6 pillars: all fields complete, all 5 validation tests passed, as specific as the Series B Blind Spot example
□ Every pillar scored on the depth-niche test (search / referral sentence / say-no / depth): 3/4 minimum, failures narrowed and re-tested
□ No generic pillar names ("thought leadership", "personal brand tips", "LinkedIn growth")
□ Every pillar: tied to a real proof point this client owns
□ Competitor study: 3 competitors, each with gap and differentiation move — or marked ASSUMED per the Search 3 fallback
□ 90-day plan matches the Step 7 structure: 16 Month-1 topics with hook angles, Week 5 fully specified, weekly rotations for the rest
□ Month-1 topics generated from the pillar-x-angle grid: every topic carries a pillar/angle label, each week meets the angle balance rule
□ Weekly operating rhythm included: named suite skill per day, pillar piece before cascade cuts
□ Quick wins: specific, actionable, executable this week
□ Visual delivered per Step 9 when the environment allows it; full text strategy delivered either way
□ Visual copy character-identical to the approved text: pillar names, topic lines, numbers
□ Visual tokens are the client's: grep the HTML for the brain's hex codes
□ Visual readable with JS off; prints clean if print is a use case
□ No banned visual elements, and the Rule of the Room honestly applied: would the client show this to someone?
