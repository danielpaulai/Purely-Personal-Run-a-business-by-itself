---
name: outreach-prospector
description: Use this skill whenever the user wants to research leads, build a prospect list, qualify potential clients, or prepare for LinkedIn outreach. Triggers include "find me leads", "research this prospect", "build a lead list", "profile this person for outreach", "who should I be DMing", or any mention of ICP (Ideal Client Profile), LinkedIn prospecting, or target audience research. Always use this skill before writing any outreach message.
---

# ◈ THE PROSPECTOR

> Your job is not to find contacts. Your job is to make the wrong approach impossible.

Before a single word is written, this skill produces a complete intelligence brief on the human behind the profile, so the outreach that follows feels less like a DM and more like a conversation that was always going to happen.

---

## ━━ BEFORE YOU BEGIN ━━

If the user hasn't provided all of the following, ask before proceeding:

**About the prospect:**
- Their name, LinkedIn URL, or a profile description
- Their role, company, and niche
- Any recent posts, comments, or content they've shared

**About the sender:**
- What do you offer? What specific problem do you solve?
- Who is your ideal client? (role, industry, company size, pain point)
- What disqualifies a lead for you?

> Do not proceed with partial information. A half-built profile produces half-built outreach.

---

## ━━ THE INTELLIGENCE BRIEF ━━

Run all five modules in sequence. Never skip one.

---

### MODULE 1, STRATEGIC FIT SCORE

**What this is:** A cold-eyed assessment of whether this person deserves your time. Scored 1–10 against four dimensions, not just gut feel.

Score across:
| Dimension | What to assess |
|---|---|
| **Role alignment** | Does their title, seniority, and function match the ICP? |
| **Pain alignment** | Do their posts, content, or profile signals suggest the problem you solve exists for them? |
| **Timing signals** | Are there indicators this is an active need, hiring posts, growth signals, complaints, transitions? |
| **Relationship potential** | Is there enough common ground to build a genuine peer-to-peer exchange? |

Average the four and round to one decimal.

**Output format:**
```
┌─────────────────────────────────────────────┐
│  STRATEGIC FIT SCORE                        │
├─────────────────────────────────────────────┤
│  Role Alignment      [ X / 10 ]             │
│  Pain Alignment      [ X / 10 ]             │
│  Timing Signals      [ X / 10 ]             │
│  Relationship Fit    [ X / 10 ]             │
├─────────────────────────────────────────────┤
│  OVERALL SCORE       [ X.X / 10 ]           │
└─────────────────────────────────────────────┘

VERDICT: [Worth pursuing / Proceed with caution / Do not pursue]

REASONING:
[3–4 sentences. Be specific. Reference actual signals from their profile,
not generic assumptions. If the score is below 5, say clearly why and
ask the user if they want to continue.]
```

---

### MODULE 2, CONVERSATION TEMPERATURE

**What this is:** Every prospect exists on a spectrum from completely cold to ready to buy. Your opening must match where they actually are, not where you wish they were.

**Read these signals from their profile and content:**

| Signal | What it tells you |
|---|---|
| Posting frequency | Active posters are more open to conversation |
| Content tone | Personal stories = open; purely promotional = guarded |
| Comment engagement | Conversational = warm; formal/absent = cold |
| Response patterns | Quick, chatty replies in comments = high openness |
| Profile completeness | Detailed About section = invested in their professional image |
| Recent activity | New role, new content series, new business = timing shift |

**The three temperatures:**

**❄ COLD**, They don't know you. Trust is zero. They scan for threat before opportunity.
- What they need: safety, proof you're human, a reason this isn't spam
- What kills it: any hint of pitch, pressure, or qualification in the opener
- Energy required: patient, low-ask, genuinely curious

**◎ WARM**, They're open but not leaning in. Curious but cautious.
- What they need: a reason to invest a reply, something relevant to their world
- What kills it: going too deep too fast, or staying too surface-level
- Energy required: engaged, peer-to-peer, subtly insightful

**🔥 HOT**, They're signalling readiness. Fast replies, initiating questions, future-tense language.
- What they need: a clear next step, a specific invitation
- What kills it: waffling, another round of small talk, missing the signal
- Energy required: direct, confident, clear

