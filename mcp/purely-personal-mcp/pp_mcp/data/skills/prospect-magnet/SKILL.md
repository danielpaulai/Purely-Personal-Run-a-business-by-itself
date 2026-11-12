---
name: prospect-magnet
description: Given a user's ICP + a published post, find 10 real LinkedIn prospects who match the ICP and draft 10 personalized DMs in the user's voice that reference the post. Uses Apify LinkedIn search (harvestapi) + profile scraper (harvestapi) + Voice Profile from Project Knowledge. The "content → pipeline" closer for the AI Marketing Employee. Use when the user wants to convert a post into qualified outreach, build a prospect list from an ICP, or generate personalized DMs at scale. Triggers on "find 10 prospects", "who should I DM about this post", "build my prospect list", "find leads for this", "prospect magnet", "turn this post into outreach", "find my ideal clients on LinkedIn".
version: 1.0.0
author: daniel-paul
tags: [linkedin, prospects, outreach, dms, icp, ai-marketing-employee, apify, sales]
---

# Prospect Magnet

The skill that closes the loop on the AI Marketing Employee. Takes the ICP and the post and produces a **prospect leaderboard**. 10 real LinkedIn profiles matched to ICP + 10 personalized DMs ready to send, in under 30 seconds.


---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "find me 10 LinkedIn prospects for my coaching business" and you get either (a) fictional names ChatGPT made up, or (b) a refusal because GPT doesn't browse the web. Either way, you can't act on it. Real outreach requires real profiles with real LinkedIn URLs you can actually click.

**This skill provides:**
1. **Real prospects, not fiction**. calls Apify `harvestapi/linkedin-profile-search` to find actual profiles matching the ICP, then `harvestapi/linkedin-profile-scraper` to enrich them with full data
2. **ICP-driven targeting**. uses the ICP Document from Project Knowledge to construct precise LinkedIn search queries (industry + role + company size + geography)
3. **Voice-locked personalization**. uses the Voice Snapshot from Project Knowledge so every DM sounds like the user, not like a copywriter
4. **Post-anchored DMs**. every DM references the user's recently published post, creating natural conversation starters with built-in social proof
5. **Match scoring**. each prospect rated 0–10 on ICP fit so the user knows which to DM first
7. **Closes the content → pipeline loop**. the entire AI Marketing Employee value prop is proven in this one skill: post → prospects → DMs → conversations → calls → clients

**You can replicate this with ChatGPT if you:** sign up for Apify, build the LinkedIn search query manually, scrape profiles, hand-write 10 personalized DMs each referencing the post + a specific signal from the prospect's profile. Takes 90 minutes per batch. This skill does it in 30 seconds.

