---
name: homework-reviewer
description: Bulk-score Day 1 challenge homework posts (or any cohort batch of posts), rank by invisibility-diagnostic score, generate the Day 2 Class Share shortlist with attendee names + industry coverage + read-aloud cues + chat shoutout list. Use when reviewing AI Employee Challenge Day 1 homework, preparing Day 2 opening material, grading cohort batches, or any "score 30+ posts and tell me the best 10" task. Triggers on "review the homework", "rank the posts", "Day 2 class share prep", "grade the cohort", "find the best posts from yesterday", "compile the shortlist".
version: 1.0.0
author: daniel-paul
tags: [homework, review, day-2-prep, scoring, cohort, ai-employee-challenge]
---

# Homework Reviewer

Bulk scoring + Class Share prep for cohort homework batches. Built for Day 1 → Day 2 transition of the AI Employee Challenge, but works for any cohort with 10-300+ post submissions to grade.

This skill is the coordinator's tool. it turns 100 raw submissions into a stage-ready Class Share shortlist in 5 minutes.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Paste 50 posts and ask "which are the best 10?". you get inconsistent picks, no industry coverage check, no read-aloud cues, no consideration of stage flow. The shortlist is unusable on stage because there's no underlying methodology.

**This skill provides:**
1. **Bulk `invisibility-diagnostic` scoring**. every post scored 0-4 consistently using the same dimensions
2. **Industry coverage check**. picks aren't biased toward one industry; explicit coverage report
3. **Read-aloud cues per post**. where to add emphasis, what one thing to point out, the speaker's transition line
4. **Three tiers of recognition**. Top 10 for stage, top 25 for chat shoutouts, full ranked list for coordinator records
5. **Stage flow improvement**. orders the top 10 for narrative momentum (open with high-energy, build, peak)
6. **Coordinator handoff format**. output is timestamped, named, ready for the Day 2 prep doc

---

## Required Inputs

| Input | Source | Format |
|---|---|---|
| Posts to review | Day 1 chat captures, screenshots, post URLs, or pasted text | Any. see "Input Formats" below |
| Cohort context | Optional but improves output | Industry mix, cohort size, Day 2 stage cues |
| Attendee names | Required per post | Each post must be tagged with author name |
| Industries | Required per post (or inferred from Workbook intake) | One word: coach / agency / e-com / b2b / saas / fitness / real-estate / other |

---

## Input Formats Accepted

### Format A. Structured (recommended for >20 posts)

```
[author: Sarah Chen | industry: coach]
Post text here...

[author: Marcus Webb | industry: e-commerce]
Post text here...

[...]
```

### Format B. URL list (LinkedIn / X posts)

```
https://linkedin.com/posts/sarah-chen_xyz · Sarah Chen · coach
https://x.com/marcuswebb/status/xyz · Marcus Webb · e-commerce
[...]
```

If URLs are provided, this skill flags them as "URL provided. fetch text separately and re-run with Format A."

### Format C. Workbook export (cohort JSON dump)

```
[{"name": "Sarah Chen", "industry": "coach", "homeworkPost": "..."}, {...}]
```

Parse and process automatically.

### Format D. Screenshots / OCR'd text

```
[image: sarah_post.png — text: "Post text from OCR..."]
```

Process as Format A using the OCR'd text. Flag for manual verification.

---

## Mode

Detect from context or ask: *"Quick top-10 only, full shortlist with stage cues, or full + chat shoutouts + coordinator JSON?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | Top 10 posts with score + author + 1-line "why it works" | Fast 5-min review when prep time is tight |
| `standard` (default) | Top 10 with read-aloud cues + speaker transition lines + industry coverage report | Day 2 prep, the production case |
| `full` | Standard + top 25 chat shoutouts + full ranked list + flagged thin-scoring posts for coach DM | Cohort with 100+ posts where you want belt-and-braces coverage |

**Default: `standard`**. covers 95% of cases.

| Mode | What you get | Best for |
|---|---|---|
| `visual` ★ | top-tier HTML dashboard: animated KPI cards, score distribution bar chart, industry coverage chart, top-10 post cards, coach-DM triage queue | Hand to Daniel before stage. Display on second screen during Class Share. Screenshot for cohort recap email. |

