---
name: prospect-magnet
description: Given a user's ICP + a published post, find 10 real LinkedIn prospects who match the ICP and draft 10 personalized DMs in the user's voice that reference the post. Uses Apify LinkedIn search (harvestapi) + profile scraper (supreme_coder) + Voice Profile from Project Knowledge. The "content → pipeline" closer for the AI Marketing Employee. Use when the user wants to convert a post into qualified outreach, build a prospect list from an ICP, or generate personalized DMs at scale. Triggers on "find 10 prospects", "who should I DM about this post", "build my prospect list", "find leads for this", "prospect magnet", "turn this post into outreach", "find my ideal clients on LinkedIn".
version: 1.0.0
author: daniel-paul
tags: [linkedin, prospects, outreach, dms, icp, ai-marketing-employee, apify, sales]
---

# Prospect Magnet

The skill that closes the loop on the AI Marketing Employee. Takes the ICP and the post and produces a **prospect leaderboard**. 10 real LinkedIn profiles matched to ICP + 10 personalized DMs ready to send, in under 30 seconds.

This is the Day 1 "holy shit" demo. The moment attendees realize their AI Employee doesn't just produce content. it produces pipeline.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "find me 10 LinkedIn prospects for my coaching business" and you get either (a) fictional names ChatGPT made up, or (b) a refusal because GPT doesn't browse the web. Either way, you can't act on it. Real outreach requires real profiles with real LinkedIn URLs you can actually click.

**This skill provides:**
1. **Real prospects, not fiction**. calls Apify `harvestapi--linkedin-profile-search` to find actual profiles matching the ICP, then `supreme_coder--linkedin-profile-scraper` to enrich them with full data
2. **ICP-driven targeting**. uses the ICP Document from Project Knowledge to construct precise LinkedIn search queries (industry + role + company size + geography)
3. **Voice-locked personalization**. uses the Voice Snapshot from Project Knowledge so every DM sounds like the user, not like a copywriter
4. **Post-anchored DMs**. every DM references the user's recently published post, creating natural conversation starters with built-in social proof
5. **Match scoring**. each prospect rated 0–10 on ICP fit so the user knows which to DM first
6. **Visual leaderboard**. the output is an HTML artifact with 10 prospect cards (profile photo · LinkedIn URL · match score · ready-to-copy DM · "Send via LinkedIn" deep-link)
7. **Closes the content → pipeline loop**. the entire AI Marketing Employee value prop is proven in this one skill: post → prospects → DMs → conversations → calls → clients

**You can replicate this with ChatGPT if you:** sign up for Apify, build the LinkedIn search query manually, scrape profiles, hand-write 10 personalized DMs each referencing the post + a specific signal from the prospect's profile. Takes 90 minutes per batch. This skill does it in 30 seconds.

---

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| ICP Document | AI Marketing Employee Project Knowledge (output of `voice-profile-builder` + ICP Builder) | STOP. run ICP Builder first |
| Voice Snapshot (or full Voice DNA) | Project Knowledge | STOP. run `voice-profile-builder` first |
| The published post | User input, the post they just shipped (from `linkedin-post-writer` ideally) | Ask: "Paste the post you want to DM-amplify" |
| Apify token | User's environment (`APIFY_TOKEN` env var or `~/.apify/auth.json`) | STOP. guide user to set up Apify token |

---

## Mode

| Mode | What you get | Best for |
|------|---|---|
| `quick` | 5 prospects + 5 DMs · single Apify pass · ~15 sec | Fast batch · daily use |
| `standard` (default) | 10 prospects + 10 DMs · enriched with profile data · match scoring · ~30 sec | Most outreach sessions |
| `deep` | 20 prospects + 20 DMs · multi-signal enrichment (recent posts, mutual connections, company news) · ~90 sec | Pre-campaign prospect mining |
| `visual` ★ | Standard + HTML leaderboard artifact (10 cards · LinkedIn deep-links · copy-ready DMs · match scores visualized) | Demos · screenshots · cohort handoff |

**Default: `standard`**. sweet spot of speed × quality.
**For Day 1 Demo 2: use `visual`**. the leaderboard is the showstopper.

---

## Process

### Phase 1. Validate inputs

1. Check ICP exists in Project Knowledge. If not → STOP, run ICP Builder.
2. Check Voice Snapshot exists. If not → STOP, run `voice-profile-builder`.
3. Confirm post is provided. If not → ask: "Paste the post."
4. Check Apify token. If not → instruct user to set it up.

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

