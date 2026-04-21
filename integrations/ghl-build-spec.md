# GHL Build Spec — Workshop 01 · Purely Personal
### Funnel → Form → Payment → Enrollment Email → Pre-Workshop Drip

**For:** GHL specialist / VA setting up the $49 workshop funnel in GoHighLevel
**Effort:** ~2 hours of GHL build time (one-time setup)
**Reusable:** duplicate the funnel for Workshops 02, 03, etc.

---

## 1. What We're Building

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │   Visitor lands on purely-personal-workshop.vercel.app           │
  │              ↓                                                   │
  │   Clicks "Reserve my seat" CTA                                   │
  │              ↓                                                   │
  │   GHL FUNNEL PAGE 1 — Checkout form + $49 Stripe payment         │
  │              ↓                                                   │
  │   GHL FUNNEL PAGE 2 — Thank-you page (Zoom link + next steps)    │
  │              ↓                                                   │
  │   IMMEDIATE EMAIL — "You're in" confirmation                     │
  │              ↓                                                   │
  │   WEBHOOK → exports name + LinkedIn URL to attendee CSV          │
  │              ↓                                                   │
  │   DRIP SEQUENCE — 6 emails from purchase to Day 2                │
  │              ↓                                                   │
  │   POST-WORKSHOP — Day 7 check-in + cohort upsell                 │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

**Three outcomes this must deliver:**
1. Attendee pays $49, gets instant confirmation + Zoom link
2. Attendee's LinkedIn URL lands in a CSV Danny can run `/prep-workshop-slides` on 24 hours before Day 1
3. Attendee gets nudged to install Claude Code + submit their LinkedIn before Day 1 starts

---

## 2. GHL Components to Build (checklist)

- [ ] **Funnel** named `Workshop 01 · May 2-3`
  - [ ] Page 1: Checkout (form + payment in one page)
  - [ ] Page 2: Thank-you (Zoom link, next steps, Slack invite)
- [ ] **Payment product** — `Workshop 01 Seat · $49 one-time`
- [ ] **Stripe connection** — confirm active in GHL billing settings
- [ ] **Custom fields** on Contact (see §4)
- [ ] **Tags** for segmentation (see §8)
- [ ] **Email templates** — 6 emails (see §5)
- [ ] **Automation workflow** named `Workshop 01 · Attendee Journey` (see §6)
- [ ] **Webhook** `on-workshop-purchase` to export attendee data (see §7)
- [ ] **Calendar event** → invite auto-added to attendee's Google/Outlook calendar

---

## 3. Form Schema — Page 1 (Checkout)

| Field | Type | Required | Custom field name | Purpose |
|-------|------|----------|------------------|---------|
| First name | text | yes | `first_name` (default) | Greeting in emails |
| Last name | text | yes | `last_name` (default) | Name on slide |
| Email | email | yes | `email` (default) | Primary contact |
| **LinkedIn URL** | url | **yes** | `linkedin_url` | **Powers `/prep-workshop-slides` — critical field** |
| Phone (WhatsApp) | phone | optional | `phone` (default) | SMS reminders Day 0 |
| Business stage | dropdown | yes | `business_stage` | Pre-workshop segmentation |
| Your #1 question | textarea | optional | `pre_workshop_question` | Fuel for Day 1 Q&A |

**Business stage dropdown options:**
- Idea stage (no revenue yet)
- 0–$100k revenue
- $100k–$500k revenue
- **$500k–$5M revenue (ICP match)**
- $5M+ revenue

**Form validation rules:**
- LinkedIn URL must start with `https://linkedin.com/in/` or `https://www.linkedin.com/in/`
- If it doesn't match, show error: *"Paste your LinkedIn profile URL. Example: https://linkedin.com/in/yourname"*
- Fail the form submit if LinkedIn URL is missing — it's load-bearing for Day 1

---

## 4. Payment Configuration

| Setting | Value |
|---------|-------|
| Product name | Workshop 01 Seat |
| Price | **$49 USD** |
| Payment type | One-time (not subscription) |
| Currency | USD |
| Tax | Configure per GHL tax settings (likely none for digital) |
| Stripe account | danny@danielpaul.ai linked Stripe account |
| Refund policy | 14-day, manual (flag in Stripe if requested) |
| Receipt | Enable GHL-generated receipt + Stripe receipt both |

---

## 5. Email Templates (write in Danny's voice — short, direct, specific)

