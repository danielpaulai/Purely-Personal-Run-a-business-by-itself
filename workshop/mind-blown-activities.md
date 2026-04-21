# Mind-Blown Activities — Workshop 01 Facilitator Guide

Three moments that turn an 8/10 workshop into a 10/10 one students post about weeks later.

> **Rule:** a mind-blown moment happens TO the student, not ON the presenter's screen. Every activity in this guide moves the wow onto their data, their voice, their life.

**The 4 mechanisms:**
1. **Personalization surprise** — "It knows me better than I know myself"
2. **Compression** — "We did that in 4 minutes?"
3. **Dissonance** — "Wait, that's not how I thought it worked"
4. **Peer amplification** — "If THEY reacted like that, it must be real"

---

## Activity 1 — The Personalized Opening

> **When:** First 3 minutes of Day 1, as attendees join Zoom
> **Duration:** ~5 min (slides auto-cycle for ~15 sec each)
> **Mechanism:** Personalization surprise + Peer amplification
> **Prep time:** 24 hours before Day 1 (runs `/prep-workshop-slides`)

### The setup

Every attendee has submitted their LinkedIn URL during registration. 24 hours before Day 1, you run:

```
/prep-workshop-slides ./workshop/attendees.csv
```

This produces `workshop/attendee-slides/index.html` — a dark-themed slideshow with one slide per attendee.

Each slide contains:
- Their name in 104px display font
- Their headshot in a red-glow circle
- Their voice verdict in 3 words ("Direct. Conversational. Allergic to corporate.")
- 4 data points: posts analyzed, signature hook, favorite word, AI-slop score
- **One mind-blowing observation** pulled from their actual writing

### The execution

As attendees join the Zoom, screen-share `index.html` in full-screen (press **F**).

Don't explain what it is. Let it play.

First attendee slide appears: their name, their face, their data. Wait ~3 seconds. Watch the chat light up.

**What they're feeling:** *"That's me. How do you know that about me?"*

Let the slideshow cycle through all attendees. By the time you're ready to start the actual workshop, every attendee has:
1. Seen their own name on screen
2. Seen something true about themselves they didn't know
3. Watched the reaction to OTHER attendees — amplifying their own

**Facilitator rule:** don't interrupt the slideshow with narration. The silence is the point.

### The transition