**Visual mode usage:**
```bash
python ~/.claude/skills/homework-reviewer/scripts/render.py \
  --in cohort-data.json \
  --out /tmp/cohort-dashboard.html && open /tmp/cohort-dashboard.html
```

The HTML dashboard features:
- 4-KPI row (total, avg score, magnetic count, coach-DM count) with staggered reveal
- Animated bar chart of score distribution
- Industry coverage with animated fill bars
- Top 10 post cards with author + score + "why it worked". expand on hover
- Coach DM triage queue with pre-drafted intervention notes
- Brand-locked Purely Personal styling, mobile responsive

See `scripts/template.html` for the full implementation.

---

## Process

### Phase 1. Input Parsing & Validation

1. Detect input format (A/B/C/D from above)
2. For each entry, validate: text present, author present, industry present (or default to "other")
3. If posts > 200 → warn (slow), suggest splitting into batches of 100
4. If posts < 5 → warn (too few for shortlist), suggest waiting for more submissions

Output summary:
> *"Received 73 posts. Industries: 28 coaches, 17 agencies, 12 e-commerce, 9 B2B sales, 4 SaaS, 3 other. Processing time: ~90 seconds."*

### Phase 2. Bulk Scoring

For each post:
1. Run `invisibility-diagnostic` in `score-only` mode (fast, no fix lines needed)
2. Capture: score (0-4), per-dimension scores, brief "what worked" note (1 sentence)

### Phase 3. Ranking

1. Sort by total score (descending)
2. For ties: secondary sort by industry coverage need (under-represented industries bumped up)
3. Tag each post: Stage Top 10 / Chat Shoutout 11-25 / Coordinator Archive

### Phase 4. Industry Coverage Check

For Top 10:
- Calculate distribution
- Compare to overall cohort distribution
- Flag if any industry is missing in Top 10 (e.g., "12% of cohort is B2B SaaS but 0 in Top 10. swap in highest-scoring SaaS post if 3/4 or higher")

### Phase 5. Read-Aloud Cues (standard + full modes)

For each Top 10 post:
1. **Read-aloud cue**. where to add vocal emphasis (1 line)
2. **The ONE thing to point out**. which dimension landed strongest, why (1 line)
3. **Speaker transition line**. what to say BEFORE reading the next post (1 line)

### Phase 6. Stage Flow improvement

Re-order the Top 10 for narrative momentum:
- **Position 1:** highest-energy 4/4 (open hot)
- **Positions 2-5:** mix industries (cover the room)
- **Positions 6-8:** include one "underdog comeback" (someone who scored 1/4 on their last post pre-Challenge but 4/4 on homework)
- **Positions 9-10:** the most memorable 4/4 (close strong)

### Phase 7. Coordinator Handoff (full mode)