### Email 1 — Immediate Confirmation
**Trigger:** Payment succeeds
**Send:** Instantly
**Subject:** You're in. Workshop 01 · May 2-3.

```
{{first_name}},

You're in. Workshop 01 is booked.

Here's the Zoom link: [ZOOM_LINK]
(Save it. I won't resend it until the morning of Day 1.)

Two things to do this week:

1. Watch the 5-min install video [PRE_SETUP_VIDEO_URL]
   This gets Claude Code working before we start.

2. Reply to this email with 3 competitor URLs.
   I'll have competitor intel ready for your Brain by Day 1.

Calendar invite for Day 1 + Day 2 is attached.

Questions? Reply here. I read every email personally.

— Daniel

P.S. The first 30 seconds of Day 1 will surprise you. Don't skip the pre-setup.
```

### Email 2 — Day -7 "What to expect"
**Trigger:** 7 days before May 2 (auto-scheduled)
**Subject:** One week out. Here's what we're building.

```
{{first_name}},

One week from today, you'll have:

- A LinkedIn profile rewritten in your voice
- 5 AI engines running on a weekly schedule
- A rendered BUSINESS-BRAIN.md worth $5k in positioning work

Tomorrow, I'll send the pre-setup video. It takes 5 minutes.

The week after, you'll wonder how you spent a year shopping for AI tools.

— Daniel
```

### Email 3 — Day -3 "Install day"
**Trigger:** 3 days before May 2
**Subject:** Install Claude Code today. 5 minutes.

```
{{first_name}},

Today: install Claude Code. Takes 5 minutes. Video here: [PRE_SETUP_VIDEO]

If anything breaks, reply to this email. I run a 15-min troubleshooting call Friday May 1 at 2pm Finland for anyone stuck.

Day 1 is Saturday, 11am Finland. Zoom link is in your first email.

— Daniel

P.S. If you can't find the Zoom link, search your inbox for "Workshop 01". It came from this exact email address.
```

### Email 4 — Day -1 "Last ask before Day 1"
**Trigger:** 1 day before May 2
**Subject:** One ask before tomorrow.

```
{{first_name}},

One ask.

Reply to this email with your LinkedIn URL so I can do the thing tomorrow that's going to blow your mind.

(I already have {{linkedin_url}} on file from signup, but confirm it's correct — that's the URL I'll use.)

See you at 11am Finland tomorrow. Zoom link: [ZOOM_LINK]

— Daniel

P.S. If your LinkedIn is private/locked, DM me — we have a workaround.
```

### Email 5 — Day 0 Morning "Zoom opens in 15 min"
**Trigger:** 8:45am Finland on May 2 (2h15 before session)
**Subject:** Workshop 01 starts in 2 hours. Zoom link inside.

```
{{first_name}},

Two hours to go.

Zoom: [ZOOM_LINK]

Before you join:
- Have Claude Code open
- Have your BUSINESS-BRAIN.md draft (blank is fine)
- Close Slack, Twitter, and the second monitor

See you at 11am Finland.

— Daniel
```

### Email 6 — Day 2 Evening "You made it"
**Trigger:** Sunday May 3, 6pm Finland
**Subject:** You built a business in 4 hours. Now run it.

```
{{first_name}},

You shipped a real LinkedIn post. You rendered your Brain. You have 5 engines wired up.

Four hours ago this didn't exist.

Your next action (this week):
- Run your chosen engine unattended for 7 days
- Day 3 check-in: I'll DM you Tuesday morning asking how it went
- Cohort Slack: you're already in. Post your first engine's output.

If Workshop 01 changed how you work, the Cohort changes how you operate. Details + waitlist: [COHORT_URL]

— Daniel

P.S. Reply with a screenshot of your rendered Brain. I'll feature 3 on LinkedIn next week.
```

---

## 6. Automation Workflow

**Workflow name:** `Workshop 01 · Attendee Journey`
**Trigger:** Payment succeeds for Workshop 01 product

### Step-by-step:

