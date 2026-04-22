# Purely Personal — Team Onboarding

> Read this first. Find your role at the bottom. 10-minute read.

---

## 1. What Purely Personal Is (in one minute)

**A 2-day live workshop** where solopreneurs and founders install a working AI Marketing + Sales system inside Claude Code — in their own voice, for $49.

**The deliverable is a plugin** they install on their laptop. Not a SaaS they rent. Not a service we do for them. They leave with the system working, forever theirs.

**The promise:** 4 hours of their time = 5 AI executives running their marketing + sales every week automatically, without needing to hire anyone.

---

## 2. Why This Exists

Most solopreneurs are doing five jobs at once. They know they should post consistently, follow up on leads, research prospects, prep for meetings, manage cash. But they're one person. So things fall through.

They've tried every "AI writing tool" on the market. All of them sound like ChatGPT. None of them sound like *them*.

**We solve this with one file and five commands:**

- One file called `BUSINESS-BRAIN.md` (9 sections: voice, offer, ICP, competitors, etc.)
- Five slash commands that read the Brain and ship real work in the user's voice
- Every output is specific, personalized, publishable

Because every output reads the user's Brain first, the AI sounds like them, not like a corporate press release.

---

## 3. What We're Building (three products)

### Product A — The Workshop ($49)
A live 2-day Zoom workshop where attendees build their Marketing Machine + Sales Machine live. This is our top-of-funnel.

- **Dates:** May 2–3, 2026 · 11am–1pm Finland time · 2 hours each day
- **Format:** Live on Zoom · max 40 seats · no replay for Workshop 01
- **Outcome:** Each attendee walks away with a working system they'll keep forever

### Product B — The Cohort ($2,400)
A 90-day immersion for founders who want to run this as their operating system. Upsell from the Workshop.

- **Format:** Workshop + weekly office hours + private Slack + 1:1 with Danny + premium engines
- **Next cohort:** June 2026 · 10 seats
- **Purpose:** This is where the real revenue comes from. Workshop 01 exists to feed the Cohort.

### Product C — The Open-Source Plugin
The `purely-personal` plugin lives on GitHub, free for anyone to clone. It's the workshop deliverable AND a permanent marketing asset.

