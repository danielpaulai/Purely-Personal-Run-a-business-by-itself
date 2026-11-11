---
name: weekly-content-engine
description: The Day 1 stage demo skill. One short form in, three published-ready outputs out, a long-form LinkedIn post, a 5-7 slide carousel, and a save-worthy cheatsheet. Each output ships with copy buttons and a Canva AI handoff prompt that turns the cheatsheet and carousel into designed visuals in under 5 minutes. Voice-locked to the user's Voice Snapshot, ICP-locked to their ICP Doc, both pulled from Claude Project Knowledge. Triggers on "build my week of content", "give me my weekly drop", "generate my LinkedIn week", "weekly content engine", "I need posts for this week", "weekly drop", "content for the week".
version: 1.0.0
author: daniel-paul
tags: [linkedin, content-system, weekly, react-artifact, canva, ai-marketing-employee, demo, stage]
---

# Weekly Content Engine

The Day 1 stage demo. One short form, three publish-ready outputs, plus the Canva AI prompts that turn them into designed visuals in 5 minutes.

This is the skill that makes attendees say "I am keeping this forever" on Day 1.

---

## Why this exists

Day 1 used to ship one 4/4 LinkedIn post per attendee. That is a good win. But across 312 attendees we need a **bigger** visible quick win that converts to the paid cohort.

This skill replaces the single-post deliverable with a three-output weekly drop:

1. **Long-form LinkedIn post** (Monday) — 1300-1500 chars, 4/4 self-scored
2. **Carousel** (Wednesday) — 5-7 slides, cover + body + CTA
3. **Cheatsheet** (Friday) — title + 5-7 items, save-worthy

Plus the two **Canva AI handoff prompts** that turn the carousel and cheatsheet into designed visuals attendees can publish the same day.

Pattern is borrowed from Ilef's `linkedin-content-system` (proven in her last cohort, Eduardo + Rob both validated) and upgraded with our Voice DNA, ICP, and 4/4 Invisibility Diagnostic.

---

## Why this vs ChatGPT?

**Problem with raw ChatGPT:** Ask for "a week of LinkedIn content" and you get five generic posts with no voice, no ICP awareness, no usable visuals, and the cheatsheet is just bullet points in chat. You still have to design every visual manually.

**This skill provides:**

1. **One form, three outputs**. Profile, goal, 3 pillars in. Post + carousel + cheatsheet out. No back-and-forth prompts.
2. **Voice-locked**. Pulls the user's Voice Snapshot from Project Knowledge so every output reads like them, not like AI.
3. **ICP-locked**. Pulls the user's ICP Doc so every post speaks to a real customer, not a vague audience.
4. **Self-scored 4/4**. Each output runs through the Invisibility Diagnostic (Voice, POV, Specificity, Asking) before render. Anything under 4 gets a one-line fix.
5. **Canva AI handoff**. Cheatsheet + carousel ship with a "premium editorial designer" master prompt the user pastes into Canva AI for a 5-minute designed visual. No graphic designer needed.
6. **React .jsx live artifact**. The on-stage demo is a React form (not HTML) so input focus does not break mid-typing. Lesson learned from Ilef's first version.

**You can replicate this with ChatGPT if you:** prompt 3 times, write your own Canva design brief, paste outputs into Canva manually, score against the 4 dimensions yourself. Takes 45-60 minutes. This skill does it in 2 minutes.

---

## Required inputs

| Input | Source | If missing |
|---|---|---|
| User's Voice Snapshot (or full Voice DNA) | Claude Project Knowledge | STOP. run `voice-profile-builder` first |
| User's ICP Doc | Claude Project Knowledge | STOP. run ICP Builder first |
| Profile (name, role, service, ideal client) | Form input, live | Form blocks generate until role + service filled |
| 1-3 content pillars | Form input, live | At least pillar 1 required |
| Goal (single select) | Form input, live | Defaults to "Attract clients" if skipped |
| Real result or story from this week (optional but nudged) | Form input, live | Skill works without it but output is noticeably weaker |
| Photos (optional, multiple) | Form input, live | If photos uploaded, image prompts become photo direction instead |

---

## Modes