| # | Trigger/delay | Action |
|---|---------------|--------|
| 1 | Immediate | Apply tag `workshop-01-registered` |
| 2 | Immediate | Send **Email 1 — Immediate Confirmation** |
| 3 | Immediate | Fire **Webhook** (§7) to export LinkedIn URL |
| 4 | Immediate | Add calendar event to contact (iCal invite in email) |
| 5 | 7 days before May 2 (auto-schedule) | Send **Email 2 — Day -7** |
| 6 | 3 days before May 2 | Send **Email 3 — Day -3 Install** |
| 7 | 1 day before May 2 (morning) | Send **Email 4 — Day -1 LinkedIn ask** |
| 8 | May 2, 8:45am Finland | Send **Email 5 — Zoom in 2 hours** |
| 9 | May 2, 10:55am Finland | Send SMS: *"Workshop starts in 5 min. Zoom: [link]"* (if phone given) |
| 10 | May 3, 6:00pm Finland | Send **Email 6 — You made it** |
| 11 | May 3, 6:05pm Finland | Apply tag `workshop-01-completed` (assumes they attended — adjust if you track attendance) |
| 12 | May 10, 10am Finland (Day +7) | Send Day 7 check-in email (draft in §9) |

### Attendance tracking branch (optional)

Add a Zoom → GHL integration (if GHL has it) to tag based on actual attendance:
- Attended Day 1: tag `ws01-day1-attended`
- Attended Day 2: tag `ws01-day2-attended`
- Missed both: tag `ws01-no-show` → trigger refund offer email

---

## 7. Webhook Integration (the magic)

When a contact registers, GHL fires a webhook to export their data to a shared CSV / Airtable / Notion doc Danny can run `/prep-workshop-slides` against 24 hours before Day 1.

### Webhook configuration

| Setting | Value |
|---------|-------|
| Trigger | Payment succeeds for Workshop 01 |
| Method | POST |
| URL | `https://YOUR_ENDPOINT/workshop-01-attendees` (see options below) |
| Payload (JSON) | `{ "first_name": "{{first_name}}", "last_name": "{{last_name}}", "email": "{{email}}", "linkedin_url": "{{contact.linkedin_url}}", "business_stage": "{{contact.business_stage}}", "registered_at": "{{timestamp}}" }` |
| Authentication | Bearer token in header (GHL supports this) |

### Where the webhook should POST to (pick one)

| Option | URL pattern | Effort | When to use |
|--------|------------|--------|-------------|
| **Google Sheet via Zapier** | Zapier webhook URL | 10 min | If you already have Zapier. Rows append to a Sheet. |
| **Airtable via webhook** | Airtable's native webhook | 15 min | Better for structured data + views |
| **Notion via Zapier** | Zapier to Notion DB | 10 min | If the team lives in Notion |
| **Direct to `attendees.csv` in repo** | GitHub Action webhook | 45 min | Full automation — CSV commits to repo, `/prep-workshop-slides` reads from there |

**Recommendation:** start with **Zapier → Google Sheet** (10 min). Danny downloads the CSV 24h before Day 1 and runs `/prep-workshop-slides attendees.csv`.

---

## 8. Tags & Custom Fields

### Custom fields to add on Contact

| Field name | Type | Purpose |
|-----------|------|---------|
| `linkedin_url` | URL | Powers `/prep-workshop-slides` |
| `business_stage` | dropdown | Pre-workshop segmentation |
| `pre_workshop_question` | long text | Fuel for Day 1 Q&A |
| `workshop_01_shipped_post_url` | URL | From Day 1 Activity 3, populated by webhook after `/ship-it-live` |
| `workshop_01_brain_rendered` | boolean | Set by webhook on Day 2 |
| `committed_engine` | text | Which engine they committed to run unattended |

### Tags to use for segmentation

| Tag | Applied when |
|-----|-------------|
| `workshop-01-registered` | On payment success |
| `ws01-day1-attended` | Via Zoom integration |
| `ws01-day2-attended` | Via Zoom integration |
| `ws01-shipped-post` | On Day 1 Activity 3 webhook |
| `ws01-brain-rendered` | On Day 2 Brain render webhook |
| `workshop-01-completed` | Both days attended |
| `ws01-no-show` | Missed both days |
| `cohort-waitlist` | Clicked cohort CTA |

---

## 9. Post-Workshop Follow-Up (Day +7 check-in)

### Email 7 — Day 7 Check-in

**Trigger:** May 10, 10am Finland (7 days after Day 2)
**Subject:** How's your engine running?

```
{{first_name}},

Day 7. You committed to running {{committed_engine}} unattended this week.

How did it go?

Reply with:
- Output or screenshot
- One thing that worked
- One thing that broke

The Cohort (June 2026 intake) is where we fix what's breaking for everyone at once. Waitlist: [COHORT_URL]

If you're already dialled in, reply anyway. I'll feature the best 3 on LinkedIn.

— Daniel
```