Generate:
- Markdown shortlist (for Daniel's eyes)
- JSON cohort archive (for member-area / records)
- Chat shoutout list (for Day 2 chat moderator)
- Flagged "coach DM" list (for attendees scoring 1/4. they need a private check-in)

---

## Output Structure

### `standard` mode output:

```markdown
# Day 2 Class Share — Shortlist
## Generated [date] · [N posts reviewed] · [time taken]

---

## INPUT SUMMARY
- Posts reviewed: 73
- Industry mix: 28 coach · 17 agency · 12 e-com · 9 B2B · 4 SaaS · 3 other
- Score distribution: 12 × 4/4 · 24 × 3/4 · 23 × 2/4 · 14 × 0-1/4
- Average score: 2.4 (up from cohort average pre-Challenge: 1.1)

---

## STAGE TOP 10 (read aloud in this order)

### 1 · Sarah Chen · Coach · 4/4
> [Post text — 150 words]

**Read-aloud cue:** Slow on line 2. Emphasis on "Tuesday".
**The ONE thing:** POV is the strongest — she names the contrarian belief
in line 3 ("Most coaches teach mindset before sales — backwards").
**Speaker transition line (before this post):** "This one's from Sarah —
coach, based in [city]. Listen to her opening line."

### 2 · Marcus Webb · E-commerce · 4/4
> [Post text]

**Read-aloud cue:** [...]
**The ONE thing:** [...]
**Speaker transition line:** [...]

[... 8 more, each in same format ...]

---

## INDUSTRY COVERAGE CHECK

Top 10 distribution:
- Coach: 3 (cohort 38%) ✓
- Agency: 2 (cohort 23%) ✓
- E-commerce: 2 (cohort 16%) ✓
- B2B: 2 (cohort 12%) ✓
- SaaS: 1 (cohort 5%) ✓
- Other: 0 (cohort 4%) — acceptable

No swap needed. Coverage looks healthy.

---

## NEXT STEPS

1. Hand this shortlist to Daniel at 13:30 CET Day 2 (30 min before stage)
2. Pin top 10 names in chat at 14:00 CET so attendees can see themselves coming
3. After reading aloud, drop their @handle in chat for live shoutout
```

### `full` mode output (adds):

```markdown
---

## CHAT SHOUTOUTS (positions 11-25)

| Rank | Name | Industry | Score | Why |
|---|---|---|---|---|
| 11 | Priya Sharma | Agency | 4/4 | Strong voice, slightly weaker hook than top 10 |
| 12 | Achmed Hassan | B2B | 4/4 | Excellent ask line ("DM 'agent'") |
| [...] |

Drop these names + the post link in chat at 14:30 CET Day 2 with "shoutout — read this one too."

---

## COACH DM LIST (positions scoring 0-1/4 — private check-in)

| Name | Industry | Score | Likely cause |
|---|---|---|---|
| [Name] | [industry] | 1/4 | Posted before completing Lesson 2 — no Voice Profile in their Project |
| [Name] | [industry] | 0/4 | Used ChatGPT instead of their AI Marketing Employee — voice didn't load |
| [...] |

These attendees need a private DM before Day 2 opens. Suggested DM template:
> "Saw your homework — let's get you to a 3+ today. The fix is probably
> a 2-min adjustment to your Project. Free 10 min before Day 2 starts?"

---

## FULL RANKED LIST (cohort archive)

[Markdown table: rank | name | industry | score | per-dim scores | post link]

---

## JSON EXPORT

[Embedded JSON of the full archive — drop into the cohort tracker]
```

### `quick` mode output:

```markdown
# Quick Shortlist · [date]

Top 10 (no cues — just names + scores):
1. Sarah Chen · Coach · 4/4
2. Marcus Webb · E-com · 4/4
3. Priya Sharma · Agency · 4/4
4. [...]

Average cohort score: 2.4

Industry coverage in Top 10: OK
```

---

## Examples

### Example 1. Day 1 → Day 2 cohort review (73 posts)

**Input:** Format C (workbook export JSON dump from coordinator)

**Output:** Standard mode markdown (see structure above) with 10 ranked posts, industry coverage check, read-aloud cues. Time: ~90 seconds.

### Example 2. Mid-event quick check (20 posts at lunch)

**Input:** Format A (structured paste from chat moderator)

**Output:** Quick mode. top 5 names + scores. "Use these in the post-lunch celebration block. Industry coverage acceptable."

### Example 3. Full cohort archive (180 posts at end of Day 1)

**Input:** Format C (full workbook export)

**Output:** Full mode. Top 10 stage shortlist + 15 chat shoutouts + 8 coach-DM-needed posts + complete ranked archive + JSON export. Time: ~4 minutes.

### Example 4. Single industry deep-dive

**Input:** Standard format, filtered to coach-industry only (28 posts)

**Output:**
```
# Coach-Industry Spotlight
Top 5 coach posts (for Day 2 Lesson 3 industry callback):

1. Sarah Chen · 4/4 — POV anchor: pricing > mindset
2. Lin Wang · 4/4 — Specificity anchor: "9 of 11 clients"
3. [...]

Average coach-industry score: 2.7 (above cohort average of 2.4 — strong)
```

### Example 5. Cohort with thin-scoring posts (flagged for intervention)

**Input:** 120 posts, where 28 scored 0/4 or 1/4

**Output (full mode coach-DM list):**

```
## COACH DM LIST (28 attendees scored 1/4 or below)

Of 28: 22 used "ChatGPT default" voice (no Project setup). 4 had Voice
Profile installed but skipped Step 2 install. 2 had complete setup but
weak inputs.

Suggested cohort-wide intervention:
- 10:00 Day 2 chat drop: "If you scored under 2/4 last night — that's a
  setup issue, not a writing issue. Reply 'fix' to this message for a
  2-min DM."
- Pre-stage 4 example fixes ready to share.

Individual DMs: 28 templates pre-drafted [appended]
```

---

## Self-Critique Checks (before delivering output)

- [ ] Did I score every post (not skip any)?
- [ ] Are the Top 10 picks evidence-backed (4/4 score) or did I include 3/4 posts?
- [ ] Did I check industry coverage explicitly?
- [ ] If I made a swap for coverage, did I note it?
- [ ] Are read-aloud cues SPECIFIC (line numbers, emphasis points) not generic?
- [ ] Did I flag any 0-1/4 posts for coach DM intervention?
- [ ] Is the time-to-handoff estimate realistic?

If any check fails: regenerate before output.

---

## Chains With Other Skills

| Upstream | How |
|---|---|
| `invisibility-diagnostic` | Called for every post, the scoring engine |
| `first-post-coach` | Posts that scored 4/4 in Game 1 with First-Post Coach are likely top candidates |
| `workbook` (interactive HTML) | Workbook JSON export is Format C input |

| Downstream | How |
|---|---|
| Day 2 opening Class Share | Direct stage use of the shortlist |
| Coach DM flow | Flagged attendees get 1-on-1 intervention |
| Future: `cohort-postmortem` | Day 1-3 score trends become input to a postmortem skill |

**Suggested chain after output:**
> *"Shortlist ready. Hand to Daniel at 13:30 CET Day 2. For the 28 attendees flagged for coach DM, drop the pre-drafted DM templates into your messaging tool now. 1 min each."*

---

## Limitations

- **Won't fetch post text from URLs.** If user provides URLs, this skill flags and asks for pasted text. (Future version: integrate with apify LinkedIn scraper to fetch.)
- **Won't read images.** OCR'd text must be provided. skill doesn't run OCR.
- **Won't judge "tone match" against the cohort.** A post can score 4/4 on the diagnostic and still feel off-brand for the cohort. Human judgment required for tone calls.
- **Won't replace stage instinct.** The shortlist is data-driven. Daniel still has the final read on which 10 actually go on stage. Use as input, not gospel.

---

## Pro Tips

1. **Run between Day 1 ending and Day 2 starting**. that's the window. Earlier = incomplete (people still submitting). Later = too rushed before stage.
2. **Run in `full` mode for cohorts > 100.** The chat shoutout list + coach DM list pays for itself in cohort goodwill.
3. **Use the JSON export as the cohort archive.** Long-term: trends across cohorts (avg score going up = curriculum working).
4. **Always do the industry coverage check.** Cohorts that feel "represented" on stage report higher Day 2 attendance + better Day 3 conversions.
5. **For the coach DM list. pre-draft the 28 DMs.** Don't make the coach write each one. Standard template + 2 personalized lines per DM.

---

## Output Hand-Off (for coordinators)

After this skill produces the shortlist, the coordinator does:

1. **Top 10 markdown** → paste into Day 2 prep doc, share with Daniel via Slack
2. **Chat shoutouts** → schedule in chat tool for 14:30 CET Day 2
3. **Coach DM list** → send DMs at 13:00 CET Day 2 (1 hour before stage)
4. **JSON export** → upload to cohort tracker / member area
5. **Average score trend** → log to cohort metrics dashboard

If this is automated via the workbook + cohort-tracker integration, all 5 happen automatically on shortlist generation.

---

*Built for Day 1 → Day 2 transition of the AI Employee Challenge. Turns 100 submissions into a stage-ready shortlist in 5 minutes.*