| Mode | What you get | Best for |
|------|---|---|
| `quick` | Long-form post only, no carousel or cheatsheet | One-off post writing |
| `standard` (default) | Post + carousel + cheatsheet, all 4/4 self-scored | Weekly drop, stage demo |
| `visual` ★ | Standard + React .jsx live form artifact for interactive use | Day 1 Game 1, live workshop |
| `preview` | Standard + HTML preview artifact (matches the rest of the bundle) | Pre-publish review, team handoff |

**Default: `standard`. Use `visual` for the stage. Use `preview` to render the HTML version that matches the other 11 skills.**

---

## The 3 outputs (what attendees take home)

### Output 1, long-form LinkedIn post (Monday slot)
- 1300-1500 chars
- Line-break formatted for mobile
- Scroll-stopping first line drawn from the user's "real result this week" field
- No em dashes. No banned AI words. No emojis.
- Soft CTA or question at the end
- 4/4 score required before render

### Output 2, carousel (Wednesday slot)
- 5-7 slides
- Slide 1 = hook cover, slide N = CTA
- Each slide: title + 1-2 line body
- Caption (120-150 chars) above the slides
- Canva AI prompt appended for one-click design handoff
- 4/4 score on the caption + cover slide before render

### Output 3, cheatsheet (Friday slot)
- Title + 5-7 items
- Each item: short label + 1-2 line body
- Caption (120-150 chars) above the cheatsheet
- Canva AI prompt appended for one-click design handoff
- 4/4 score on caption + title before render

Each output gets its own copy button. Carousel and cheatsheet get TWO copy buttons each: one for content, one for the Canva AI prompt.

---

## Process

### Phase 1, validate inputs
1. Voice Snapshot in Project Knowledge?
2. ICP Doc in Project Knowledge?
3. Form fields: role + service + pillar 1 filled?
4. If `visual` mode: render the React form first, wait for submit.

### Phase 2, build the system prompt
Compose a single Anthropic API call with the user's Voice DNA + ICP + form inputs. Ask for 3 outputs in one JSON response (post + carousel + cheatsheet).

### Phase 3, self-score 4/4
Run each output through the 4 Invisibility Diagnostic dimensions:
- **Voice** — sounds like them, no AI tells
- **POV** — a real opinion, not generic advice
- **Specificity** — concrete number, name, scene, or example
- **Asking** — clear CTA, question, or DM trigger

Anything under 4 gets a one-line rewrite suggestion in the output.

### Phase 4, attach Canva AI prompts
Append the cheatsheet master prompt to the cheatsheet output.
Append the carousel master prompt to the carousel output.

### Phase 5, render
- `standard` → markdown with all 3 outputs + scores + Canva prompts
- `visual` → React .jsx artifact for live workshop use
- `preview` → HTML 3-card artifact (light theme, paper-grid, Purely Personal red)

---

## Output structure (`standard` mode)

```
WEEKLY CONTENT ENGINE · 3 OUTPUTS · WEEK OF [date]
Voice: [user] · ICP: [from doc] · Goal: [selected]

═══════════════════════════════════════
OUTPUT 1, LONG-FORM POST (Monday)
Score: 4/4 (Voice ✓ POV ✓ Specificity ✓ Asking ✓)

[post body, 1300-1500 chars]

[Copy] [Edit voice] [Edit POV]

═══════════════════════════════════════
OUTPUT 2, CAROUSEL (Wednesday)
Score: 4/4

Caption:
[caption, 120-150 chars]

Slide 1, [title]
[body]

Slide 2, [title]
[body]

... [up to slide 7] ...

[Copy all slides] [Copy caption]

CANVA AI HANDOFF PROMPT:
[premium editorial designer prompt with the carousel copy embedded]

[Copy Canva prompt]

═══════════════════════════════════════
OUTPUT 3, CHEATSHEET (Friday)
Score: 4/4

Caption:
[caption, 120-150 chars]

[Title]
1. [Label]: [body]
2. [Label]: [body]
...
7. [Label]: [body]

[Copy cheatsheet] [Copy caption]

CANVA AI HANDOFF PROMPT:
[premium editorial designer prompt with the cheatsheet copy embedded]

[Copy Canva prompt]

═══════════════════════════════════════
NEXT STEPS
1. Paste post into LinkedIn, schedule for Monday 8am local
2. Paste carousel Canva prompt into Canva AI, polish in 5 min, schedule for Wednesday
3. Paste cheatsheet Canva prompt into Canva AI, polish in 5 min, schedule for Friday
```

