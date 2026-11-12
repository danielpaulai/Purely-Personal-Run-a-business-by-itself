---
name: competitor-x-ray
description: Given 3 competitor LinkedIn URLs + the user's ICP, scrape each competitor's profile + last 30 days of posts, then produce a side-by-side positioning analysis showing what they do well, where they have content gaps, what they're missing, and where the user's positioning can win. Outputs a strategic content direction the AI Marketing Employee can immediately use. Use when the user wants competitive intelligence, pre-event positioning prep, content gap analysis, or to understand why they're being out-published by a specific competitor. Triggers on "analyze my competitors", "competitor x-ray", "compare me to [name]", "what is [competitor] doing", "content gap analysis", "competitor positioning", "where can I win", "find content gaps".
version: 1.0.0
author: daniel-paul
tags: [linkedin, competitor-analysis, positioning, content-strategy, ai-marketing-employee, apify, intelligence]
---

# Competitor X-Ray

The skill that gives the AI Marketing Employee strategic intelligence. Scrape 3 competitors → side-by-side analysis → content gaps surfaced → strategic content direction handed back. Pre-event prep or quarterly intel refresh.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "analyze my competitor [URL]" and ChatGPT either (a) refuses because it can't browse, or (b) hallucinates a generic SWOT analysis with no real data. Either way, you can't make positioning decisions from it.

**This skill provides:**
1. **Real scraped data**. uses Apify (`harvestapi/linkedin-profile-posts` for people, `harvestapi/linkedin-company-posts` for company pages, plus `harvestapi/linkedin-profile-scraper` / `harvestapi/linkedin-company` for profile and page details) to pull actual data + recent posts for each competitor
2. **Structured comparison**. 8-dimensional analysis (headline · positioning · post cadence · top topics · hook patterns · CTA patterns · engagement signals · content gaps)
3. **ICP-aware**. uses the user's ICP from Project Knowledge to flag where competitors are winning the user's ideal customer (or missing them)
4. **Strategic output**. not just data, but a 5-bullet "Strategic Content Direction" the user can hand to their AI Marketing Employee

**You can replicate this with ChatGPT if you:** scrape each competitor manually, build a comparison framework, identify content gaps yourself, write up a strategic direction. Takes 3-4 hours per competitor batch. This skill does it in 2 minutes.

---

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| 3 competitor LinkedIn URLs | User input | Ask: "Drop the 3 competitor LinkedIn URLs (one per line)" |
| User's ICP | AI Marketing Employee Project Knowledge | STOP. ask the operator for their ICP (ICP.md or the Business Brain) |
| User's Voice Snapshot (optional) | Project Knowledge | Used for the "Strategic Content Direction" output |
| Apify | The operator's own Apify connector (their account and credit) | STOP. ask them to connect Apify first |

---

## Mode

| Mode | What you get | Best for |
|------|---|---|
| `quick` | Headlines + top 3 topics each + 1 content gap | Fast pre-call prep |
| `standard` (default) | Full 8-dimensional comparison + 3-5 content gaps + Strategic Content Direction | Quarterly intel refresh |
| `deep` | Standard + scrape last 90 days of posts + engagement pattern analysis | Pre-launch competitive positioning |

**Default: `standard`.**

---

## The 8 Dimensions

For each competitor, scrape and analyze:

1. **Headline**. their stated positioning + niche
2. **About section**. their narrative, social proof, CTA
3. **Post cadence**. posts/week + best time of day
4. **Top topics**. 3-5 recurring themes (extracted from last 30 days)
5. **Hook patterns**. how they start posts (frameworks they reuse)
6. **CTA patterns**. what they ask readers to do (DM keywords, comments, links)
7. **Engagement signals**. average likes/comments/saves ratio (proxy for what resonates)
8. **Content gaps vs ICP**. topics ICP wants discussed that this competitor doesn't cover

---

## Process

### Phase 1. Validate inputs
1. 3 URLs provided?
2. ICP in Project Knowledge?

### Phase 2. Scrape (Apify)
For each URL: a `linkedin.com/company/...` URL is a COMPANY PAGE (use `harvestapi/linkedin-company` for the page and `harvestapi/linkedin-company-posts` for its posts); a `linkedin.com/in/...` URL is a PERSON (use `harvestapi/linkedin-profile-scraper` for the profile and `harvestapi/linkedin-profile-posts` for the posts). Last 30 days for `standard`, 90 days for `deep`.

### Phase 3. Per-competitor analysis (8 dimensions)
Run all 8 dimensions on each scraped competitor.

