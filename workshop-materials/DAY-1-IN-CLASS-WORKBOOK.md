# DAY 1 · IN-CLASS WORKBOOK
## Build a Business That Runs By Itself · Saturday May 2, 2026

```
┌────────────────────────────────────────────────────────────────┐
│  DURATION    11:00 - 13:00 Finland (UTC+3)                     │
│  FORMAT      Live Zoom · Cameras ON · Claude Code OPEN         │
│  YOUR JOB    Fill this workbook · Paste prompts · Show output  │
│  RESULT      By 13:00 you will have run 2 routines + week map  │
└────────────────────────────────────────────────────────────────┘
```

---

## ✍ YOUR DETAILS · fill before we start

```
NAME:           ______________________________________________

WHAT I DO:      ______________________________________________

WHO I SERVE:    ______________________________________________

#1 BOTTLENECK:  ______________________________________________
                (the part of your business that drains you most)

ZOOM HANDLE:    ______________________________________________
                (so I can call on you by name)
```

---

## ⚡ PRE-FLIGHT CHECK · 10:45 - 11:00

Before the workshop starts · run these 3 checks in your terminal.

### ☐ Check 1 · Claude Code is installed

```
┌─────────────────────────────────────────┐
│  PASTE THIS in your terminal:           │
│                                         │
│  claude --version                       │
│                                         │
└─────────────────────────────────────────┘
```

▸ Should print something like `1.0.x` or higher
▸ If "command not found" → re-open terminal, then `source ~/.zshrc` (Mac) or restart PowerShell (Windows)

```
WHAT YOU SAW: ___________________________________________
```

### ☐ Check 2 · Plugin is loaded

```
┌─────────────────────────────────────────┐
│  PASTE THIS in your terminal:           │
│                                         │
│  claude                                 │
│                                         │
└─────────────────────────────────────────┘
```

Then once Claude Code opens, type `/purely-personal:` and watch autocomplete.

▸ You should see 9 commands appear: `build-my-brain`, `marketing-engine`, `sales-engine`, `operations-engine`, `cash-engine`, `leadership-engine`, `prep-workshop-slides`, `ship-it-live`, `new-workshop`

▸ If nothing appears → type `/exit` then re-launch with `claude` (plugins only load at startup)

```
HOW MANY COMMANDS APPEARED?  _____ / 9
```

### ☐ Check 3 · BUSINESS-BRAIN.md is filled

```
┌─────────────────────────────────────────┐
│  PASTE THIS in Claude Code:             │
│                                         │
│  read BUSINESS-BRAIN.md and tell me     │
│  which sections are still empty         │
│                                         │
└─────────────────────────────────────────┘
```

▸ Claude lists empty sections
▸ If sections 4 (Voice) or 5 (ICP) are empty → STOP · run `/purely-personal:build-my-brain` first

```
SECTIONS STILL EMPTY: ___________________________________
```

```
═══════════════════════════════════════════════════════════
  ✅ Pre-flight pass    ☐ Yes    ☐ No (raise hand in Zoom)
═══════════════════════════════════════════════════════════
```

---

# ACTIVITY 1 · YOUR FIRST CONTENT DROP
## ⏰ 11:20 - 11:35 (15 minutes)

```
┌────────────────────────────────────────────────────────────────┐
│  GOAL    Generate 3 LinkedIn posts in YOUR voice               │
│  TOOL    /purely-personal:marketing-engine                     │
│  WIN     One post good enough to publish today                 │
└────────────────────────────────────────────────────────────────┘
```

### Step 1.1 · Set the topic

What's ONE thing you've learned this week that your audience needs?

```
TOPIC: ________________________________________________________

       ________________________________________________________

       ________________________________________________________

(One sentence is enough · Claude expands it)
```

### Step 1.2 · Run marketing-engine

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   PASTE THIS into Claude Code:                                ║
║                                                               ║
║   /purely-personal:marketing-engine                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

▸ Claude will ask "what's the topic?" → paste your topic from Step 1.1
▸ Claude reads your voice corpus (5 LinkedIn posts) before writing
▸ Wait 30-60 seconds · 3 posts will appear

### Step 1.3 · Score the output

For each post Claude generated, fill this in:

