---
description: Interactive 4-act intake that builds BUSINESS-BRAIN.md from scratch. Scrapes LinkedIn, website, competitors, and Reddit via Apify to auto-fill 80% of sections.
argument-hint: [optional: linkedin-url]
---

# /build-my-brain

You are running the 4-act Business Brain intake. Your job is to produce a filled `BUSINESS-BRAIN.md` at the project root in under 40 minutes. Most of that time is automation — the user only answers 5 strategic questions.

Load `purely-personal/examples/BUSINESS-BRAIN.sample.md` as the structural reference for the output file.

---

## Opening (30 seconds)

Say this, verbatim:

> "We're going to build your Business Brain. This is the one file every AI executive reads before acting. Four acts, four wow moments. Ready?"

Wait for "yes" or equivalent.

---

## Act 1 — Voice (5 minutes)

Say:

> "Act 1. Paste your LinkedIn profile URL."

Once they paste:

1. Use `apify-linkedin` (if installed) OR `apify--linkedin-profile-scraper` to pull:
   - Profile headline, about, experience, headshot URL
   - Last 30 posts (content + engagement)

2. Run `voice-extractor` skill on the scraped posts. Extract:
   - 3–5 banned phrases (observed absences — phrases that DON'T appear)
   - 5 hook patterns (first-line openings repeated across posts)
   - 3 example post excerpts (first 2–3 sentences)
   - Tone description (1–2 sentences)

3. Run `linkedin-profile-optimizer` to generate a profile score (out of 100).

4. Display results to user:

```
✓ Pulled profile + 30 posts
✓ Voice rules extracted: [N banned phrases, N hook patterns]
✓ Profile score: {score}/100
```

5. Ask: "Anything to add or remove before I save?"

6. On confirmation, write Voice section to `BUSINESS-BRAIN.md`.

**Wow moment:** "Wait, that's exactly how I write."

---

## Act 2 — Business (5 minutes)

Say:

> "Act 2. Paste your website URL."

Once they paste:

1. Use `apify--website-content-crawler` to pull the homepage + pricing page (if found).

2. Extract:
   - Offer statement (one line)
   - Positioning (one sentence)
   - Pricing (price points)
   - Key claims / social proof

3. Run `brand-identity-extractor` on the same URL. Extract:
   - 4–8 colors (dominant, excluding pure `#ffffff` and `#000000`)
   - Display font + body font (from CSS inspection)
   - Visual voice description (1 sentence, auto-generated from observed patterns)

4. Ask user 2 questions:
   - "What's your 90-day goal? One sentence."
   - "What's the one metric that matters? Give me a number + label (e.g. '$75K monthly recurring')."

5. Display preview of extracted sections. Ask: "Good, or rewrite?"

6. On confirmation, write Business + Brand Identity sections to `BUSINESS-BRAIN.md`.

**Wow moment:** "It extracted my colors and fonts automatically."

---

## Act 3 — Competitors + ICP (10 minutes)

Say:

> "Act 3. Paste three competitor URLs. One per line."

Once they paste 3 URLs:

1. For each: `apify--website-content-crawler` → extract homepage hero + pricing
2. For any LinkedIn URLs among them: also run `apify-linkedin`

3. For each competitor, derive:
   - Name (from site title)
   - Their angle (positioning in 1 sentence)
   - Gap to own (1 sentence — what they don't say that you can)

4. Display the 3x3 matrix preview. Ask: "Gaps feel right? Edit any that don't."

5. Then ICP. Ask the user:
   - "Describe your ideal client. Role + context in one line."

6. Using the user's input + the competitor data + `positioning-basics` skill, generate:
   - 3 pain bullets
   - 3 desire bullets
   - 3 objection bullets
   - Where they hang out (1 line)

7. Display ICP card preview. Ask: "Anything to adjust?"

8. On confirmation, write Competitors + ICP sections to `BUSINESS-BRAIN.md`.

**Wow moment:** "This is the competitor research I've been paying an agency for."

---

## Act 4 — Audience Pain + AI Visibility (10 minutes)

Say:

> "Act 4. Final step. Give me one keyword that describes what you sell."

Once they give a keyword:

1. Run `reddit-insights` or `apify__trudax--reddit-scraper-lite` with the keyword. Pull top 50 recent posts/comments.

2. Cluster into 4–6 pain themes. For each:
   - Theme name (2–4 words)
   - Best verbatim (1–2 sentences, quoted exactly)
   - Source (subreddit + month)

3. In parallel: run `ai-discoverability-audit` on the user's name + business. Generate:
   - Score 0–100
   - 5–7 gap queries (searches where they don't appear)

4. Display both: pain themes and AI visibility score. Ask: "Anything to cut?"

5. On confirmation, write AI Visibility + Audience Pain sections to `BUSINESS-BRAIN.md`.

**Wow moment:** "These are my prospects' actual words, live."

---

## Closing (2 minutes)

Once all 8 content sections are written:

1. Append the Actions section (hardcoded — always the same 5 engine commands).

2. Save `BUSINESS-BRAIN.md` at project root.

3. Say:

> "Done. Your Brain is at `./BUSINESS-BRAIN.md`. Every engine reads from this. Run `/render-brain` to see it as a one-pager."

4. Optionally run `/render-brain` immediately and open the HTML artifact.

---

## Error Handling

| Problem | What to do |
|---------|------------|
| Apify API rate-limited | Fall back to manual: "Paste your top 3 posts here" |
| User has no LinkedIn | Ask for 3 examples of their writing (emails, docs, anything) |
| User has no website | Ask the questions directly (offer, positioning, pricing) |
| User has no competitors they know | Use Google search via WebFetch for "[their niche] + alternatives" |
| Reddit has no matches for keyword | Try broader keyword or Twitter/X search via Apify |
| `ai-discoverability-audit` not available | Render section with manual-check CTA |

---

## Output Contract

After running, you must have:

- [ ] `./BUSINESS-BRAIN.md` exists at project root
- [ ] All 9 sections present (Operator, Voice, Business, ICP, Competitors, Brand, AI Visibility, Pain, Actions)
- [ ] No `{{placeholder}}` text in the file
- [ ] User has confirmed each section before it was written
- [ ] File ends with the canonical Actions section (5 slash commands)

If ANY section is empty or skipped, flag it and suggest the skill to fill it later.

---

## Anti-patterns

- ❌ Never write to `BUSINESS-BRAIN.md` without user confirmation on that section.
- ❌ Never fabricate data when a scrape fails. Fall back to asking the user.
- ❌ Never skip the "wow moment" narration. That's the workshop payoff — the user needs to feel it happen.
- ❌ Never run all 4 acts in silence. Narrate each act's start and each section's completion.
- ❌ Never end without offering to render. The Brain is more valuable visible.