---

## 10. Pre-Launch QA Checklist

Test before opening registration publicly:

- [ ] Stripe test payment runs through successfully ($0.50 test mode)
- [ ] Confirmation email arrives within 60 seconds
- [ ] Calendar invite attaches correctly (Google + Outlook tested)
- [ ] Webhook fires + populates Google Sheet / Airtable
- [ ] LinkedIn URL field validates properly
- [ ] Refund flow works (admin-triggered manual refund)
- [ ] Drip sequence schedules correctly (test with a future-dated purchase)
- [ ] Mobile form renders cleanly (iPhone + Android)
- [ ] Thank-you page loads with Zoom link visible
- [ ] All email links work (Zoom, pre-setup video, cohort URL)
- [ ] Personalized merge fields pull correctly ({{first_name}} not blank)

---

## 11. Launch-Day Operations

**On May 1 (registration closes):**
- [ ] Set funnel to `inactive` or show "Workshop full — join Workshop 02 waitlist"
- [ ] Export final attendee list from GHL → CSV
- [ ] Run `/prep-workshop-slides attendees.csv` in Claude Code (see `commands/prep-workshop-slides.md`)
- [ ] Review generated slides — flag any with weak "observations"
- [ ] Backup: push rendered slides to a shared Drive folder

**Morning of May 2:**
- [ ] Send SMS reminders via GHL to any contact with phone number
- [ ] Open Zoom 20 min early for tech check
- [ ] Pin the Slack cohort invite in email template
- [ ] Have `attendee-slides/index.html` full-screen on second monitor
- [ ] Backup: pre-recorded demo videos queued in case Claude API stutters

---

## 12. Reporting Dashboard (in GHL)

Build a quick dashboard widget for:
- Registrations today / this week
- Revenue today / this week
- Attendance rate (registered vs. attended both days)
- Cohort waitlist conversions
- Post-workshop LinkedIn post URLs (from the `ws01-shipped-post` tag)

---

## 13. What the Landing Page Needs From You

Once the GHL funnel is live, Danny needs **one URL** to paste into the landing page:

```
GHL Funnel URL: https://_________________________________
```

Once pasted, every "Reserve my seat · $49" button on `purely-personal-workshop.vercel.app` will route to GHL, and the rest of this spec runs automatically.

---

## 14. Duplicate This for Workshop 02

Every field above has an implicit `Workshop 01` scope. When Workshop 02 opens:

1. Duplicate the funnel: `Workshop 02 · [new dates]`
2. Update tags from `workshop-01-*` to `workshop-02-*`
3. Update email dates in the drip sequence
4. Update product name + keep price
5. Update the webhook URL if using a different sheet

Everything else stays. The funnel is reusable infrastructure.

---

## 15. Questions for the GHL Specialist to Answer Back

Before building, confirm with Danny:

1. Do you already have Stripe connected in GHL? (If not, 15-min setup)
2. Do you want SMS reminders? (Requires a GHL phone number + budget for SMS)
3. Do you want attendance tracking via Zoom integration? (Requires Zoom Business plan)
4. Do you want the webhook to go to Zapier → Google Sheet, or somewhere else?
5. What's the custom domain you want for the funnel? (e.g., `go.purelypersonal.ai` vs. default `*.gohighlevel.com`)

---

## Effort Estimate

| Phase | Time |
|-------|------|
| Build funnel + checkout + thank-you page | 45 min |
| Configure Stripe product + test payment | 15 min |
| Create custom fields + tags | 15 min |
| Build 7 email templates | 40 min |
| Build automation workflow | 30 min |
| Configure webhook + test with Zapier/Sheet | 15 min |
| QA checklist (§10) | 20 min |
| **Total first-time build** | **~3 hours** |
| **Total duplicate for Workshop 02+** | **~30 min** |

---

## One-Line Handoff to Your GHL Specialist

> *"Here's the 15-section build spec for Workshop 01. Follow it in order. All 7 email copies are pre-written. Ping me when you finish §10 (QA) and I'll stress-test it with a real $49 payment before we open registration."*

---

**Spec owner:** Daniel Paul
**Last updated:** Apr 21, 2026
**Related files:**
- `landing-page/index.html` — live at [purely-personal-workshop.vercel.app](https://purely-personal-workshop.vercel.app)
- `commands/prep-workshop-slides.md` — consumes the webhook CSV
- `workshop/mind-blown-activities.md` — what the attendees experience after registering