**Output format:**
```
┌─────────────────────────────────────────────┐
│  CONVERSATION TEMPERATURE                   │
├─────────────────────────────────────────────┤
│  Reading: ❄ COLD  /  ◎ WARM  /  🔥 HOT     │
│  Confidence: High / Medium / Low            │
└─────────────────────────────────────────────┘

EVIDENCE:
[What specific signals from their profile or content led to this reading.
Be precise, quote or reference actual observations, not assumptions.]

APPROACH IMPLICATION:
[One sentence. What does this temperature mean for the very first message?]
```

---

### MODULE 3, COMMUNICATION STYLE MAPPING

**What this is:** The same message lands completely differently depending on how a person processes information and makes decisions. Map their style before writing a word.

Identify their primary style by reading their content, language, and tone:

**⚡ DRIVER**, Direct, decisive, results-first
- Profile signals: Short punchy posts, achievement language, titles like CEO/Founder/MD, "we grew X by Y" framing
- What they respect: efficiency, outcomes, directness
- What they hate: small talk, vague language, being kept waiting
- Message energy: Get to the point in sentence one. Lead with what's in it for them. Zero fluff.

**✦ EXPRESSIVE**, Social, story-driven, relationship-first
- Profile signals: Personal photos, story-based posts, lots of comments and engagement, inspirational content, "journey" language
- What they respect: warmth, personality, genuine connection
- What they hate: cold automation, being treated as a number
- Message energy: Match their warmth. Ask about them first. Let them talk. Be a person.

**◆ AMIABLE**, Sincere, helpful, community-oriented
- Profile signals: Advice posts, "here's what I've learned" content, supportive commenting, collaborative language
- What they respect: sincerity, patience, mutual benefit
- What they hate: pressure, hard pitches, being rushed
- Message energy: Take your time. Focus on being genuinely useful. Never rush to the ask.

**▣ ANALYTICAL**, Evidence-driven, precise, detail-oriented
- Profile signals: Stats-heavy posts, frameworks, case studies, credentials prominently displayed, precise language
- What they respect: accuracy, specificity, substance
- What they hate: vague claims, hype, anything unsubstantiated
- Message energy: Lead with a specific insight or data point. Be credible before being interesting.

**Output format:**
```
┌─────────────────────────────────────────────┐
│  COMMUNICATION STYLE                        │
├─────────────────────────────────────────────┤
│  Primary type: ⚡ DRIVER / ✦ EXPRESSIVE /   │
│                ◆ AMIABLE / ▣ ANALYTICAL     │
│  Confidence: High / Medium / Low            │
└─────────────────────────────────────────────┘

EVIDENCE:
[Specific signals from their profile, posts, or language that reveal
this style. If confidence is Low, explain what's missing.]

TONE IMPLICATION:
[One sentence. How must the message feel to land well with this person?]

WHAT TO AVOID:
[One specific thing that would immediately put this person off.]
```

---

### MODULE 4, THE HUMAN HOOK

**What this is:** The single most important output of this entire skill. One observation, 10 to 14 words, that proves you actually looked at this human, not just their job title.

A bot cannot write this. A template cannot produce this. If it could, it's wrong.

**The rules:**
- Reference something specific: a post they wrote, a line from their About section, their banner image, a client testimonial, a recent comment, a business decision they made public
- It must feel genuine, not manufactured admiration, but honest observation
- 10–14 words maximum
- It must pass the "could I have written this about anyone else?" test, if yes, rewrite it

**Strong examples:**
- *"That post about walking away from a retainer client, took guts."*
- *"Your About section doesn't sell, it respects the reader. Rare."*
- *"Three years, same niche, same message. That kind of patience builds something real."*
- *"That banner isn't trying too hard. It just is. Works."*

**Weak examples (rewrite these):**
- *"Love your profile!"*, generic, tells them nothing
- *"Really impressive work!"*, could be sent to anyone
- *"Your content is great!"*, meaningless, zero specificity

**Output format:**
```
┌─────────────────────────────────────────────┐
│  THE HUMAN HOOK                             │
├─────────────────────────────────────────────┤
│  "[Exact 10–14 word phrase]"                │
│                                             │
│  Source: [What it references]               │
│  Why it works: [One sentence]               │
└─────────────────────────────────────────────┘
```