### Phase 4. Cross-competitor synthesis
Identify:
- **Saturation:** topics ALL 3 cover (don't compete here. skip or do contrarian)
- **Coverage:** topics SOME cover (low-priority for user)
- **GAPS:** topics ICP wants discussed that NONE cover (highest-priority for user)

### Phase 5. Strategic Content Direction
Output 5 bullets the user (or their AI Marketing Employee) acts on:
1. Topic to own (the biggest gap)
2. Hook pattern to steal-and-adapt (the strongest hook used by best competitor)
3. CTA to test (the highest-performing CTA used by competitors)
4. Cadence to match (the optimal post frequency from analysis)
5. Format to win (the format competitors UNDER-use that ICP wants)

### Phase 6. Render output
`standard` → markdown comparison table + Strategic Direction

---

## Output Structure (`standard` mode)

```
COMPETITOR X-RAY · 3 PROFILES ANALYZED
Date: [date]
ICP anchor: [from Project Knowledge]

═══════════════════════════════════════
COMPETITOR 1: [Name]
URL: linkedin.com/in/...
- Headline: "..."
- Positioning: [extracted]
- Cadence: X posts/week
- Top 3 topics: 1) ... 2) ... 3) ...
- Hook patterns: "..."
- CTA patterns: "..."
- Avg engagement: ... likes / ... comments
- Gaps vs your ICP: [list]

[... competitor 2, 3 same format ...]

═══════════════════════════════════════
SIDE-BY-SIDE COMPARISON

| Dim | Comp 1 | Comp 2 | Comp 3 | Your opportunity |
| Headline strength | ... | ... | ... | ... |
| Niche specificity | ... | ... | ... | ... |
| ... [8 rows] ... |

═══════════════════════════════════════
CONTENT GAPS (ICP cares · no one covers)
1. [Gap 1]: [why it matters]
2. [Gap 2]: ...
3. [Gap 3]: ...

═══════════════════════════════════════
STRATEGIC CONTENT DIRECTION (your AI Marketing Employee acts on this)
1. OWN: [topic]
2. STEAL-ADAPT HOOK: "[pattern]"
3. TEST CTA: "[pattern]"
4. CADENCE: [N posts/week]
5. FORMAT: [carousel / cheatsheet / story]
```

## Examples

> **Illustrative only.** The names, numbers and results in the examples below are invented to show the format. Never reuse them. In real output use only facts from the operator's Business Brain or from the request, and leave a detail out rather than make one up.

### Example 1: Coach niche · standard mode

**Input:**
- Competitor URLs: 3 well-known coaches in wellness coaching space
- User ICP: "Solo wellness coaches doing $5-30K/month"

**Output excerpt:**
```
Competitor 1: Sarah Williams · 7 posts/week · top topics: mindset, morning routines, content cadence
Competitor 2: Marcus Lee · 4 posts/week · top topics: pricing, client selection, calendar discipline
Competitor 3: Priya Sharma · 6 posts/week · top topics: program structure, retention, AI-in-coaching

SIDE-BY-SIDE:
- All 3 cover mindset and program structure (SATURATED — skip)
- Only 1 covers AI-in-coaching (UNDER-COVERED — opportunity)
- ZERO cover the operational reality of solo coaches juggling 5 roles (GAP — own this)

STRATEGIC DIRECTION:
1. OWN: "The 5-hat solo coach problem" — no competitor addresses this
2. STEAL-ADAPT HOOK: "Most [niche] get this wrong:" (Sarah's highest-performing)
3. TEST CTA: "DM 'engine' for the doc" (Marcus's only DM CTA — works for him)
4. CADENCE: 5 posts/week (median of 3)
5. FORMAT: Cheatsheet comparisons (only Priya uses these · highest save rate)
```

---

## Limitations

- **Public LinkedIn data only.** Won't analyze private profiles or paywalled content.
- **Engagement metrics are approximations.** LinkedIn API doesn't expose exact engagement; this skill uses public proxies.
- **Won't predict competitor moves.** Surfaces patterns, doesn't forecast.

---

## Pro Tips

1. **Run quarterly, not monthly.** Competitor positioning shifts every 60-90 days. Monthly = noise, quarterly = signal.
2. **Pick 3 competitors of different sizes.** One above you, one peer, one below. Different intel from each.
3. **Use Q4 (the gap analysis) as the agenda for your next quarterly planning.** That's the operationalizable output.
4. **Pair with prospect-magnet.** Find prospects who follow your competitors but match YOUR ICP (perfect poaching list).
5. **Don't copy hooks verbatim.** Steal the structure, adapt the voice. Your Voice Snapshot handles the adaptation.

---
## Use in the Purely Personal connector


After the draft: Turn the content gaps into posts with write_post, and find who to talk to with find_prospects.
