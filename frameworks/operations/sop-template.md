# SOP Template · Trigger · Inputs · Steps · Outputs · QC

> The 5-section template that turns any repeated task into a system.
> If you do something twice, write the SOP. If you do it three times
> and haven't · you're the bottleneck.

---

## When to write an SOP

You should write an SOP when:

1. You'll do this task **3+ times**
2. The task takes **5+ minutes** each time
3. The task has **fixed steps** (not 100% improvisation)
4. Someone ELSE could potentially do it (now or later)

If all 4 are true · write the SOP. The 30 min you spend writing it
saves 30 hours over the next year.

---

## The 5-section template

```
1 · TRIGGER     ·  what initiates this SOP?
2 · INPUTS      ·  what data / files / access is needed?
3 · STEPS       ·  the actual procedure (numbered)
4 · OUTPUTS     ·  what does success look like?
5 · QC          ·  how do we verify it worked?
```

---

## Section 1 · TRIGGER

**The question:** "When does this SOP get run?"

**Bad triggers:**
- "Whenever needed"
- "When I think about it"
- "Sometimes"

**Good triggers:**
- "Every Monday at 7am"
- "When a new client signs up"
- "When inbox count exceeds 50 unread"
- "When Stripe MRR drops below $10K"
- "When a sales call is booked for tomorrow"

A good trigger is **observable, specific, and automatable.** If a
human (or an engine) can tell whether the trigger fired · the SOP
will run reliably.

---

## Section 2 · INPUTS

**The question:** "What does the person running this SOP need to
have BEFORE they start?"

**Categories of inputs:**
- **Data:** numbers, files, customer info, API keys
- **Access:** logins, permissions, tools open
- **Time:** how long does this take? (block it on calendar)
- **Decisions:** what choices need to be pre-made?

**Example for /marketing-engine SOP:**

```
INPUTS:
- Access to Claude Code on your laptop
- BUSINESS-BRAIN.md filled out (specifically: voice section, ICP)
- Notion connected · content calendar database exists
- Gmail connected · last 7 days readable
- Topic for the week (or let engine pick from positioning gaps)
- 4-10 minutes blocked on calendar
```

If any input is missing · the SOP fails. Before the steps even
start, validate inputs.

---

## Section 3 · STEPS

**The question:** "What does the person actually DO, in order?"