Once the slideshow has cycled through all attendees (or you're at minute 5), pause on a blank slide and say:

> "What you just saw — I didn't write any of those observations. Claude read your last 30 posts and figured out what makes you, you. By the end of today, Claude is going to do that about your whole business. Let's start."

### The failure mode

If ANY attendee's slide contains a generic observation ("you're creative and thoughtful"), pull it before Day 1. Regenerate with more specific data or fall back to the honest state: "Welcome, {name}. Your Brain is about to get built."

Generic > absent.
Absent > fake-specific.

### The equipment check

- [ ] `workshop/attendee-slides/index.html` in browser, full-screen (F key)
- [ ] Zoom set to "HD video" + "Share sound" (sound isn't used, but no surprises)
- [ ] Backup: one slide per attendee as standalone HTML so you can manually advance if auto-cycle breaks

---

## Activity 2 — The Live Voice Autopsy

> **When:** Day 1, minutes 15–30 (right after the Universal Engine Pattern teach)
> **Duration:** 15 min (5 min per volunteer, 3 volunteers)
> **Mechanism:** Personalization surprise + Peer amplification
> **Prep:** pick 3 volunteers from the slideshow reactions

### The setup

From the slideshow reactions, you identified 3 attendees who reacted strongest to their own slide. Those are your volunteers.

DM each privately (before minute 15):

> "Quick ask — willing to volunteer your LinkedIn for a live analysis in 10 min? I'll pull one thing about your writing you'll find useful. Takes 3 min. Say 'yes' and you're in."

Three yeses = ready.

### The execution (15 min = 3 volunteers × 5 min each)

Volunteer 1:

> "Okay, {name}. Your LinkedIn is on screen. I'm going to run `voice-extractor` on your last 30 posts right now. Everyone watch."

Screen-share Claude Code. Paste their LinkedIn URL. Run:

```
Pull the last 30 posts from {linkedin_url} via apify-linkedin. Then run voice-extractor. Report:
- Their signature hook pattern
- The single most-overused phrase (they probably don't realize it)
- One stylistic tell that IS their voice
- One AI-slop pattern they're slipping into
```

Wait ~30 seconds. Output drops. Read it aloud.

**What to read:** the specific details. "Sarah, you open 7 out of 30 posts with 'I was..."'" — then look up. Watch their reaction. Narrate it back to the room.

> "See Sarah's face? That's the moment. She's known herself for 34 years. Claude's known her for 45 seconds."

Repeat for volunteers 2 and 3.

### The three things the analysis MUST produce per volunteer

1. **A specific stat they didn't know** ("34% of your sentences start with 'And' or 'But'")
2. **A word they're unconsciously attached to** ("You've used 'actually' 41 times in 30 posts")
3. **An AI-slop pattern OR signature pattern** ("Em-dashes in 19 of 30 posts" OR "Every 4th post ends with a question")

If ANY of these three is missing for a volunteer, pivot to a different volunteer. Don't ship a boring autopsy.

### The transition

After volunteer 3:

> "This is going to happen for every one of you, on every one of your engines, over the next 4 hours. The AI isn't writing FOR you. It's becoming YOU. Let's build that."

### Failure modes

| What could go wrong | Fix |
|-------------------|-----|
| `apify-linkedin` rate-limits mid-demo | Pre-pull all 3 volunteers' posts before the session. Paste directly. |
| One volunteer's analysis is generic | Switch to a pre-prepared "teaching example" using Danny's own LinkedIn |
| Volunteer gets defensive about a callout | Lean in. "Yes, that's the AI slop in your voice. By tomorrow you'll have filters for it." |

### The volunteer pre-flight

For each of the 3 volunteers, BEFORE the session, pre-run the voice-extractor on their data and keep the results in a notes doc. The live demo looks improvised; the prep makes sure the output lands.

---

## Activity 3 — Ship a Real LinkedIn Post Before Day 1 Closes

> **When:** Day 1, minutes 100–120 (last 20 minutes)
> **Duration:** 20 min
> **Mechanism:** Dissonance + Peer amplification + Compression
> **Requirement:** attendees have Worksheets 1 + 2 filled (at minimum)

### The setup

At minute 95, as the Q&A winds down, say:

> "Close your worksheets. I want every one of you to do one thing in the next 20 minutes: ship a real post on LinkedIn. Real account. Real audience. Right now."

Pause. Watch the room.

### The execution

Each attendee runs:

```
/ship-it-live
```

The command does the following for each attendee:
1. Reads their partial `BUSINESS-BRAIN.md`
2. Asks them: "What's one thing you learned today that your ICP needs to hear?"
3. Drafts a LinkedIn post in their voice
4. Runs strict voice validation
5. Opens LinkedIn composer with the post pre-populated (via clipboard)
6. Asks them to paste the URL back when posted

See `commands/ship-it-live.md` for the full workflow.

### The countdown moment

At minute 117 (3 min before close):

> "Everyone on 'hit Post' in 30 seconds. Count me down. 30… 29…"

Yes, this is theatrical. Yes, it works.

Watch the Zoom chat. Posts start dropping as URLs.

### The call-backs

At minute 119:

> "I'm clicking 5 of these right now. Live."

Click 5 random URLs. React out loud. Specifically call out:
- **Great hook:** "Jane opened with 'I spent 12 hours on this, then Claude took it over.' Jane, that's the personal-proof hook from the worksheet. You just shipped a week of content in 20 minutes."
- **Great CTA:** "Marcus ended with 'What's the one system you can't afford not to build?' That's a savable P.S. The hook writes the comments."
- **A shy one:** (find the shyest post, amplify it) "Sarah, you kept it tight. That's the cleanest voice in the cohort."

### The close

> "Four hours ago you were scrolling your feed. Now you have 42 posts shipped by 42 founders who walked in here strangers. Tomorrow we hire the other 4 executives. Same time."

### Failure modes

| What could go wrong | Fix |
|-------------------|-----|
| Some attendees refuse to ship | Don't pressure. Say: "Email me your URL tomorrow at 10am or you don't get access to Day 2 replay." Creates accountability without humiliation. |
| LinkedIn rate-limits someone | Rare. Save their draft. They post in the morning. |
| Post gets 0 engagement in the moment | Expected. Don't promise virality. The ritual matters, not the metric. |
| Time runs out at minute 120 | End at 120. Never run over. If 5 people didn't ship, DM them individually. |

### Why this works

Attendees walked in thinking "this will be a cool demo." They're walking out having **shipped something real**.

The dissonance ("I actually did the thing") is the moment. The cohort amplification ("they all did it too") seals it. The post URLs become social proof for the next workshop.

---

## Timing Integration Into Day 1

Here's how the 3 mind-blown activities slot into the existing Day 1 run-of-show:

```
00:00 - 00:05  ACTIVITY 1 — Personalized Opening Slideshow
00:05 - 00:15  Welcome + Universal Engine Pattern teach
00:15 - 00:30  ACTIVITY 2 — Live Voice Autopsy (3 volunteers × 5 min)
00:30 - 00:45  Activity: Worksheet 1 — YOU™
00:45 - 00:55  Demo: Voice Extraction
00:55 - 01:00  Break
01:00 - 01:15  Activity: Worksheet 2 — The Offer™
01:15 - 01:25  Demo: The $75K Moment
01:25 - 01:40  Activity: Worksheet 3 — Your One Client™
01:40 - 01:55  Q&A (wind down gently at 01:50)
01:55 - 02:00  ACTIVITY 3 — Ship a Real Post (starts early at minute 100)

Actually, revise: move Worksheet 3 earlier. Activity 3 needs the full 20 min.

00:00 - 00:05  ACTIVITY 1 — Personalized Opening
00:05 - 00:15  Universal Engine Pattern teach
00:15 - 00:30  ACTIVITY 2 — Live Voice Autopsy
00:30 - 00:45  Worksheet 1 — YOU™
00:45 - 00:55  Demo: Voice Extraction on YOUR Brain
00:55 - 01:00  Break
01:00 - 01:15  Worksheet 2 — The Offer™
01:15 - 01:25  Demo: The $75K Moment
01:25 - 01:40  Worksheet 3 — Your One Client™ (condensed — 15 min fill)
01:40 - 01:55  ACTIVITY 3 — Ship a Real Post
01:55 - 02:00  Close + Day 2 preview
```

---

## The Combined Effect

All 3 activities back-to-back create a crescendo of personalization:

| Moment | What attendee feels |
|--------|---------------------|
| Minute 0 | *"That's me on screen. In the first 30 seconds."* |
| Minute 15 | *"Three people just got the same level of analysis I got. This is going to happen to me too."* |
| Minute 30 | *"The AI is running on MY data now. I'm typing MY answers."* |
| Minute 100 | *"Wait, I'm actually about to post this publicly?"* |
| Minute 120 | *"I just shipped a LinkedIn post in my own voice in 20 minutes. What else can this do?"* |

That's the 10/10 workshop.

---

## The Post-Activity Capture

After the workshop, collect:

1. **Screenshots** of the 3 Live Voice Autopsy outputs (for future testimonials)
2. **Post URLs** from all Activity 3 ships (cohort social proof)
3. **Quotes** from the Zoom chat during the opening slideshow (raw reactions)

Turn these into a "Workshop 01 Recap" LinkedIn post + newsletter within 24 hours. The recap becomes the marketing for Workshop 02.

---

## Anti-patterns

- ❌ **Don't skip the prep for Activity 1.** A generic slideshow = zero mind-blown moments.
- ❌ **Don't let Activity 2 run more than 15 min.** Past 15 min it becomes a roast session.
- ❌ **Don't let Activity 3 slip later than minute 100.** 20 min is the floor for Ship.
- ❌ **Don't promise any specific outcome.** "Hit Post and see what happens." The ritual is the point.
- ❌ **Don't make Activity 3 optional.** The workshop promise IS shipping. Soft-optional becomes 50% participation.

---

## One Thing to Remember

The workshop isn't about the worksheets. The worksheets are the canvas. The workshop is about the 3 moments in this guide.

If Day 1 had only these 3 moments and nothing else, it would still be the best workshop the attendee has ever done.