---

## Output structure (`visual` mode)

React `.jsx` artifact (built per `scripts/widget.jsx`). 3 steps:

1. **Profile step** — name, role, service, ideal client, real result this week, optional photos
2. **Goal step** — single-select buttons (Attract clients / Build authority / Get DMs / Other)
3. **Pillars step** — 3 content pillars (pillar 1 required)

Then a `Generate my week` button. Loading state: "Writing your 3 outputs, takes about 20 seconds". Then a results screen with 3 cards, each with copy buttons + Canva AI prompts.

**Critical implementation notes** (lessons from Ilef's first version):
- Use **individual `useState`** per input field. Do not use a nested state object, it causes focus loss mid-typing.
- Build as React `.jsx`, **never** as HTML widget or `visualize:show_widget` call, the sandbox blocks keyboard input.
- Include all three Anthropic API headers: `Content-Type`, `anthropic-version: 2023-06-01`, `anthropic-dangerous-direct-browser-access: true`. Do not include `x-api-key`, Claude.ai injects it.
- `CopyButton` must implement both `navigator.clipboard.writeText` AND the `execCommand` fallback for sandboxed contexts.

See `scripts/widget.jsx` for the full reference implementation.

---

## Examples

### Example 1, solo wellness coach · standard mode

**Inputs:**
- Voice Snapshot: "direct, conversational, real numbers, no fluff"
- ICP: "Solo wellness coaches doing 5-30K USD/month"
- Profile: Sarah Lin, wellness coach, 1:1 coaching for women over 40
- Real result this week: "client lost 8kg in 90 days without giving up wine"
- Goal: Attract clients
- Pillars: Coaching frameworks · Client wins · Behind-the-scenes

**Output excerpt:**

```
OUTPUT 1, LONG-FORM POST (Monday) · 4/4

8 kilos in 90 days. Wine still in the fridge.

That is the result a client of mine got last quarter.

Most weight-loss programs tell women over 40 to cut everything. Wine, bread, dessert, late dinners. Then they wonder why nobody sticks past week 3.

We did the opposite. We kept the wine. We swapped 2 meals. We added one walk after dinner.

3 months later, 8kg gone. Energy up. Sleep better. Marriage still happy because Friday dinner did not become a fight.

The whole program is 3 things on a single page. Not 17.

If you are a coach building 1:1 packages for women over 40, comment "PAGE" and I will send you the single sheet I use to scope every program.

[Copy]

═══════════════════════════════════════
OUTPUT 2, CAROUSEL (Wednesday) · 4/4

Caption: "The 5-mistake list every wellness coach makes in year 1. I made 4 of them. Save this."

Slide 1, [Cover] "The 5 mistakes I made in year 1 as a wellness coach"
Slide 2, "Pricing per session, not per outcome"
Slide 3, "Saying yes to every prospect"
Slide 4, "Building a meal plan from scratch every week"
Slide 5, "Coaching during the school run"
Slide 6, "Not asking for the testimonial on the win day"
Slide 7, [CTA] "Which one are you making? Comment the number."

CANVA AI HANDOFF PROMPT:
[full premium editorial designer prompt with these 7 slides embedded — see scripts/prompts/canva-carousel.md]

═══════════════════════════════════════
OUTPUT 3, CHEATSHEET (Friday) · 4/4

Caption: "Save this. The 7 questions I ask every new client in our first 20 minutes."

THE FIRST 20 MINUTES, 7 QUESTIONS THAT BUILD THE WHOLE PROGRAM

1. What does your week look like Monday to Friday?
2. What time do you eat dinner?
3. What do you drink with dinner?
4. How many times a week do you walk for over 20 minutes?
5. What was the last weight-loss thing that actually worked, even for 2 weeks?
6. What is the meal you will never give up?
7. What does success look like for you in 90 days?

CANVA AI HANDOFF PROMPT:
[full premium editorial designer prompt with these 7 questions embedded — see scripts/prompts/canva-cheatsheet.md]
```

---

## Chains with other skills

| Upstream | How |
|---|---|
| `voice-profile-builder` | Required, supplies the Voice Snapshot |
| ICP Builder | Required, supplies the ICP |
| `competitor-x-ray` | Optional, the "topic to own" from competitor analysis seeds pillar 1 |

| Downstream | How |
|---|---|
| `invisibility-diagnostic` | Built in, each output is self-scored 4/4 before render |
| `multi-platform-amplifier` | Take the Monday long-form post and amplify to X + IG + Reels + Threads |
| `prospect-magnet` | Take the carousel topic, find 10 prospects, send 10 personalised DMs referencing the carousel |

**Suggested chain after output:**
> *"Week shipped. Next: run `multi-platform-amplifier` on the Monday post to ship it to X + IG + Reels + Threads. Then `prospect-magnet` on the carousel topic to find 10 prospects who would save this exact carousel."*

---

## Limitations

- **Will not work without Voice + ICP in Project Knowledge.** Outputs degrade to generic content. The skill stops and points the user at `voice-profile-builder` and the ICP Builder.
- **Canva AI handoff requires a Canva account.** The prompts work in any AI-assisted design tool (Canva AI, Adobe Firefly, ChatGPT image), Canva is the cleanest path.
- **Photos are optional.** If uploaded, the skill switches image prompts to photo direction. The skill does not crop, resize, or store the photos.
- **One week at a time.** This is not a content calendar tool. For multi-week planning, run weekly.

---

## Pro tips

1. **Always fill the "real result this week" field.** It is the highest-leverage input. Voice + ICP shape the tone, but the real story shapes the hook. Skip it and the post drops from "this is mine" to "this is generic."
2. **Use the same 3 pillars for 4 weeks before changing them.** Audience needs repetition to recognise your themes. Rotating pillars every week feels like noise.
3. **Schedule the 3 outputs the same day they are generated.** Friction kills publishing. Generate Monday morning, schedule all 3, done.
4. **Run `competitor-x-ray` once a quarter and feed the "topic to own" in as pillar 1.** That is the biggest unlock for cutting through.
5. **For the stage demo, pre-fill the form with a fake "Sarah Lin" profile.** Live typing eats stage time. Pre-fill, click Generate, walk through the output.

---

## Stage script (Day 1, Game 1)

This is the script for the live workshop demo. Adapt as needed.

> "Open Claude. Type `/weekly-content-engine`. The form pops up. You fill in 6 fields, takes 60 seconds. You click Generate. Claude pulls your Voice from Project Knowledge, pulls your ICP from Project Knowledge, and writes your week. 20 seconds. Three outputs. Post, carousel, cheatsheet. Each one scored 4 out of 4 against the Invisibility Diagnostic.
>
> Now look at the bottom of the carousel. There is a second button, Copy Canva prompt. Click it. Open Canva. Click Canva AI. Paste. 5 minutes later, a designed carousel. No designer. No template hunting. Just done.
>
> Same for the cheatsheet. Copy the Canva prompt, paste in Canva AI, 5 minutes, done.
>
> 3 publish-ready pieces of content with designed visuals, in 25 minutes total. That is what your AI Marketing Employee does on a Monday morning while you are still on your first coffee."

---

## GitHub + source references

- [**Ilef's linkedin-content-system**](https://github.com/) (private). Pattern source for the React `.jsx` form artifact, the 3-step flow, and the Canva AI handoff. Validated in her last cohort by Eduardo and Rob.
- [**Anthropic Claude Skills**](https://docs.claude.com/en/docs/claude-code/skills). React `.jsx` artifact spec.
- [**Claude artifacts**](https://www.anthropic.com/news/artifacts). React component sandbox notes.

---

## Bundled files

```
~/.claude/skills/weekly-content-engine/
├── SKILL.md                          (this file)
└── scripts/
    ├── render.py                     (JSON → HTML preview artifact for the bundle)
    ├── template.html                 (HTML preview template, light theme)
    ├── widget.jsx                    (React .jsx live form artifact, for `visual` mode)
    └── prompts/
        ├── canva-cheatsheet.md       (Canva AI master prompt, cheatsheet)
        └── canva-carousel.md         (Canva AI master prompt, carousel)
```

---

*Built for the AI Marketing Employee Challenge Day 1 stage demo. One form, three outputs, one Monday morning's worth of content in two minutes. The skill that converts attendees to the paid cohort.*