**Rules for writing steps:**
- Each step is ONE atomic action
- Use action verbs (open, paste, run, save, review, send)
- Number them
- Include "wait for X" when needed (don't move on until X happens)
- Specify the destination/output of each step

**Bad steps:**
- "Set up the marketing thing"  (too vague)
- "Do the engine"  (not atomic)

**Good steps:**

```
STEPS:
1 · Open Claude Code in your terminal
2 · Navigate to your business folder · `cd ~/Desktop/my-business`
3 · Type `/marketing-engine` and press Enter
4 · Wait for the engine to ask for a topic
5 · Type your topic (or "let me pick" to have it suggest)
6 · Wait ~90 seconds while the engine runs
7 · Review the 3 LinkedIn variants displayed
8 · Pick the best variant by typing the variant number
9 · Verify the engine saved to Notion content calendar
10 · Verify the newsletter idea was queued for Wednesday
```

10 steps. Each one specific. A new person could run this without
asking you a question.

---

## Section 4 · OUTPUTS

**The question:** "What does success look like? How do you know it's
done?"

Outputs are the **artifacts** that exist after the SOP runs. Not the
process · the deliverables.

**Example:**

```
OUTPUTS:
- 3 LinkedIn posts saved in Notion · Content Calendar
- 1 newsletter idea queued for Wednesday
- Notion records timestamped + voice-validated
- Calendar reminder set for Tuesday: "review + post"
- Drive backup of post drafts saved
```

Outputs are observable. You can SEE them. You can verify them.

If an SOP doesn't have clearly defined outputs · you can't tell when
it's done.

---

## Section 5 · QC (Quality Check)

**The question:** "How do we know the OUTPUT was actually good?"

QC is the difference between "did the task get done" (steps
completed) and "did the task get done WELL" (output is high-quality).

**QC checklist for /marketing-engine output:**

```
QC:
- [ ] Each post is 150-350 words
- [ ] Each post has a hook in the first 210 characters
- [ ] No em-dashes or banned phrases (validate_voice ran)
- [ ] Each post has ONE CTA (not 0, not 3)
- [ ] Newsletter idea is specific enough to write Wednesday
- [ ] All 3 posts use DIFFERENT hook archetypes
- [ ] Voice score against BRAIN > 80/100
```

QC items should be:
- **Observable** (you can see if they pass/fail)
- **Binary** (yes/no, not "kinda")
- **Independent** of the steps (testing the output, not the process)

---

## Worked example · the full SOP

### SOP: Monday Content Drop

```
TRIGGER:
Every Monday at 7:00 AM (calendar reminder fires)
OR when called manually via /marketing-engine

INPUTS:
- BUSINESS-BRAIN.md filled in (Voice + ICP minimum)
- Notion connected (content calendar database exists)
- Gmail connected (last 7 days readable)
- Topic for the week (or "let engine pick")
- 4-10 min calendar block

STEPS:
1 · Open Claude Code in business folder
2 · Type /marketing-engine
3 · Wait for topic prompt · provide topic or "let me pick"
4 · Wait for 3 LinkedIn variants (~90s)
5 · Review variants · pick best by typing number
6 · Engine writes to Notion · verify entry
7 · Engine queues newsletter idea for Wednesday · verify
8 · Engine validates voice · review any flags
9 · Set Tuesday calendar reminder: "review + post"

OUTPUTS:
- 3 LinkedIn posts in Notion content calendar (timestamped)
- 1 newsletter idea queued for Wednesday
- Voice validation report (saved to Drive)
- Tuesday review reminder set

QC:
- [ ] All 3 posts 150-350 words
- [ ] All 3 hooks within 210 chars
- [ ] Different archetypes used per post
- [ ] Zero em-dashes / banned phrases
- [ ] One CTA per post
- [ ] Newsletter idea specific (not generic topic)
- [ ] Voice score > 80/100
- [ ] Notion entry saved correctly

ESCALATION (when QC fails):
- Voice score < 80: re-run with more BRAIN context
- Hook too long: regenerate with shorter constraint
- Generic newsletter idea: prompt engine to add specifics
```

That SOP, copied into Notion · runs forever. Anyone (or the engine)
can execute it without asking you a question.

---

## SOP storage and discovery

**Where SOPs live:**
- `purely-personal/sops/` directory (text-based, version-controlled)
- Notion · "SOPs" database (linked to Areas)
- Notion auto-generates from /operations-engine

**Naming convention:**
- `[area]-[verb]-[outcome].md`
- Examples:
  - `marketing-write-monday-content-drop.md`
  - `sales-research-tuesday-prospects.md`
  - `cash-pull-friday-stripe-numbers.md`

**Discovery:**
- Index page · table of contents by area
- Each Area in PARA links to its SOPs
- Search-friendly · use clear titles

---

## How to write SOPs FAST

The 5-minute SOP method:

1. **Run the task ONCE while recording yourself** (Loom or screen
   recording)
2. **Watch the recording back at 1.5x**
3. **Pause every 30 seconds and write down the step you just took**
4. **Group steps into TRIGGER / INPUTS / STEPS / OUTPUTS / QC**
5. **Edit pass for clarity (5 min)**

Total time: 25-35 min for a 5-min task that you'll run 50+ times.
ROI is massive.

---

## SOPs don't have to be perfect

SOP v1 is always rough. Run it 3 times. Update it. By v3 it's stable.

The biggest mistake: trying to write the perfect SOP before
publishing it. Ship a rough one. Use it. Improve it as you go.

---

## Apply it to /operations-engine

The /operations-engine has a built-in SOP-generator behavior. When it
detects you've answered the SAME question 3 times in your inbox · it
auto-generates an SOP from your responses.

The generated SOP follows the 5-section template:
- TRIGGER · the question pattern that prompted you
- INPUTS · what context you typically pulled in to answer
- STEPS · your actual response steps
- OUTPUTS · the artifact (the email reply, the Notion entry)
- QC · what makes a good response vs a generic one

The SOP is then:
- Saved to `purely-personal/sops/`
- Linked from BUSINESS-BRAIN.md § Operations area
- Available to the engine for future auto-responses

---

## The SOP audit (run quarterly)

Every 90 days, review your SOPs:

```
[ ] How many SOPs exist?
[ ] How many are actively used?
[ ] How many are stale (haven't run in 60 days)?
[ ] What new repeated tasks DON'T have SOPs yet?
[ ] What SOPs could be merged or simplified?
[ ] What SOPs could be automated entirely?
```

The goal isn't to maximize SOP count. The goal is to maximize SOP
LEVERAGE · how many tasks run reliably without you.