---

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| ICP Document | AI Marketing Employee Project Knowledge (the operator's ICP.md or the Business Brain) | STOP. ask the operator for their ICP (ICP.md or the Business Brain) |
| Voice Snapshot (or full Voice DNA) | Project Knowledge | STOP. run `voice-profile-builder` first |
| The published post | User input, the post they just shipped (from `linkedin-post-writer` ideally) | Ask: "Paste the post you want to DM-amplify" |
| Apify | The operator's own Apify connector (their account and credit) | STOP. ask them to connect Apify first |

---

## Mode

| Mode | What you get | Best for |
|------|---|---|
| `quick` | 5 prospects + 5 DMs · single Apify pass · ~15 sec | Fast batch · daily use |
| `standard` (default) | 10 prospects + 10 DMs · enriched with profile data · match scoring · ~30 sec | Most outreach sessions |
| `deep` | 20 prospects + 20 DMs · multi-signal enrichment (recent posts, mutual connections, company news) · ~90 sec | Pre-campaign prospect mining |

**Default: `standard`**. sweet spot of speed × quality.

---

## Process

### Phase 1. Validate inputs

1. Check ICP exists in Project Knowledge. If not → STOP, ask for the operator's ICP (ICP.md or the Business Brain).
2. Check Voice Snapshot exists. If not → STOP, run `voice-profile-builder`.
3. Confirm post is provided. If not → ask: "Paste the post."

### Phase 2. Construct LinkedIn search query from ICP

Pull from the ICP doc:
- **Target ICP Insights · Q1** (urgent problem) → translates to industry + role keywords
- **Core Service & Outcome · Q3** (who benefits most) → narrows to seniority + company size
- **Company Snapshot · Q3** (regions served) → geography filter

Output a structured search query:
```json
{
  "keywords": "coach AND ('content marketing' OR 'personal brand')",
  "industries": ["coaching", "consulting", "wellness"],
  "seniority": ["owner", "founder"],
  "company_size": ["1-10", "11-50"],
  "geography": ["United States", "United Kingdom", "Canada", "Australia"],
  "limit": 10
}
```

### Phase 3. Call Apify `harvestapi/linkedin-profile-search`

Pass the structured query. Returns 10 profile URLs + basic data (name, headline, current company, photo URL).

### Phase 4. Enrich via `harvestapi/linkedin-profile-scraper`

For each of the 10 URLs, pull full profile data:
- Headline · summary · current role · company
- Recent posts (last 30 days)
- Education · location · mutual connections
- Activity signals (recent likes/comments on AI-related content)

### Phase 5. Compute ICP match score (0–10)

For each prospect, score:
- Industry match (3 pts max)
- Role/seniority match (2 pts max)
- Geography match (1 pt max)
- Activity match (recent engagement with AI/marketing/your topic: 2 pts max)
- Buying signal (job change, funding, hiring, course creation: 2 pts max)

Sort prospects by score descending.

### Phase 6. Draft 10 personalized DMs

For each prospect, generate a DM using `prompts/personalized-dm.md`:
- Opens with a specific reference to ONE thing from their profile (headline phrase, recent post topic, mutual interest)
- Bridges to the user's published post in one line
- Ends with ONE specific ask (DM keyword OR question OR resource offer)
- Stays in the user's voice (vocabulary + rhythm + signature phrases from Voice Snapshot)
- 80–150 characters (LinkedIn DM sweet spot for first message)
- Anti-hallucination: only uses facts pulled from scraped profile data

### Phase 7. Render output

`standard` mode → markdown table with 10 rows (name · score · DM · profile URL)

### Phase 8. Suggest next steps

> *"10 prospects ready. Suggested next moves:*
> *1. Open the LinkedIn deep-links in 10 tabs (visual mode includes them)*
> *2. Send the top 5 DMs today (match score 8+)*
> *3. Tomorrow morning check replies → run `linkedin-post-writer` on responders to escalate*

---

## Output Structure (`standard` mode)

```
PROSPECT MAGNET · 10 LEADS

ICP: [extracted summary from Project Knowledge]
Post anchor: "[first 50 chars of the user's post]..."
Search query: [the query used]
Total found: 10/10
Average match score: 8.4/10

═══════════════════════════════════════
| # | Name           | Match | DM Preview                            | Profile URL |
| 1 | Sarah Chen     | 10/10 | "Sarah — saw your post about ..."     | linkedin.com/in/sarah-chen |
| 2 | Marcus Webb    | 9/10  | "Marcus — your point about ..."       | linkedin.com/in/marcus-webb |
[... 8 more]

═══════════════════════════════════════
NEXT MOVES:
- Top 5 (score ≥9) → send today
- Profiles 6-10 → send tomorrow
- Run `linkedin-post-writer` on replies
```

## Examples

> **Illustrative only.** The names, numbers and results in the examples below are invented to show the format. Never reuse them. In real output use only facts from the operator's Business Brain or from the request, and leave a detail out rather than make one up.

### Example 1. Quick mode · coach industry

**Input:**
- ICP: "Solo wellness coaches doing $5-30K/month who've tried 2+ content agencies"
- Post: "I told a wellness coach last week to stop posting daily..."

**Output (quick mode):**

```
PROSPECT MAGNET · 5 LEADS (quick mode)
Average match: 8.2/10 · Found in 14 sec

1. Sarah Chen · 9/10 · "Solo wellness coach · $15K/month · Tampere"
   DM: "Sarah — saw your post about firing your content agency last month. The pattern you described matches what I just wrote about. Mind if I send you the worksheet I gave a client this week?"

2. Marcus Webb · 9/10 · "Wellness coach · Berlin"
   DM: "Marcus — your post about pricing pivots last week stopped my scroll. Worked on a similar reframe with a client this week. DM me 'voice' if you want the 3-step playbook."

3-5. [3 more]
```

### Example 2. Standard mode · B2B SaaS

**Input:**
- ICP: "Founders of B2B SaaS companies, $1-10M ARR, struggling with content velocity"
- Post: "We replaced our content team with one AI workflow. Output 3×, cost down 80%."

**Output:** 10 SaaS founder profiles · sorted by ICP match score · personalized DMs that each reference a specific signal from the prospect's profile (recent funding, job change, recent post topic).

## Self-Critique Checks (before delivering output)

- [ ] Are all 10 prospects REAL (have valid LinkedIn URLs)?
- [ ] Did I use the actual ICP from Project Knowledge (not made-up criteria)?
- [ ] Did each DM reference a SPECIFIC signal from the prospect's profile (not generic)?
- [ ] Does each DM match the user's voice (vocabulary from Voice Snapshot)?
- [ ] Is each DM 80–150 chars (LinkedIn first-message sweet spot)?
- [ ] Did I include ONE specific ask per DM (not multiple, not vague)?
- [ ] Are match scores computed honestly (no inflation to all 10/10)?

If any check fails: regenerate that prospect/DM before output.

---

## Limitations

- **Won't generate prospects from nothing.** Requires a populated ICP doc in Project Knowledge.
- **Won't replace human judgment on send.** The skill produces DMs ready to copy, the user still clicks send. Intentional: prevents spam at scale.
- **LinkedIn search filters are imperfect.** Some prospects may not be 100% ICP match, that's why we compute match score so the user prioritizes.

---

## Pro Tips

1. **Run after every published post.** Post in the morning → run prospect-magnet at noon → DM top 5 by 3 PM → first replies by 6 PM. That's a content-to-conversation loop you can run every day.
2. **Refresh your ICP quarterly.** Voice + ICP both drift. Refresh your ICP every 90 days for sharper targeting.
3. **Use `quick` mode for daily ops.** `standard` for weekly batches. `deep` for new market pushes.
4. **Track which DMs convert.** Day 3 of the Challenge teaches the Conversion Engine. feed reply data back to sharpen the next DM batch.

---
## Use in the Purely Personal connector


After the draft: Start from a published post. Clean every message with de_ai_ify.