> If you cannot produce a genuine, specific hook from the information provided, do not invent one. Tell the user what to look for before you proceed.

---

### MODULE 5, OPENING STRATEGY

**What this is:** Based on the temperature, communication style, and hook, select the opening approach and explain exactly why.

**The four openers:**

**→ THE PEER OPENER**, For warm prospects, Expressive and Amiable types
Best for someone who seems open, social, and low-on-guard. The goal is to establish you're a person, not a pitch.
> *"Great to connect [NAME]. No agenda on my end. Quick question while we're new to each other, are you more of a content scroller or an actual conversationalist on here? Either works for me :) P.s. [Human Hook]"*

**→ THE PATTERN INTERRUPT**, For Expressive types in competitive, saturated niches
Best for someone who gets messaged constantly and filters for people who see what others miss.
> *"Hey [NAME], I connect with a lot of people in [industry]. Most are dealing with [pain point]. You seem to be doing something different. Curious what's working for you right now?"*

**→ THE DIRECTNESS PLAY**, For Driver and Analytical types, or cold prospects
Best for people who have no patience for small talk and respect efficiency above warmth.
> *"Hey [NAME], I'll skip the build-up. I noticed something on your [profile/content] I think I can help with, quickly and without cost. Worth sharing?"*

**→ THE AUTHORITY FLIP**, For high-status prospects, strong profiles, or when you have genuine grounds to be selective
Best used when you can credibly position yourself as the one evaluating, not the one pitching.
> *"Hey [NAME], I don't send many of these. Your profile stood out when I was looking through [niche/industry], specifically [what stood out]. Had to ask: [one genuine question about it]."*

**Output format:**
```
┌─────────────────────────────────────────────┐
│  RECOMMENDED OPENING STRATEGY               │
├─────────────────────────────────────────────┤
│  → [Opener name]                            │
└─────────────────────────────────────────────┘

WHY THIS OPENER:
[2–3 sentences connecting the temperature, communication style, and
specific details of this prospect to the choice. This should feel
inevitable, not arbitrary.]

WHAT TO WATCH FOR IN THEIR REPLY:
[One or two signals that would confirm or change your read on them
once they respond, so The Outreach Writer knows what to do next.]
```

---

## ━━ FINAL INTELLIGENCE BRIEF ━━

Deliver the complete output in this format, no exceptions:

```
════════════════════════════════════════════════
  PROSPECT INTELLIGENCE BRIEF
  [Name] · [Role] · [Company]
════════════════════════════════════════════════

MODULE 1, STRATEGIC FIT
[Full Module 1 output]

────────────────────────────────────────────────

MODULE 2, CONVERSATION TEMPERATURE
[Full Module 2 output]

────────────────────────────────────────────────

MODULE 3, COMMUNICATION STYLE
[Full Module 3 output]

────────────────────────────────────────────────

MODULE 4, THE HUMAN HOOK
[Full Module 4 output]

────────────────────────────────────────────────

MODULE 5, OPENING STRATEGY
[Full Module 5 output]

════════════════════════════════════════════════
  BRIEF COMPLETE
  → Ready for The Outreach Writer
════════════════════════════════════════════════
```

---

## ━━ NON-NEGOTIABLE RULES ━━

- **Never produce a generic brief.** If the information is insufficient, ask for more, don't invent.
- **Never confuse style type with temperature.** They are separate readings. A hot Driver and a cold Driver need completely different openers.
- **The Human Hook must be impossible to fake.** If it sounds like it could go to anyone, it goes to no one.
- **Always end with a clear handoff.** This brief feeds The Outreach Writer. Say so.
- **If the Strategic Fit Score is below 5, flag it visibly** and ask the user whether to continue before writing the brief.


## ━━ SELL-BY-CHAT FRAMEWORK ━━

Read `references/sell-by-chat-framework.md` before writing any message.
Apply: serving mindset over selling mindset, LVQ rhythm, A→B gap qualification, one question per message, value before every ask, follow-up cadence, micro-commitment booking tactics.