```
─────────────────────────────────────
POST 1 · HOOK:
___________________________________________________________

Sounds like me?           ☐ YES   ☐ NO   ☐ MEH
Would I publish this?     ☐ YES   ☐ NO   ☐ EDIT FIRST
What ONE word feels off?  ___________________________

─────────────────────────────────────
POST 2 · HOOK:
___________________________________________________________

Sounds like me?           ☐ YES   ☐ NO   ☐ MEH
Would I publish this?     ☐ YES   ☐ NO   ☐ EDIT FIRST
What ONE word feels off?  ___________________________

─────────────────────────────────────
POST 3 · HOOK:
___________________________________________________________

Sounds like me?           ☐ YES   ☐ NO   ☐ MEH
Would I publish this?     ☐ YES   ☐ NO   ☐ EDIT FIRST
What ONE word feels off?  ___________________________
─────────────────────────────────────
```

### Step 1.4 · Pick your champion

```
WINNING POST:    ☐ #1    ☐ #2    ☐ #3

WHY IT WORKS:  __________________________________________

               __________________________________________
```

### Step 1.5 · Tighten + ship

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   PASTE THIS into Claude Code:                                ║
║                                                               ║
║   take post #[YOUR PICK] · tighten the hook · cut 20%         ║
║   words · keep my voice                                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

```
☐ Copied final post to LinkedIn
☐ Scheduled for tomorrow 7am (or published now)
☐ Saved to /content-bank/2026-05-02.md
```

### 🔧 TROUBLESHOOTING · Activity 1

| What went wrong | Quick fix |
|---|---|
| Posts sound like generic AI | Voice corpus empty → paste 3 of your real LinkedIn posts into `frameworks/marketing/linkedin-voice-examples/` and re-run |
| Hook is weak | Paste: `make the hook more visceral · pattern interrupt · no buzzwords` |
| Too long for LinkedIn | Paste: `cut to 1300 characters · keep the punch line` |
| Banned phrases appearing | Paste: `re-read VOICE-SIGNATURE.md · remove banned phrases · keep meaning` |

```
═══════════════════════════════════════════════════════════
  ☐ ACTIVITY 1 COMPLETE · 1 post ready to publish
═══════════════════════════════════════════════════════════
```

---

# ACTIVITY 2 · YOUR FIRST 10 LEADS
## ⏰ 11:40 - 12:00 (20 minutes)

```
┌────────────────────────────────────────────────────────────────┐
│  GOAL    10 prospects researched · BANT-scored · 3 outreached │
│  TOOL    /purely-personal:sales-engine                         │
│  WIN     3 personalized outreach drafts ready to send          │
└────────────────────────────────────────────────────────────────┘
```

### Step 2.1 · Define your ICP filter

Who are you looking for? Be specific.

```
ROLE / TITLE:        ______________________________________

INDUSTRY:            ______________________________________

COMPANY SIZE:        ______________________________________

LOCATION:            ______________________________________

SIGNAL TO SCRAPE:    ______________________________________
                     (e.g. "posted about AI hiring in last 30 days"
                       or "hiring a marketer right now"
                       or "raised seed in last 6 months")
```

### Step 2.2 · Run sales-engine

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   PASTE THIS into Claude Code:                                ║
║                                                               ║
║   /purely-personal:sales-engine                               ║
║                                                               ║
║   then when prompted, paste your ICP filter from Step 2.1     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

▸ Claude scrapes via Apify (free tier · ~30-60 seconds)
▸ Returns 10 prospects with: name, title, company, signal, fit-score (0-10)
▸ BANT-scores each (Budget · Authority · Need · Timing)

### Step 2.3 · Pick your top 3

Fill in the 3 highest-scoring prospects Claude returned:

```
─────────────────────────────────────
PROSPECT 1
NAME:        _______________________________________________
TITLE/CO:    _______________________________________________
SIGNAL:      _______________________________________________
BANT SCORE:  ___ / 40
─────────────────────────────────────
PROSPECT 2
NAME:        _______________________________________________
TITLE/CO:    _______________________________________________
SIGNAL:      _______________________________________________
BANT SCORE:  ___ / 40
─────────────────────────────────────
PROSPECT 3
NAME:        _______________________________________________
TITLE/CO:    _______________________________________________
SIGNAL:      _______________________________________________
BANT SCORE:  ___ / 40
─────────────────────────────────────
```

