# Automation Hierarchy · Eliminate · Automate · Delegate

> The wrong question is "what should I automate?" The right question
> is "what should I ELIMINATE first · then automate · then delegate?"
> 80% of operators automate work that should have been deleted.

---

## The 3 levels (in order)

```
Level 1 · ELIMINATE  ·  the work shouldn't exist
Level 2 · AUTOMATE   ·  the work exists but a system can do it
Level 3 · DELEGATE   ·  the work exists, can't be automated, but
                        someone else can do it
```

The order is non-negotiable. Most operators flip 1 and 2 (or skip
1 entirely). The result: they automate work that should have been
killed.

---

## Level 1 · ELIMINATE (always check this FIRST)

Before automating anything, ask:

> **"Why does this work exist at all?"**

Most repeated tasks exist because of:
- A historical decision that no longer applies
- Customer over-promising you didn't have to make
- A bad process you inherited
- Habit
- Anxiety ("but what if we don't?")

If you can KILL the work, you save 100% of the time. Automation
saves ~80%. Delegation saves ~60%. Elimination is the highest
leverage move.

### Elimination test (ask all 4)

```
1 · Does this work serve a customer outcome?
2 · Would my best customers care if this stopped?
3 · Has anyone ever specifically asked for this?
4 · If I disappeared for 6 weeks, would the absence of this
    work hurt revenue?
```

If "no" to 3 of 4 · KILL it. Don't automate. Don't delegate. End it.

### Examples to kill

- Monthly customer "newsletter" no one opens (kill or repurpose)
- Daily standups you keep "for visibility" (kill if they're status
  reports)
- Quarterly reports that no one reads (kill the report · keep the
  data)
- Manual tracking spreadsheets that duplicate Stripe data (kill)
- Emails to internal team that should be Slack (consolidate)
- Legacy meetings (always check: is this still serving its
  purpose?)

---

## Level 2 · AUTOMATE (after elimination · before delegation)

If the work survives elimination · ask:

> **"Can a system do this without a human?"**

Modern automation tools cover ~70% of repeated knowledge work:

- **AI engines** (Claude · GPT · Gemini) for content, research,
  drafting, summarization
- **Zapier / Make / n8n** for tool-to-tool data flow
- **Airtable / Notion automations** for database-driven workflows
- **Sheets / Apify** for data aggregation
- **Apify / Browse / Playwright** for web scraping
- **Stripe webhooks → CRM** for revenue tracking
- **Calendar tools** for scheduling
- **MCP servers** (your Workshop MCP) for AI-callable tools

### Automation test (ask all 3)

```
1 · Does this task have STABLE inputs and STABLE outputs?
2 · Are the steps repeatable (not heavily improvisation)?
3 · Is the cost of automation < the value of time saved?
```

If yes to all 3 · automate.

### What to automate first

Start with HIGH-FREQUENCY tasks. If you do something 50 times a
week, automation pays back in days. If you do it 5 times a week,
weeks. If you do it 1 time a week, months.

**For Purely Personal:**
- /marketing-engine · automated content drafting (was 4 hrs/week)
- /sales-engine · automated lead research (was 6 hrs/week)
- /operations-engine · automated inbox triage (was 7 hrs/week)
- /cash-engine · automated revenue tracking (was 2 hrs/week)
- /leadership-engine · automated daily brief (was 1 hr/week)

That's 20 hrs/week of human time replaced. The $49 workshop pays
back in 4 hours.

---

## Level 3 · DELEGATE (only after eliminate + automate fail)

If the work survived elimination AND can't be automated · ask:

> **"Could someone ELSE do this · with proper SOPs?"**

Delegation is the third-best option · because human delegation has
overhead:

- Hiring / onboarding cost
- SOP creation
- QC and management time
- Communication overhead
- Cost per output

**Delegation test (ask all 3)**

```
1 · Is this task above someone else's pay grade or below mine?
2 · Will the SOP I write let them deliver 80% of my quality?
3 · Is my time saved > the cost of the help (including management)?
```

If yes to all 3 · delegate.