### Phase 3. Call Apify `harvestapi--linkedin-profile-search`

Pass the structured query. Returns 10 profile URLs + basic data (name, headline, current company, photo URL).

### Phase 4. Enrich via `supreme_coder--linkedin-profile-scraper`

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

For each prospect, generate a DM using `scripts/prompts/personalized-dm.md`:
- Opens with a specific reference to ONE thing from their profile (headline phrase, recent post topic, mutual interest)
- Bridges to the user's published post in one line
- Ends with ONE specific ask (DM keyword OR question OR resource offer)
- Stays in the user's voice (vocabulary + rhythm + signature phrases from Voice Snapshot)
- 80–150 characters (LinkedIn DM sweet spot for first message)
- Anti-hallucination: only uses facts pulled from scraped profile data

### Phase 7. Render output

`standard` mode → markdown table with 10 rows (name · score · DM · profile URL)
`visual` mode → HTML leaderboard artifact (see Section "Output Structure · Visual Mode")

### Phase 8. Suggest next steps

> *"10 prospects ready. Suggested next moves:*
> *1. Open the LinkedIn deep-links in 10 tabs (visual mode includes them)*
> *2. Send the top 5 DMs today (match score 8+)*
> *3. Tomorrow morning check replies → run `linkedin-post-writer` on responders to escalate*
> *4. For Day 2 of the AI Employee Challenge, this skill becomes a deployed Research Assistant running on a daily Apify schedule, finding fresh prospects every morning while you sleep."*

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
- Day 2 AI Employee Challenge → Deploy this as a Research Assistant on a daily Apify schedule (background worker)
```

## Output Structure (`visual` mode)

Brand-locked HTML artifact (`scripts/template.html`). Features:
- Hero: "PROSPECT MAGNET · 10 LEADS" + ICP summary + post excerpt
- KPI row: total found · average match · top score · estimated calls if 10% reply
- 10 prospect cards (2-column grid on desktop):
  - Avatar (initials in red gradient)
  - Name + verified checkmark
  - Headline + current company
  - Match score badge (color: green 8-10, blue 5-7, amber <5)
  - 1-line "why they match" (extracted from profile data)
  - Full DM in a code block with "Copy DM" button
  - "Open Profile in LinkedIn ↗" button (deep-link)
- Footer: "Built it once. Keep it forever." + Purely Personal brand stripe
- Animations: cards stagger-fade-in, match scores count up, confetti on 10/10 cards

See `scripts/render.py` + `scripts/template.html` for the implementation.

---

## Bundled Files

```
~/.claude/skills/prospect-magnet/
├── SKILL.md                          (this file)
└── scripts/
    ├── render.py                     (JSON → HTML leaderboard)
    ├── template.html                 (visual leaderboard template)
    └── prompts/
        ├── prospect-search.md        (ICP → LinkedIn search query)
        └── personalized-dm.md        (prospect + post + voice → DM)