### Step 2.4 · Generate outreach

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   PASTE THIS into Claude Code:                                ║
║                                                               ║
║   draft a 3-step outreach sequence for prospect #1            ║
║   · LinkedIn connection note (300 chars)                      ║
║   · email follow-up day 3 (150 words)                         ║
║   · breakup message day 7 (50 words)                          ║
║   tone: my voice from VOICE-SIGNATURE.md                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

▸ Repeat for prospects #2 and #3 (change the number)

### Step 2.5 · Score + ship

```
For each prospect, mark:

PROSPECT 1   ☐ Connection sent on LinkedIn
             ☐ Email queued in Gmail draft
             ☐ Day 7 reminder set in Calendar

PROSPECT 2   ☐ Connection sent on LinkedIn
             ☐ Email queued in Gmail draft
             ☐ Day 7 reminder set in Calendar

PROSPECT 3   ☐ Connection sent on LinkedIn
             ☐ Email queued in Gmail draft
             ☐ Day 7 reminder set in Calendar
```

### 🔧 TROUBLESHOOTING · Activity 2

| What went wrong | Quick fix |
|---|---|
| "I don't have access to Apify" | Restart Claude Desktop fully (Cmd+Q on Mac) · re-run |
| Apify free credits exhausted | Drop to 5 prospects: paste `re-run with limit 5 prospects` |
| All 10 are bad fit | Tighten the signal in Step 2.1 · paste: `re-run with stricter filter: [add criteria]` |
| Outreach feels generic | Paste: `add the specific signal from their LinkedIn into line 1 of every message` |

```
═══════════════════════════════════════════════════════════
  ☐ ACTIVITY 2 COMPLETE · 3 outreaches queued
═══════════════════════════════════════════════════════════
```

---

# ACTIVITY 3 · MAP YOUR WEEK
## ⏰ 12:05 - 12:25 (20 minutes)

```
┌────────────────────────────────────────────────────────────────┐
│  GOAL    Lock 6 routines into your calendar · 4 hrs/wk total  │
│  TOOL    Google Calendar (manually · one-time setup)           │
│  WIN     Monday 7am alarm set + Sunday 6pm alarm set           │
└────────────────────────────────────────────────────────────────┘
```

### Step 3.1 · The 6 weekly anchors

Copy each into your calendar with a recurring alarm:

```
┌──────────────────────────────────────────────────────────────┐
│  DAY    TIME      ROUTINE              COMMAND               │
├──────────────────────────────────────────────────────────────┤
│  MON    7:00am    Content Drop         marketing-engine      │
│  TUE    8:00am    Lead Research        sales-engine          │
│  WED    8:00am    Newsletter Draft     marketing-engine      │
│  THU    7:00am    Meeting Prep         sales-engine          │
│  FRI    5:00pm    Weekly Wrap          operations-engine     │
│  SUN    6:00pm    Pipeline Report      sales-engine          │
└──────────────────────────────────────────────────────────────┘

Each takes 4-7 min · YOU review + approve · Claude writes everything
```

### Step 3.2 · Set the alarms NOW

```
☐ MON 7:00am · /purely-personal:marketing-engine          (recurring)
☐ TUE 8:00am · /purely-personal:sales-engine              (recurring)
☐ WED 8:00am · /purely-personal:marketing-engine          (recurring)
☐ THU 7:00am · /purely-personal:sales-engine              (recurring)
☐ FRI 5:00pm · /purely-personal:operations-engine         (recurring)
☐ SUN 6:00pm · /purely-personal:sales-engine              (recurring)

⚠ THE COMMAND IS THE TITLE · so when the alarm fires you know what to paste
```

### Step 3.3 · Block your "do not disturb" windows

```
DEEP WORK WINDOW 1:    Day _________  Time __________ - __________

DEEP WORK WINDOW 2:    Day _________  Time __________ - __________

DEEP WORK WINDOW 3:    Day _________  Time __________ - __________
```

### Step 3.4 · The screenshot proof