### Who to delegate to (in order of leverage)

1. **AI engines** (already covered · automation)
2. **VAs / contractors** for low-context repetitive work
3. **Specialists** for high-context expert work (designer,
   developer, accountant)
4. **Full-time hires** for embedded ongoing work (only after
   1-3 are exhausted)

The default for most solopreneurs: AI + 1 VA covers 90% of work
that survives elimination. You don't need a team of 10. You need a
well-designed system + 1-2 humans.

---

## The hierarchy in action · weekly inbox example

**Week 0 (before the system):**
- 200 emails/week
- 4 hours/week processing

**Apply Level 1 · ELIMINATE:**
- Unsubscribe from 30 newsletters → kills 60 emails
- Archive auto-notifications without reading → kills 40 emails
- Set up filters for known junk → kills 30 emails
- Result: 70 real emails/week (130 killed)

**Apply Level 2 · AUTOMATE:**
- /operations-engine triages remaining 70 emails
- Drafts replies for ~50 (the routine ones)
- Surfaces 20 that need YOUR attention
- Result: 20 emails/week need you (50 drafted)

**Apply Level 3 · DELEGATE:**
- VA reviews + sends Engine drafts after spot-check (15 min/day)
- VA handles inbox-only Slack comms
- Result: VA owns 50 drafts. You own 20.

**Final state:** 20 emails/week × 1 minute each = 20 min/week.

From 4 hrs/week to 20 min/week. 92% reduction. Achieved by stacking
all three levels.

---

## The hidden cost of automation-first thinking

Most operators jump straight to Level 2. They automate without
eliminating. The result:

- The bad process now runs faster · BAD
- Edge cases (which were ignorable manually) become catastrophic
  failures
- Maintenance overhead grows (every automation is a system to
  maintain)
- The "we automated it!" feels productive · masks that the work
  shouldn't have existed

**The discipline:** before any new automation, force yourself to
spend 5 minutes asking "could I just stop doing this?"

---

## When delegation BEATS automation

Some work resists automation:

- Judgment-heavy work (a real human ROI assessment)
- Relationship work (client check-ins where presence matters)
- Creative work that needs novel angles
- High-context strategic work
- Customer escalations (humans expect humans)

For these · delegate to a human (specialist or VA) rather than
forcing automation that produces robotic output.

---

## The annual elimination audit

Every January · audit EVERYTHING you do:

```
[ ] Make a list of every recurring task you do
[ ] Score each: HIGH / MED / LOW value to a customer outcome
[ ] Cross out everything LOW value (eliminate · 30%)
[ ] Score remaining: AUTOMATABLE / NOT
[ ] Build / fix automations for the AUTOMATABLE ones (50% of remaining)
[ ] DELEGATE remaining 20% to humans (AI + VA)
```

Most operators emerge from the audit with 50% less work · same
revenue · 2x energy.

---

## Apply it to /operations-engine

When the engine generates the Friday Wrap (or weekly review):

1. **Tally hours** spent on each work category this week
2. **Flag tasks done 5+ times** that have no SOP (automation
   candidates)
3. **Flag tasks that produced no value** (elimination candidates)
4. **Suggest specific automation opportunities** (with the engine
   that could handle it)
5. **Suggest specific delegation opportunities** (with the SOP that
   would need to be written)

When the engine onboards a new user (during /build-my-brain):

1. Ask: "What 3 tasks consume the most time per week?"
2. Audit each: eliminate / automate / delegate
3. For automate · pre-build the engine routine
4. For delegate · output the SOP
5. For eliminate · note in BRAIN to STOP doing

This is how 80-hour weeks become 30-hour weeks within 60 days.

---

## The 1-question filter

When you encounter ANY new task that's about to land in your
calendar · ask:

> "Is this work I should ELIMINATE, AUTOMATE, or DELEGATE?"

(Not: "how do I do this faster?")

If your default answer is "I'll just do it · it's quick" · you're
the bottleneck. Force the question. Force one of the 3 answers. The
business that runs without you is the one where YOU stop being the
default answer.
