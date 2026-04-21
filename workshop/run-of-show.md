# Workshop Run-of-Show
### Build a Business That Runs by Itself — 2-Day Live Workshop

**Duration:** Pre-setup (30 min async) + Day 1 (2h live) + Day 2 (2h live)
**Outcome:** Every attendee leaves with a filled `BUSINESS-BRAIN.md` and 5 AI executives installed.
**Delivery:** Zoom. Single facilitator. 10–50 attendees.

---

## Philosophy

> One pattern. Five canvases. Don't teach more than you have to.

The whole workshop teaches exactly one idea: **the Universal Engine Pattern** (Input → Brain → Review → Ship → Log). Everything else is applying that pattern to 5 engines. Attendees leave with pattern recognition, not a pile of techniques.

**Rule of 3 per session.** Max 3 skills demoed live. Max 3 priorities called out. Anything more is noise.

---

## Pre-Setup Session (30 min async, before Day 1)

### Delivery
Video + checklist emailed 48h before Day 1. Attendees watch + install on their own time.

### What they do
1. Install Claude Code (~5 min)
2. Clone the `purely-personal` repo (~2 min)
3. Install the plugin: `claude plugin install .` (~1 min)
4. Run health-check: `/plugin list` → confirm `purely-personal` shows all skills + commands (~1 min)
5. Optional: install Apify MCP for automated scraping (~10 min)
6. Join the Day 1 Zoom 5 minutes early

### Deliverable
Attendee shows up with a working plugin and their LinkedIn URL + website URL + 3 competitor URLs in a notes doc.

### Failure mode
If the plugin doesn't install, the facilitator runs a 15-min troubleshooting office-hours call 24h before Day 1. Five common errors + fixes pre-documented.

---

# DAY 1 — The Foundation (2 hours, 120 min)

> Theme: *Who you are, what you sell, who you serve.*
> Outcome: Worksheets 1–3 complete. `BUSINESS-BRAIN.md` sections 1–4 filled.

---

### 00:00 — Welcome + Frame (5 min)

**Say verbatim:**
> "For the next two days we're building a business that runs without you. Not automated, not delegated — actually running. One document. Five AI executives. Zero SaaS. You'll leave with every system working on your laptop."

**Show on screen:**
- The V3 BUSINESS-BRAIN render (full page) — "this is what you have at the end of Day 2"
- The Actions Panel close-up — "these are the 5 engines you'll install"

**Rule:** Don't ask attendees to introduce themselves. Steals 20 minutes. Let the work introduce them.

---

### 00:05 — Teach: The Universal Engine Pattern (10 min)

**The only framework you teach. Do this slowly.**

Show the diagram:

```
 INPUT → BRAIN → REVIEW → SHIP → LOG
```

**Explain (verbatim-ish):**
> "Every engine you install works the same way. A trigger comes in. Your Brain supplies context — voice, ICP, positioning. The AI produces output. You approve or edit. It ships. It logs back to your Brain. Five engines, one pattern. Once you've learned it for Marketing, you've learned it for all five."

**Check for understanding:**
> "Put a 👍 in chat if you see how this is different from 'use AI to write a post for me'."

Wait for ~60% ticks. If <50%, re-explain with the Marketing example.

---

### 00:15 — Activity 1: Worksheet 1 — YOU™ (15 min)

**Taki pattern: teach → fill → share → debrief → capture**

| Min | Phase | What happens |
|-----|-------|--------------|
| 0–1 | Teach | Show the 4-col Taki worksheet. "Column 3 is your current line. Column 4 is your sharpened one." |
| 1–6 | Fill | Attendees open `fillable.html` in their browser. Fill silently. |
| 6–11 | Share | Zoom breakout rooms of 2. One round of feedback each. |
| 11–14 | Debrief | Main room. Call 2 volunteers to share their Column 4. Annotate live. |
| 14–15 | Capture | Click **"Copy to Brain"** button. Paste into `BUSINESS-BRAIN.md`. |