```
☐ Screenshot of the week view (showing all 6 routines)
☐ Drop into Zoom chat
☐ I'll react ✅ as I see them come in
```

```
═══════════════════════════════════════════════════════════
  ☐ ACTIVITY 3 COMPLETE · Week is mapped
═══════════════════════════════════════════════════════════
```

---

# ACTIVITY 4 · MONDAY 7AM ANCHOR
## ⏰ 12:30 - 12:50 (20 minutes)

```
┌────────────────────────────────────────────────────────────────┐
│  GOAL    Run Monday 7am routine RIGHT NOW · prove the loop    │
│  TOOL    /purely-personal:leadership-engine                    │
│  WIN     You see the morning brief format · know what's next  │
└────────────────────────────────────────────────────────────────┘
```

### Step 4.1 · Run the morning brief

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   PASTE THIS into Claude Code:                                ║
║                                                               ║
║   /purely-personal:leadership-engine                          ║
║                                                               ║
║   simulate Monday 7am · pull from all 5 engines               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

▸ Returns a 60-second-read brief with: yesterday's wins, today's #1 priority, blockers, money in/out, content ready to ship

### Step 4.2 · The 60-second read

What did the brief tell you? Fill in:

```
🏆 YESTERDAY'S BIGGEST WIN:
___________________________________________________________

⚡ TODAY'S #1 PRIORITY:
___________________________________________________________

🚨 BIGGEST BLOCKER:
___________________________________________________________

💰 MONEY IN (week):  $ ____________

💸 MONEY OUT (week): $ ____________

📤 CONTENT READY TO SHIP:  ___ pieces
```

### Step 4.3 · The "is this useful?" gut check

```
If I got this brief every Monday at 7am · would my week be better?

☐ YES · clearly
☐ MAYBE · need to tune what's in it
☐ NO · this isn't useful

If MAYBE or NO · paste:

  ╔═══════════════════════════════════════════════════════════╗
  ║                                                           ║
  ║   change the brief to include: ___________________        ║
  ║                                                           ║
  ║   remove from the brief: _________________________        ║
  ║                                                           ║
  ╚═══════════════════════════════════════════════════════════╝
```

```
═══════════════════════════════════════════════════════════
  ☐ ACTIVITY 4 COMPLETE · Monday loop proven
═══════════════════════════════════════════════════════════
```

---

# DAY 1 COMMITMENTS · 12:55 - 13:00

By tomorrow's session, I commit to:

```
1. PUBLISH the LinkedIn post from Activity 1.

   Will publish on:  ____________________ (date · time)


2. SEND the 3 outreach messages from Activity 2.

   Will send by:     ____________________ (date · time)


3. RUN Monday 7am morning brief for real.

   Alarm set:        ☐ YES   ☐ NO


SIGNED: _______________________      DATE: ____________________
```

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  📸 SCREENSHOT THIS PAGE → DROP IN ZOOM CHAT                   │
│                                                                │
│  This is your accountability proof.                            │
│  Tomorrow we open Day 2 by reading these out loud.             │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎯 DAY 1 SCORECARD

```
ACTIVITY 1   ☐ Marketing engine ran      ☐ 1 post ready to publish
ACTIVITY 2   ☐ Sales engine ran          ☐ 3 outreaches queued
ACTIVITY 3   ☐ 6 routines on calendar    ☐ Screenshot in chat
ACTIVITY 4   ☐ Leadership engine ran     ☐ Brief makes sense

──────────────────────────────────────────────────────────────
SCORE: ___ / 8 boxes ticked

7-8 = You're shipping tomorrow.
5-6 = Catch up tonight (60 min)
0-4 = DM Danny tonight · we troubleshoot before Day 2
──────────────────────────────────────────────────────────────
```

---

## 📚 BEFORE DAY 2 · Optional (15 min)

▸ Read `frameworks/marketing/linkedin-hooks.md` (7 hook archetypes)
▸ Skim `frameworks/sales/grand-slam-offer.md` (4-lever offer construction)
▸ Glance at `frameworks/operations/sop-pattern.md` (the SOP template ops-engine uses)

```
─── END OF DAY 1 ─── See you tomorrow at 11:00 Finland ───
```