- **Repo:** [github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself](https://github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself)
- **License:** MIT (free to use and modify)
- **Purpose:** Credibility + distribution. Every GitHub star, fork, and clone is an inbound lead for the Workshop.

---

## 4. How It All Fits Together

The customer journey, end to end:

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   1. STRANGER sees a LinkedIn post or Claude Design cheatsheet       │
│                ↓                                                     │
│   2. Lands on purely-personal-workshop.vercel.app                    │
│                ↓                                                     │
│   3. Watches the 2-min VSL · reads the page                          │
│                ↓                                                     │
│   4. Clicks "Reserve my seat · $49"                                  │
│                ↓                                                     │
│   5. GHL funnel captures name + email + LinkedIn URL + $49 payment   │
│                ↓                                                     │
│   6. Receives 7 emails over 2 weeks (install, reminders, pre-work)   │
│                ↓                                                     │
│   7. Day 0: Danny runs /prep-workshop-slides on the attendee list    │
│              → personalized slide per attendee generated              │
│                ↓                                                     │
│   8. Day 1 Zoom: first 3 min shows each attendee's own slide         │
│              → mind-blown moment #1                                   │
│                ↓                                                     │
│   9. Workshop runs over 2 days · attendee leaves with system         │
│                ↓                                                     │
│  10. Day 7: email check-in · 10% convert to Cohort ($2,400)          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

Every stage has an asset. We've built most of them. The team's job is to finish the rest and ship the first cohort on May 2.

---

## 5. What's Already Built (inventory)

All of this is live in the GitHub repo. 5 commits shipped. 56+ files.

### ✅ The Plugin
- `3 skills` — business-brain-renderer, content-visual-builder, engine-output-builder
- `8 slash commands` — /build-my-brain, /marketing-engine, /sales-engine, /operations-engine, /cash-engine, /leadership-engine, /prep-workshop-slides, /ship-it-live
- `1 Python script` — HTML→PDF export via Playwright

### ✅ The Workshop Materials
- `5 fillable HTML worksheets` — YOU™, The Offer™, Your One Client™, The Gaps™, Your Engines™ — Taki-style with Claude Prompts + Guidelines
- `1 facilitator run-of-show` — minute-by-minute script for both days
- `1 mind-blown activities guide` — the 3 memorable moments that make the workshop 10/10
- `1 attendee slideshow system` — personalized opening slides + auto-cycle

### ✅ The Landing Page
- Live at [purely-personal-workshop.vercel.app](https://purely-personal-workshop.vercel.app)
- V3 visual language (cream + red + dark drumbeats)
- 15 sections: hero, VSL slot, proof band, problem, promise, value stack ($4,200 → $49), Day 1/Day 2, schedule table, testimonials, trainer bio, pricing, FAQ, final CTA
- Auto-deploys on push to main

### ✅ The Lead Magnet
- `Claude Design cheatsheet` — 10 recipes for Claude Design, as PDF + PNG
- 1080×1350 portrait (LinkedIn-ready)
- Links back to the workshop

### ✅ The GHL Build Spec
- 15-section spec for a GHL specialist to build the funnel in ~3 hours
- 7 pre-written email templates in Danny's voice
- Webhook integration that feeds `/prep-workshop-slides` automatically

### ✅ Sample Asset
- `BUSINESS-BRAIN.rendered.html` — what the deliverable looks like when filled in
- This is our "demo" artifact

### ❌ Not Yet Built (team focus)
- The VSL video (record once, paste URL in landing page)
- Real testimonials for the landing page (placeholder exists)
- The GHL funnel (spec ready, needs a specialist to build)
- Demo GIF of `/build-my-brain` running
- Screenshots of the rendered Brain on social
- Launch content (LinkedIn post series, newsletter announcement)

---

## 6. The Workshop in 60 Seconds

**Pre-setup (30 min async, before Day 1):** attendees install Claude Code, run a health-check, submit their LinkedIn URL.

**Day 1 (2h live, Saturday May 2):**
- First 3 minutes: everyone sees their own personalized slide (their name, voice analysis, signature hook)
- Live voice autopsy on 3 volunteers
- 3 worksheets filled: YOU, Offer, Ideal Client
- Live demo: `/marketing-engine` on Danny's Brain
- Last 20 min: **ship a real LinkedIn post live** before Zoom closes

**Day 2 (2h live, Sunday May 3):**
- 2 more worksheets: The Gaps + Your Engines
- Live demos of all 5 engines
- The Brain renders as a one-pager (the reveal)
- Each attendee commits to running one engine unattended for 7 days

**Outcome:** attendee walks away with a filled Brain + 5 engines + their first published post + a 7-day commitment.

---

## 7. The Money

| Metric | Workshop | Cohort |
|--------|----------|--------|
| Price | $49 | $2,400 |
| Seats per run | 40 | 10 |
| Max revenue per run | $1,960 | $24,000 |
| Frequency | Monthly | Quarterly |
| Annual upper bound | ~$23,000 | ~$96,000 |

**The unit economics:**
- Workshop exists to **find Cohort buyers**. 10% conversion = 4 Cohort signups per Workshop = $9,600 per 40-person workshop.
- With a monthly Workshop cadence, that's ~$9,600 × 12 = **$115,000/year from Cohort conversions alone.**
- Workshop fee ($1,960/run) covers Danny's time + Claude costs + any paid ads.
- The plugin is the moat. Every cohort member becomes a case study.

---

## 8. Your Role (find yours below)

### 🎨 Designer (Ilef / Catherine / Anny)

**What you own:** the visual layer.

**Priorities:**
1. Finalize the 5 engine icons (megaphone / target / grid / bar chart / compass) — current ones are functional placeholders
2. Design a proper founder headshot slot (the current "DP" initials circle is placeholder)
3. Design a social preview image (OG card) for the landing page
4. Approve the V3 visual language — it's already working but we want your sign-off
5. Design the LinkedIn launch carousel (post + 5 slides) promoting the Workshop

**Where to work:** Everything visual lives in `landing-page/`, `skills/business-brain-renderer/references/`, `worksheets/`

**Visual reference:** the V3 design language = cream paper (`#faf8f4`) + red accent (`#e90d41`) + dark drumbeats (`#0f0f10`) + Rethink Sans (display) + Inter (body) + JetBrains Mono (code). Don't introduce new brand colors.

---

### 👨‍💻 Developer / Skill Builder (Malik)

**What you own:** the plugin itself.

**Priorities:**
1. Test `/prep-workshop-slides` end-to-end with a real Apify LinkedIn scrape
2. Add error handling for when `apify-linkedin` rate-limits
3. Build the VSL video embedding logic in the landing page (swap placeholder for iframe)
4. Write a README section with screenshots of each engine's output
5. Record a 60-second demo GIF using `demo/build-my-brain.tape` with `vhs`

**Where to work:** `skills/`, `commands/`, `scripts/`

**Key files to understand:**
- `skills/business-brain-renderer/references/code-templates.md` — the visual templates
- `skills/business-brain-renderer/references/design-system.md` — the tokens
- `commands/prep-workshop-slides.md` — the hero command
- `commands/ship-it-live.md` — the Day 1 finale activity

---

### 🚀 GHL / Funnel Specialist

**What you own:** the checkout + email automation.

**Priorities:**
1. **Read the full spec** at `integrations/ghl-build-spec.md` (15 sections)
2. Build the Workshop 01 funnel in GHL (~3 hours first-time)
3. Configure the Stripe $49 product + payment flow
4. Create 7 email templates (all copy is pre-written — paste as-is)
5. Wire the webhook to Zapier → Google Sheet for attendee export
6. Run the QA checklist (§10 of the spec)
7. Ship one test $49 payment end-to-end before opening registration

**When done:** send Danny the GHL funnel URL and he'll swap it into the landing page.

---

### 📝 Content / Marketing Lead

**What you own:** filling the Workshop + feeding the pipeline.

**Priorities:**
1. **Write the launch sequence** — 5 LinkedIn posts announcing Workshop 01 (hook, story, testimonial, countdown, final call)
2. **Collect 3 real testimonials** from Workshop 00 / past clients — drops into the testimonials section
3. **Design the launch schedule** — aim for 2 weeks of posting before April 30 (to hit the May 1 registration close)
4. **Script the VSL** (2-minute video) — Danny records it but you write the script
5. **Newsletter announcement** — the Purely Personal list gets a dedicated issue for the Workshop

**Voice rules (non-negotiable):**
- No em-dashes
- No "unlock", "delve", "supercharge", "game-changer"
- Short sentences. One idea per line.
- Always end LinkedIn posts with a P.S. question
- Specifics only — "12 hours a month" beats "many hours"

Every piece of content should reference Danny's actual wins: `$0 content cost`, `2hr/wk on content`, `5 AI executives running`.

---

### 🧑‍💼 Sales / Cohort Lead

**What you own:** converting Workshop graduates to Cohort buyers.

**Priorities:**
1. **Read the plugin README** to understand what Cohort graduates actually get
2. **Draft the cohort waitlist email** (not yet written) — sends on Day 2 evening after the workshop close
3. **Build the cohort landing page** (not yet built — would be `/cohort` subpath on Vercel)
4. **Set up 1:1 intro calls** with the top 3 most engaged Workshop 01 attendees within 72 hours of Day 2
5. **Own the Day 7 check-in flow** — email reply triage, identifying Cohort-ready accounts

**Conversion target:** 10% of Workshop attendees → Cohort buyers = 4 out of 40 = **$9,600 revenue per Workshop**.

---

### 🧑‍🔧 Operations / VA

**What you own:** the machinery that makes every Workshop run.

**Priorities:**
1. **Own the attendee CSV** — export from GHL, format for `/prep-workshop-slides`
2. **24 hours before each Workshop:** run `/prep-workshop-slides attendees.csv` and review each generated slide
3. **Day 0 morning:** send the Zoom link SMS reminders to anyone who gave a phone number
4. **During Zoom:** monitor chat, DM confused attendees, flag tech issues to Danny
5. **After each Workshop:** pull post URLs, screenshot Brain renders, collect consent for social sharing

**The one thing you must not miss:** the LinkedIn URL is load-bearing. Every attendee needs one captured in GHL before Day 1 or they miss the personalized opening slide.

---

## 9. Where Everything Lives

```
purely-personal/                          ← the whole project
│
├── README.md                             ← repo hero page
├── TEAM-ONBOARDING.md                    ← you are here
├── LICENSE
│
├── landing-page/
│   └── index.html                        ← live at purely-personal-workshop.vercel.app
│
├── commands/                             ← 8 slash commands
│   ├── build-my-brain.md                 ← the intake
│   ├── marketing-engine.md
│   ├── sales-engine.md
│   ├── operations-engine.md
│   ├── cash-engine.md
│   ├── leadership-engine.md
│   ├── prep-workshop-slides.md           ← pre-workshop automation
│   └── ship-it-live.md                   ← Day 1 finale activity
│
├── skills/                               ← 3 skills powering the commands
│   ├── business-brain-renderer/          ← renders the one-page Brain
│   ├── content-visual-builder/           ← 4-platform content cards
│   └── engine-output-builder/            ← standalone section graphics
│
├── worksheets/                           ← 5 fillable HTML worksheets
│   ├── 01-you/
│   ├── 02-the-offer/
│   ├── 03-your-one-client/
│   ├── 04-the-gaps/
│   └── 05-your-engines/
│
├── workshop/
│   ├── run-of-show.md                    ← minute-by-minute facilitator script
│   ├── mind-blown-activities.md          ← the 3 memorable moments
│   └── attendee-slides/                  ← personalized opening slideshow
│
├── integrations/
│   └── ghl-build-spec.md                 ← 15-section GHL funnel spec
│
├── lead-magnets/
│   └── claude-design-recipes/            ← cheatsheet HTML + PDF + PNG
│
├── demo/
│   ├── storyboard.md                     ← 60-sec GIF storyboard
│   └── build-my-brain.tape               ← vhs recording script
│
├── examples/
│   ├── BUSINESS-BRAIN.sample.md          ← Danny's Brain as reference
│   ├── BUSINESS-BRAIN.rendered.html      ← what the deliverable looks like
│   ├── BUSINESS-BRAIN.pdf                ← same, PDF format
│   └── screenshots/                      ← 5 PNGs of the rendered Brain
│
└── scripts/
    └── build_pdf.py                      ← HTML→PDF export script
```

---

## 10. Current Status & What's Next

### Status: 80% built

We have the product. We have the workshop. We have the landing page. We have the spec for the funnel. We have 5 commits shipped.

### What's blocking launch (April 30 → May 2)

Ordered by who must do what:

| Who | What | Deadline | Status |
|-----|------|----------|--------|
| GHL specialist | Build funnel per spec | Apr 25 | Not started |
| Danny | Test $49 payment end-to-end | Apr 26 | Waiting on specialist |
| Content lead | Launch sequence posted | Apr 28 | Not started |
| Danny | Record VSL video | Apr 23 | Not started |
| Malik | VSL iframe swap in landing page | Apr 24 | Not started |
| Designer | 3 testimonial designs | Apr 26 | Not started |
| Content lead | Newsletter announcement | Apr 28 | Not started |
| Ops/VA | Registration open procedure | Apr 30 | Not started |
| All | Registration closes | **May 1** | Hard deadline |

If any item slips past its deadline, the Workshop 01 date slips too. This is the critical path.

### After Workshop 01 ships

- Launch Workshop 02 (duplicate everything, swap dates)
- Open Cohort June 2026 intake
- Publish the 10 Claude Design recipes cheatsheet as a LinkedIn lead magnet
- Start collecting case studies from Workshop 01 graduates

---

## 11. Glossary (for non-technical teammates)

| Term | What it actually means |
|------|-----------------------|
| **Claude Code** | Anthropic's terminal app that runs Claude on your computer (like ChatGPT but locally, with plugins) |
| **Plugin** | A folder of files that adds new features to Claude Code (our `purely-personal` folder) |
| **Skill** | A set of instructions Claude reads before acting (3 of them in our plugin) |
| **Slash command** | A shortcut that triggers a skill (e.g. `/marketing-engine`) |
| **MCP / Apify** | Tools that let Claude scrape real data from the web (LinkedIn, websites, Reddit) |
| **BUSINESS-BRAIN.md** | The one markdown file that contains the user's voice, ICP, offer, competitors |
| **Engine** | Our word for a slash command that does a specific job (Marketing, Sales, Operations, Cash, Leadership) |
| **Brain render** | Turning the text `BUSINESS-BRAIN.md` into a beautiful HTML page (via `/render-brain`) |
| **V3 design language** | Our current visual brand — cream + red + dark drumbeats |
| **Taki-style worksheets** | Our 4-column fillable worksheet format (based on Taki Moore's coaching system) |
| **Mind-blown activities** | The 3 workshop moments designed to create emotional peaks for attendees |
| **Proof band** | The dark horizontal strip with 3 big stats ($0 / 2hr/wk / 5 engines) |
| **Funnel** | The checkout + email automation flow in GHL |
| **VSL** | Video Sales Letter — the 2-minute explainer video on the landing page |
| **Cohort** | The $2,400 premium program (Workshop is the top-of-funnel for this) |
| **GHL** | GoHighLevel — the CRM + email + funnel platform we use |

---

## 12. What To Do Right Now

1. Find your role in §8
2. Read the files linked in your section
3. DM Danny in the team Slack with your one clarifying question
4. Ship your first deliverable by end of this week

If you're unclear about anything in this document, reply in Slack and we'll fix the doc so the next person isn't confused too.

---

**Document owner:** Daniel Paul
**Last updated:** Apr 21, 2026
**Next review:** Apr 28 (before launch week)