**Facilitator rule:** Don't read the worksheet aloud. Let attendees read. Silence is fill time.

**End state:** Every attendee has a tagline + voice rules in their Brain.

---

### 00:30 — Live Demo 1: Voice Extraction (10 min)

**The first wow moment.**

Screen-share Claude Code. Run on your own filled `BUSINESS-BRAIN.md`:

```
Analyze my voice rules + last post opening. What hook pattern am I unconsciously using? Name it so I can reuse it.
```

Watch Claude name your signature hook pattern. Read it out.

**Frame it:**
> "This is what happens when the AI has memory. It's not writing for you — it's writing *as* you."

---

### 00:40 — Activity 2: Worksheet 2 — The Offer™ (15 min)

Same Taki pattern as Activity 1. 15 min. Attendees fill + share + capture.

**Debrief prompt:** "Who's willing to say their offer out loud?"

Call 3 volunteers. After each reads, ask: "Can I repeat that back?" If you can't remember it verbatim, the offer is too long. Push them to sharpen.

**End state:** Brain sections 1–3 filled (Operator + Voice + Business).

---

### 00:55 — Break (5 min)

Stretch. Refill. Say "back in 5."

---

### 01:00 — Live Demo 2: The $75K Moment (8 min)

**The second wow moment.**

Show the rendered V3 BUSINESS-BRAIN with your filled Business section:

```
/render-brain
```

The big red `$75K` card drops. Let it sit. Don't explain.

**After 5 seconds, say:**
> "That's your hero stat. Every time you open your Brain, you see the number you're working toward. Every engine reads that number and pulls toward it."

---

### 01:08 — Activity 3: Worksheet 3 — Your One Client™ (15 min)

Same Taki pattern. This is the longest fill (12 min guideline) — ICP is where people get stuck.

**Debrief prompt:** "If you can't name one real person who fits your ICP, raise your hand." Work with them live. Usually 2–3 people — the rest learn by watching.

**Wow moment in the debrief:** When you narrow an ICP from "SaaS founders" to "SaaS founder, $500k–$5M ARR, sells B2B, 1–5 person team, does their own marketing," the whole room feels the shift.

**End state:** Brain sections 1–4 filled.

---

### 01:23 — Live Demo 3: Sales Engine Preview (10 min)

**Plant the seed for Day 2.**

Run on your Brain:

```
/sales-engine
```

Watch Claude find 10 prospects matching your ICP. Show the scoring. Read one prospect's personal hook aloud.

**Frame it:**
> "You're not going to run this tomorrow. You're going to run it every Tuesday at 9am until one of these engines pays for the workshop 100x over."

---

### 01:33 — Q&A (15 min)

Open floor. Fifteen minutes is enough. If questions run out at 10 min, let people leave early — respect is a gift.

**Common questions + answers pre-scripted:**

| Q | A |
|---|---|
| "What if I don't have a LinkedIn?" | "Use any platform. Paste 10 of your own posts from anywhere." |
| "Can I run this without Apify?" | "Yes. You just paste data manually. Adds 20 min to Brain build." |
| "What if my ICP changes?" | "Edit your Brain. Every engine re-reads it on next run." |
| "How often do I run each engine?" | "Marketing weekly. Sales weekly. Ops daily. Cash weekly. Leadership daily." |

---

### 01:48 — Preview Day 2 + Close (7 min)

**Say:**
> "Tomorrow: the other 4 engines + your full Brain rendered. You'll leave with a one-pager that looks like it cost $5k and 5 engines running. Before tomorrow: finish worksheets 1–3 if you didn't. Take 10 minutes tonight."

**Show the V3 Brain render one more time.** Linger on it.

