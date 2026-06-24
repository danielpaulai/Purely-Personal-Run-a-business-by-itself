# AI Employee Bootcamp Plugin
## Purely Personal · by Daniel Paul
### Complete Plugin Architecture, Updated June 2026

---

## WHAT THIS PLUGIN IS

One brain. Five executives. Real work, on a schedule.

Install once. Your AI team runs on a schedule, drafting posts, finding prospects, briefing your morning, reporting your revenue, while you sleep.

---

## THE STRUCTURE

```
Layer 1, Your Brain
  Your Business Brain folder (7 foundation documents)
  Everything downstream reads from this.

Layer 2, The Build Room
  /matchmaker    → audits skills against your foundation
  /tailor        → customises skills to your specific business
  /build-your-own-employee → builds new employees from scratch

Layer 3, The AI CEO
  /ceo           → orchestrates all executives, one answer

Layer 4, The Executives
  /cmo-daily-post        → Marketing (daily post, hooks, pinned comments)
  /cro-weekly-prospects  → Sales (10 prospects, sequences, pipeline review)
  /coo-morning-brief     → Operations (calendar, inbox, tasks, content)
  /cfo-weekly-revenue    → Finance (revenue, pipeline, unpaid invoices)

Layer 5, The Skills (wired to executives)
  CMO skills:
    /linkedin-caption-writer     → posts in participant's voice
    /content-strategy            → content pillars and positioning
    /content-pillars-extractor   → builds 3–5 content territories
    /content-calendar-generator  → 30-day posting calendar
    /batch-writing-sequencer     → timed batch writing session plan
    /newsletter-writer           → weekly email in participant's voice

  CRO skills:
    /outreach-prospector         → full intelligence brief per prospect
    /outreach-writer             → 5-message sequence per prospect
    /outreach-closer             → conversation diagnosis + next message
    /outreach-reactivator        → re-engage gone-quiet or cold leads
    /deal-tracker                → pipeline triage + next-action plan
    /sales-call-prep             → discovery call brief + objection scripts
    /dm-sequence-writer          → standalone DM sequences

Layer 6, Connectors
  Gmail · Google Calendar · Notion · Apify · Google Drive · Canva · Publisher
```

---

## EXECUTIVES AND THEIR SKILLS

### CMO, Marketing
**Runs:** Daily (weekdays, 7:30 AM)
**Skills wired:**
- `linkedin-caption-writer`, writes the post
- `content-pillars-extractor`, knows what territory to post in
- `content-calendar-generator`, knows which slot to fill today
- `batch-writing-sequencer`, for weekly batch sessions
- Hook generator (embedded in CMO skill)
- Pinned comment writer (embedded in CMO skill)

### CRO, Sales
**Runs:** Every Monday (8:00 AM)
**Skills wired:**
- `outreach-prospector`, intelligence brief per prospect
- `outreach-writer`, 5-message sequence per prospect
- `outreach-closer`, diagnoses active conversations
- `outreach-reactivator`, re-engages cold leads
- `deal-tracker`, weekly pipeline triage
- `sales-call-prep`, pre-call brief for booked calls

### COO, Operations
**Runs:** Daily (weekdays, 7:00 AM)
**Connectors used:** Notion · Gmail · Google Calendar
**Output:** Branded HTML morning brief

### CFO, Finance
**Runs:** Every Friday (6:00 PM)
**Connectors used:** Notion · Gmail
**Output:** HTML revenue dashboard

---

## THE 5 RECOMMENDED ROUTINES

### Routine 1, COO Morning Brief
```
Name: COO Morning Brief
Schedule: Weekdays at 7:00 AM
Instructions: Run the COO morning brief. Pull from Notion, Gmail, and Google Calendar. 
Output as HTML using my brand colors from my documents. Save the file. 
Then create a Gmail draft with the subject "Morning Brief – [Today's Date]" 
and paste the brief content into the email body.
Folder: [My Business Brain] or [GitHub repo]
```

### Routine 2, CMO Daily Post
```
Name: CMO Daily Post
Schedule: Weekdays at 7:30 AM
Instructions: Run the CMO daily post skill. Check my 30-day content calendar for today's 
slot. Generate 5 hooks, write the post in my voice using my Voice DNA document. 
Score it on the Invisibility Diagnostic. Then create a Gmail draft with subject 
"LinkedIn Post Draft – [Today's Date]" containing the scored post.
Folder: [My Business Brain] or [GitHub repo]
```

### Routine 3, CRO Weekly Prospects
```
Name: CRO Weekly Prospects
Schedule: Mondays at 8:00 AM
Instructions: Run the CRO weekly prospects skill. Find 10 qualified LinkedIn prospects 
matching my ICP using Apify. Run a full intelligence brief on each. For each one, draft 
a personalised 5-message DM sequence in my voice. Output as an HTML prospect pack. 
Then create a Gmail draft with subject "Weekly Prospect List – [Date]".
Folder: [My Business Brain] or [GitHub repo]
```

### Routine 4, CFO Weekly Revenue
```
Name: CFO Weekly Revenue
Schedule: Fridays at 6:00 PM
Instructions: Run the CFO weekly revenue skill. Summarise this week's revenue activity, 
pipeline movement, and any unpaid invoices. Flag anything that needs my attention. 
Output as a clean HTML dashboard. Then create a Gmail draft with subject 
"Weekly Revenue Report – [Week of Date]".
Folder: [My Business Brain] or [GitHub repo]
```

### Routine 5, Content Planning
```
Name: Weekly Content Planning
Schedule: Sundays at 9:00 AM
Instructions: Run the content-pillars-extractor to review my content territories, 
then run the content-calendar-generator to plan next week's posts. 
Output as an HTML content calendar. Then create a Gmail draft with subject 
"Content Plan – Week of [Date]".
Folder: [My Business Brain] or [GitHub repo]
```

---

## SKILL COUNT

| Category | Skills |
|----------|--------|
| Executive layer | 5 (CEO, CMO, CRO, COO, CFO) |
| Content skills | 6 (caption writer, content strategy, pillars, calendar, batch, newsletter) |
| Sales skills | 7 (prospector, outreach writer, closer, reactivator, deal tracker, call prep, DM writer) |
| Build tools | 3 (matchmaker, tailor, build-your-own) |
| **Total** | **21 skills** |

---

## REQUIRED FOUNDATION DOCUMENTS

Before running any skill, the participant's Business Brain folder must contain:

### Personal Authority Foundation
- `personal-story-[name].md`
- `voice-dna-[name].md`

### Business Authority Foundation
- `icp-[name].md`
- `messaging-[name].md`
- `rule1-[name].md`
- `positioning-[name].md`
- `inbox-[name].md`

---

*AI Employee Bootcamp · Purely Personal · by Daniel Paul · Updated June 2026*