```

---

## Examples

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

### Example 3. Visual mode for Day 1 Demo 2

**Input:** Same as Example 2

**Output:** Full HTML leaderboard artifact opens in browser. 10 cards visible. Daniel walks through cards 1-3 live on screen, shows match scores, reads DM #1 aloud, clicks "Open Profile" to confirm real LinkedIn URL. **Stunned silence in chat. Then it explodes.**

---

## Chains With Other Skills

| Upstream | How |
|---|---|
| `voice-profile-builder` (or Voice Snapshot) | Required. provides the voice for DMs |
| `ai-marketing-employee` | Required. provides Project context |
| ICP Builder (HTML fillable) | Required. provides the ICP for prospect targeting |
| `linkedin-post-writer` | Optional. provides the post to anchor DMs to |

| Downstream | How |
|---|---|
| `cold-outreach-sequence` | Takes the 10 prospects + DMs → builds 5-touch follow-up sequence |
| Day 2 Deploy on Schedule | Run prospect-magnet as a daily background worker via Apify scheduled tasks · fresh 10 prospects every morning |
| `invisibility-diagnostic` | Can score each DM individually for voice/POV/specificity/asking |

**Suggested chain after output:**
> *"10 prospects ready. Next: send the top 5 today. Run `cold-outreach-sequence` to build the 5-touch follow-up. Tomorrow on Day 2 we deploy this skill on an Apify schedule so it finds 10 fresh prospects every morning while you sleep."*

---

## Apify Setup (first-time only)

This skill requires the user to have an Apify account + API token.

### One-time setup:

1. Sign up at https://apify.com (free tier includes $5/month credits. enough for ~50 prospect-magnet runs)
2. Get your API token from https://console.apify.com/account/integrations
3. Set the env var: `export APIFY_TOKEN="your_token_here"` (add to ~/.zshrc or ~/.bashrc)
4. Test: `python ~/.claude/skills/prospect-magnet/scripts/find-prospects.py --test`

### Apify Actors used:

| Actor | Purpose | Cost per run (~) |
|---|---|---|
| [`harvestapi/linkedin-profile-search`](https://apify.com/harvestapi/linkedin-profile-search) | LinkedIn profile search by keyword + filters | $0.50 per 10 profiles |
| [`supreme_coder/linkedin-profile-scraper`](https://apify.com/supreme_coder/linkedin-profile-scraper) | Enrich profile URLs with full data | $0.10 per profile |

**Total cost per `standard` run: ~$1.50** (10 prospects). That's $0.15 per personalized DM.

For comparison: a freelance VA hand-researching 10 prospects + writing 10 personalized DMs = $50–150 and 3-5 hours.

---

## Self-Critique Checks (before delivering output)

- [ ] Are all 10 prospects REAL (have valid LinkedIn URLs)?
- [ ] Did I use the actual ICP from Project Knowledge (not made-up criteria)?
- [ ] Did each DM reference a SPECIFIC signal from the prospect's profile (not generic)?
- [ ] Does each DM match the user's voice (vocabulary from Voice Snapshot)?
- [ ] Is each DM 80–150 chars (LinkedIn first-message sweet spot)?
- [ ] Did I include ONE specific ask per DM (not multiple, not vague)?
- [ ] Are match scores computed honestly (no inflation to all 10/10)?
- [ ] If visual mode: did the HTML artifact render with all 10 cards?

If any check fails: regenerate that prospect/DM before output.

---

## Limitations

- **Won't scrape without Apify token.** This is a paid API. Free tier covers ~50 runs/month.
- **Won't generate prospects from nothing.** Requires a populated ICP doc in Project Knowledge.
- **Won't replace human judgment on send.** The skill produces DMs ready to copy, the user still clicks send. Intentional: prevents spam at scale.
- **LinkedIn search filters are imperfect.** Some prospects may not be 100% ICP match, that's why we compute match score so the user prioritizes.
- **DMs are first-touch only.** For 5-touch sequences, chain to `cold-outreach-sequence`. For daily automated discovery, deploy on a schedule (Day 2 lesson).

---

## Pro Tips

1. **Run after every published post.** Post in the morning → run prospect-magnet at noon → DM top 5 by 3 PM → first replies by 6 PM. That's a content-to-conversation loop you can run every day.
2. **Refresh your ICP quarterly.** Voice + ICP both drift. Re-run ICP Builder every 90 days for sharper targeting.
3. **Use `quick` mode for daily ops.** `standard` for weekly batches. `deep` for new market pushes.
4. **Track which DMs convert.** Day 3 of the Challenge teaches the Conversion Engine. feed reply data back to sharpen the next DM batch.
5. **For Day 1 Demo 2:** rehearse the visual output once before the live demo. The wow moment depends on the cards rendering smoothly. Pre-stage a backup video.

---

## GitHub References (this skill builds on)

- [**OpenOutreach** (eracle)](https://github.com/eracle/OpenOutreach). open-source pattern for "Describe your product. Define your target market. The AI finds the leads for you." Same concept, this skill is Claude-native and Apify-powered.
- [**awesome-ai-agents-2026** (caramaschiHG)](https://github.com/caramaschiHG/awesome-ai-agents-2026). 25K stars · #1 GitHub Trending Feb 2026 · LinkedIn outreach category has 12+ proven patterns this skill draws from.
- Apify Actor Store: [harvestapi/linkedin-profile-search](https://apify.com/harvestapi/linkedin-profile-search) + [supreme_coder/linkedin-profile-scraper](https://apify.com/supreme_coder/linkedin-profile-scraper). the real data layer powering this skill.

---

*Built for Day 1 Demo 2 of the Build Your 1st AI Employee Challenge. The skill that proves the AI Employee produces pipeline, not just content. Sets up Day 2 (Deploy on Schedule) perfectly.*