**Assignment:**
- Finish worksheets 1–3 tonight
- Paste your competitor URLs into a notes doc (you'll need them Day 2)

**End exactly at 01:55.** Never run over.

---

# DAY 2 — The Engines (2 hours, 120 min)

> Theme: *What runs itself.*
> Outcome: Worksheets 4–5 complete. Full Brain rendered. 5 engines installed. 1 committed to run unattended for 7 days.

---

### 00:00 — Welcome Back + Recap (5 min)

**Say:**
> "Yesterday: who you are, what you sell, who you serve. Today: how they find you, what keeps them up, and how you run all 5 engines. By 12:00, your Brain is rendered and your C-Suite is hired."

**Show on screen:** the Universal Engine Pattern diagram again. "Same pattern. Four more canvases."

---

### 00:05 — Activity 4: Worksheet 4 — The Gaps™ (20 min)

**The longest activity.** 20 min because attendees are scraping competitor sites and pulling Reddit pain.

| Min | Phase | What happens |
|-----|-------|--------------|
| 0–2 | Teach | Show the competitor matrix format. "Three rows: competitor / their angle / YOUR gap to own." |
| 2–12 | Fill | Attendees open `fillable.html` for Worksheet 4. Paste competitor URLs, write angle + gap. Add 4 pain verbatims from Reddit/DMs. |
| 12–17 | Share | Breakouts of 3. Each shares one gap and one pain theme. |
| 17–19 | Debrief | Call 2 volunteers. Focus on the "gap to own" — often generic on first pass. Sharpen live. |
| 19–20 | Capture | Copy to Brain. |

**Wow moment:** When someone's competitor matrix shows three competitors all saying the same thing, the gap jumps out.

---

### 00:25 — Live Demo 4: Full Competitor Matrix Render (5 min)

```
/render-brain competitor
```

Show the violet gap blocks full-bleed. "This is the asset you screenshot and share on LinkedIn."

---

### 00:30 — Activity 5: Worksheet 5 — Your Engines™ (15 min)

Same Taki pattern. Brand + AI Visibility + Goals all in one worksheet.

**Debrief prompt:** "What's your 90-day priority — in a single sentence with a number in it?"

Call 3 volunteers. If their priority doesn't have a number, push: "What's the number?"

**End state:** All 5 worksheets filled. `BUSINESS-BRAIN.md` sections 1–9 complete.

---

### 00:45 — Break (5 min)

---

### 00:50 — Live Demo 5: `/render-brain` — The Reveal (8 min)

**The biggest wow moment.**

Run on your filled Brain:

```
/render-brain
```

The full V3 one-pager loads. Scroll through it slowly. Don't narrate.

**After a full scroll:**
> "This is your Brain. Every engine reads it. It's a single markdown file on your laptop. You can print it. You can share it. You can edit it in your text editor. It's yours — not locked in someone's SaaS."

**Tell attendees:**
> "Run `/render-brain` on your own Brain right now."

Wait 90 seconds. Let them react.

**Collect reactions in chat:** "Drop an emoji in chat when yours loads."

---

### 00:58 — The Four-Engine Tour (45 min, 10 min each)

**Teach breadth. One demo per engine. Same Universal Engine Pattern applied each time.**

#### Sales Engine — 10 min

```
/sales-engine
```

- Shows 10 prospects scored
- Draft 3-step outreach for top 3
- Frame it: "Your Tuesday 9am ritual."

**After demo:** "Open a terminal. Run this on your Brain. Right now."
90 seconds of silence. Let them do it.

#### Operations Engine — 10 min

```
/operations-engine inbox
```

- Inbox triage mode
- 5-bucket categorize (urgent / reply / FYI / delegate / delete)
- Drafts shown
- Frame it: "Your 7am Monday ritual."

**After demo:** attendees don't need to run this live — requires Gmail connector. Instead, show the output on your screen and let them see the pattern.

#### Cash Engine — 10 min

```
/cash-engine forecast
```

- Pulls Stripe (or paste manually)
- 90-day forecast vs Brain's $75K goal
- Flags risks
- Frame it: "Your Friday 4pm ritual."

**Say:** "If the forecast says you're behind, good. Better to see it now than on day 89."

#### Leadership Engine — 10 min

```
/leadership-engine today
```

- Yesterday recap across 4 engines
- Today's 3 priorities
- Open loops
- The one thing NOT to do

**Frame it:** "This is your morning brief. Run it before coffee."

**After demo:** "Run this on your Brain tomorrow morning and post the output in the workshop Slack."

---

### 01:43 — Q&A + Commitment (12 min)

Open Q&A for 5 min.

**Then:**
> "Before you close the Zoom, name one engine you'll run unattended for 7 days. Drop it in chat."

Wait for the list. Call out 5 by name and commit to DM check-in on Day 7.

**Common final questions:**

| Q | A |
|---|---|
| "Can I add my own engine?" | "Yes. Copy any engine command file as a template. Swap the logic." |
| "What about a web UI?" | "Not today. The command line is the feature. Less chrome, more throughput." |
| "What about team access?" | "Coming. For now, one Brain per project." |
| "Premium cohort?" | "Success Resources cohort starts June. Waitlist link at the end." |

---

### 01:55 — Close (5 min)

**Say:**
> "Four hours ago you had a Claude account. Now you have a business that can run without you for a week. Thirty minutes of morning briefs this week and you'll never need another productivity tool again."

**Call to action:**
- Share your Brain on LinkedIn (optional). Tag `#PurelyPersonal`.
- 7-day check-in: reply to my DM on Day 7 with your unattended engine's output.
- Waitlist for the Success Resources cohort: [link]

**End exactly at 02:00.** The respect is the brand.

---

## Facilitator Cheat Sheet

### What to have on screen at all times
- Claude Code window (primary)
- The V3 `BUSINESS-BRAIN.rendered.html` in a browser (secondary)
- Universal Engine Pattern diagram (sticky note in corner)

### What NOT to do
- Don't walk through every section of every worksheet. Attendees read.
- Don't do round-robin introductions. Burns time, kills momentum.
- Don't improvise demos. Pre-record a backup in case Claude API stutters.
- Don't apologize for bugs. If something breaks, say "this is why we teach local — you can fix it."

### Pre-flight checklist (30 min before each session)
- [ ] Zoom set to "HD video" + "Share sound"
- [ ] Claude Code open with your Brain loaded
- [ ] Browser open to `BUSINESS-BRAIN.rendered.html`
- [ ] Backup pre-recorded demo video ready (in case of API failure)
- [ ] 5 volunteer handles picked from the attendee list (people who've engaged in DMs)
- [ ] Workshop slack channel pinned
- [ ] Water, coffee, no tea (tea takes too long to sip)

### Time budget cheat sheet
- Welcome: never more than 5 min
- Teach: never more than 10 min consecutive
- Fill: never less than 5 min
- Debrief: always 2 volunteers, never 3+
- Demo: always exactly 10 min, never 15
- Q&A: max 15 min
- Close: 5 min hard stop

### The 3 sentences that run the whole workshop
1. "One pattern, five canvases."
2. "If you can't name one real person, the ICP is too vague."
3. "Run this on your Brain right now."

---

## Post-Workshop (Day 3–10)

### Day 3: DM every attendee
One-line DM: "Day 3 check-in. Which engine are you running this week?"

### Day 7: Public call-out
LinkedIn post: "Workshop 01 graduates: drop your unattended engine's output in the comments."

### Day 10: Case study collection
Email the 3 best outcomes. Ask for permission to turn into case studies for the premium cohort sales page.

---

## Measuring Success

| Metric | Target | Why |
|--------|--------|-----|
| Brain completion rate | ≥ 80% | If <80%, cut worksheet count or extend |
| Engine install rate | ≥ 90% | Install should be frictionless |
| Day-7 unattended engine run | ≥ 50% | This is the retention metric |
| Cohort conversion | ≥ 10% | Free → paid funnel health |
| NPS | ≥ 50 | Live workshop benchmark |

Log these in your Brain after each cohort. The Leadership engine will surface trends.
