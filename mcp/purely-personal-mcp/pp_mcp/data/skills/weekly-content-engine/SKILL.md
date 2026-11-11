---
name: weekly-content-engine
description: One short idea in, three publish-ready outputs out: a long-form LinkedIn post, a 5-7 slide carousel, and a save-worthy cheatsheet, each with a Canva AI handoff prompt. Voice-locked to the operator's Voice DNA and ICP-locked to their ICP. Triggers on "build my week of content", "give me my weekly drop", "weekly content engine", "I need posts for this week".
version: 1.0.0
author: daniel-paul
tags: [linkedin, content-system, weekly, canva]
---

# Weekly Content Engine


---

## Why this vs ChatGPT?

**Problem with raw ChatGPT:** Ask for "a week of LinkedIn content" and you get five generic posts with no voice, no ICP awareness, no usable visuals, and the cheatsheet is just bullet points in chat. You still have to design every visual manually.

**This skill provides:**

1. **One form, three outputs**. Profile, goal, 3 pillars in. Post + carousel + cheatsheet out. No back-and-forth prompts.
2. **Voice-locked**. Pulls the user's Voice Snapshot from Project Knowledge so every output reads like them, not like AI.
3. **ICP-locked**. Pulls the user's ICP Doc so every post speaks to a real customer, not a vague audience.
4. **Self-scored 4/4**. Each output runs through the Invisibility Diagnostic (Voice, POV, Specificity, Asking) before render. Anything under 4 gets a one-line fix.
5. **Canva AI handoff**. Cheatsheet + carousel ship with a "premium editorial designer" master prompt the user pastes into Canva AI for a 5-minute designed visual. No graphic designer needed.

**You can replicate this with ChatGPT if you:** prompt 3 times, write your own Canva design brief, paste outputs into Canva manually, score against the 4 dimensions yourself. Takes 45-60 minutes. This skill does it in 2 minutes.

---

## Required inputs

| Input | Source | If missing |
|---|---|---|
| User's Voice Snapshot (or full Voice DNA) | Claude Project Knowledge | STOP. run `voice-profile-builder` first |
| User's ICP Doc | Claude Project Knowledge | STOP. ask the operator for their ICP (ICP.md or the Business Brain) |
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
| `preview` | Standard + HTML preview artifact (matches the rest of the bundle) | Pre-publish review, team handoff |


---

## The 3 outputs (what you get)

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

## Examples

> **Illustrative only.** The names, numbers and results in the examples below are invented to show the format. Never reuse them. In real output use only facts from the operator's Business Brain or from the request, and leave a detail out rather than make one up.

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
[full premium editorial designer prompt with these 7 slides embedded — see prompts/canva-carousel.md]

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
[full premium editorial designer prompt with these 7 questions embedded — see prompts/canva-cheatsheet.md]
```

---

## Limitations

- **Will not work without Voice + ICP in Project Knowledge.** Outputs degrade to generic content. The skill stops and points the user at `voice-profile-builder` and your ICP.md.
- **Canva AI handoff requires a Canva account.** The prompts work in any AI-assisted design tool (Canva AI, Adobe Firefly, ChatGPT image), Canva is the cleanest path.
- **Photos are optional.** If uploaded, the skill switches image prompts to photo direction. The skill does not crop, resize, or store the photos.
- **One week at a time.** This is not a content calendar tool. For multi-week planning, run weekly.

---

## Pro tips

1. **Always fill the "real result this week" field.** It is the highest-leverage input. Voice + ICP shape the tone, but the real story shapes the hook. Skip it and the post drops from "this is mine" to "this is generic."
2. **Use the same 3 pillars for 4 weeks before changing them.** Audience needs repetition to recognise your themes. Rotating pillars every week feels like noise.
3. **Schedule the 3 outputs the same day they are generated.** Friction kills publishing. Generate Monday morning, schedule all 3, done.
4. **Run `competitor-x-ray` once a quarter and feed the "topic to own" in as pillar 1.** That is the biggest unlock for cutting through.

---
## Use in the Purely Personal connector


After the draft: Score each output with score_post, then polish_post and de_ai_ify.
