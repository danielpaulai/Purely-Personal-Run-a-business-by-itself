---
name: email-month
description: The hero skill. Plans and writes next month's emails in one go: 4 weeks from the cadence and the member's weekly promise, about 10 emails across the five Email Room recipes (client win, story, 9-word, how-to, event invite) built only from their ideas.md, proof bank and story bank, each rated by the separate rater up to a 10, saved as Email/months/<YYYY-MM>/ with one file per email plus calendar.md, then rendered as an inbox preview. Trigger on "write next month's emails", "write my emails for November", "plan my month of emails", "a month of emails", "fill my email calendar", "next 4 weeks of emails". Say "quick draft" to skip the rating.
---

# A month of emails

This is the skill members use most. It must feel like sitting down with a good editor who already knows their business: three quick questions, then a finished month they can read, fill in and schedule in one sitting.

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first, find the Email folder, then read, in this order:
1. `Email/EMAIL-BRAIN.md` and every file it links (Voice DNA first).
2. `${CLAUDE_PLUGIN_ROOT}/references/master-prompt.md` (the voice and rules for every email), `recipes.md`, `subject-lines.md`, `nine-word-scripts.md`, `cadence.md`. If `Email/kit/` has edited copies, theirs win.
3. `Email/ideas.md` (open ideas).
4. What already went out: `Email/sent/` and the last two folders in `Email/months/` (subjects, stories, proof and 9-word scripts used), so nothing repeats within 6 weeks.
5. `Email/scoreboard.md`: last Friday's "one upgrade" line. Apply it this month.

The file format for every email is `${CLAUDE_PLUGIN_ROOT}/references/email-file-format.md`.

## Step 1: three quick questions (one message)

Ask all three at once, short, and say "Skip any you like":

```
Before I write your month, three quick ones:
1. Any event, workshop or launch next month? (name, date, price, link)
2. Anyone you helped lately, a client or a friend? What changed for them, and may I name them?
3. Anything happen this month you'd tell a client over coffee?
```

Add every real answer to EMAIL-BRAIN.md (proof bank, story bank, events) and to ideas.md, so it is saved for later too. If they say "just write it", go on with what you have.

## Step 2: the plan

**Which month:** the calendar month after today, unless they name one. **Week 1** starts on the first Monday of that month. Four weeks: week 1 to week 4.

**How many emails:** from `emails_per_week` in EMAIL-BRAIN.md (default 1). Never schedule more weekly emails than they promised. Their promise sets the **weekly slots**; the 9-word emails and the event set come on top, the way the cadence card says.

| Promise | Weekly slots (cadence.md) | Plus | Total |
|---|---|---|---|
| 1 a week | Wednesday, 4 emails, rotating client win, how-to, story, then the best fit | 2 nine-word (Mon week 1 and week 3), the event set if there is an event, spares to reach about 10 | about 10 (4 scheduled + 2 + 3 + spares) |
| 2 a week | Tuesday how-to, Thursday story or client win, 8 emails | 2 nine-word (Mon week 1 and week 3) | 10 |
| 3 a week | Tuesday how-to, Wednesday win, Friday Upgrade (12 slots) | 2 nine-word | write 10 now: fill the slots in date order and list the rest as open slots in calendar.md |
| 5 a week | the full table (20 slots) | 2 nine-word | write 10 now, the rest as open slots |

Rules for the mix:
- At least one each of: client win (or the **no clients yet** version), story, how-to, nine-word.
- **Event set:** if there is an event (from question 1 or EMAIL-BRAIN.md), write all three event emails. Email 1 takes the slot closest to two weeks before the event (or a Monday). Email 2 is dated the same day (it is a reply, never scheduled). Email 3 is three days after email 1. No event? No event set. Never invent one. About two campaign weeks a month at most.
- **Spares** (`status: spare`, no date, file name `spare-<type>.md`): with a promise of 1 a week, write 1 or 2 spares so the folder has about 10 emails. A spare is for the week they miss: "send the spare".
- The Friday Upgrade (3 and 5 a week) uses the `story` recipe: this week's win, the lesson, one upgrade for next week. `name: "Friday Upgrade · ..."`.
- **Never more than one client win a week**, never two emails on the same day.
- Each email has **one** idea. Use open ideas from ideas.md first, then unused proof and story bank rows, then their offer and what they teach. Match each idea to the recipe that fits it (an ideas.md line already suggests a type).
- 9-word emails: two different scripts from `nine-word-scripts.md`, adapted to the offer, not used in the last 6 weeks.

Show the plan before writing, in one short table, and ask "Good? Or change anything?" One reply is enough; if they say yes or nothing to change, write.

```
November plan · 1 email a week + 2 nine-word + your workshop
Week 1  Mon 2 Nov   9-word      "Are you still doing your books on Sunday nights?"
        Wed 4 Nov   Client win  Helping your cousin with her shoebox of receipts (no clients yet version)
Week 2  Wed 11 Nov  How-to      3 ways to spend 15 minutes on your books every Friday
...
Spare               Story       The coffee shop that never runs ads
```

## Step 3: write every email

For each email in the plan, follow `master-prompt.md` exactly, like `email-write` does:
- The recipe's shape and length. The house style. Their voice from Voice DNA and samples. Their clients' language.
- **Honesty:** only facts from EMAIL-BRAIN.md, ideas.md and their answers. A missing fact is a `[placeholder]` in the email and in `fill_in`. Never name a client unless the proof bank says `yes`.
- Their call to action exactly as given. The Three Ways PS from EMAIL-BRAIN.md where the recipe allows it. No PS offers? No PS.
- Three subject lines (moment, label, problem), the strongest as `subject`, character counts: 33 or less fits every phone, 34 to 48 is cut off in the Gmail app (the first 33 characters must make sense alone), over 48 is too long.
- Preview text 40 to 90 characters that continues the subject. Put the point in the first line of the body too: newer iPhones may show an AI summary instead of the preview text.
- Vary the openings and the subjects across the month. No two emails start the same way.

Save each to `Email/months/<YYYY-MM>/<YYYY-MM-DD>-<type-slug>.md` (spares as `spare-<type-slug>.md`). Tick each idea used in ideas.md (`- [x] ... → months/<YYYY-MM>/<file>`). Add every `side_idea` to ideas.md.

Then run the checker on the folder and fix every ERROR:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/check-emails.mjs" "Email/months/<YYYY-MM>"
```

## Step 4: rate every email (unless "quick draft")

Run the loop in `${CLAUDE_PLUGIN_ROOT}/skills/email-rate/SKILL.md` on every email file in the folder:
- Round 1: start one `email-rater` agent per email, **all in the same message**, so they run side by side.
- Rewrite only the emails under 10, using only their fixes, keeping each `best_line`, never adding facts.
- Rounds 2 and 3: fresh raters again, side by side, only for emails still under 10.
- Subject lines are part of every rating; weak subjects get rewritten in the same loop.

Then a quick whole-month read, as the writer: do two emails share an opening, a subject shape or a story? Change the weaker one and re-rate only that one.

## Step 5: calendar.md

Write `Email/months/<YYYY-MM>/calendar.md`:

```markdown
# November 2026 · my emails

Promise: 1 email a week. Send to: the newsletter tag. Tool: Mailchimp.

| Week | Day | Date | Email | Subject | Score | File | Status |
|---|---|---|---|---|---|---|---|
| 1 | Mon | 2 Nov | 9-word | Are you still doing your books on Sunday nights? | 9 | 2026-11-02-nine-word.md | draft |
| 1 | Wed | 4 Nov | Client win | My cousin's receipts were in a shoebox | 9 | 2026-11-04-client-win.md | draft |

## Spares (for the week you miss)
- Story: "The coffee shop that never runs ads" · spare-story.md

## Open slots (say "write the open slots")
- (only for 3 or 5 a week)

## Event emails
- Email 2 is a reply to people who say yes. Do not schedule it.
- Email 3 goes three days after email 1, to people who did not reply.

## Before you schedule
1. Fill in every [bracket] (12 in total, listed below).
2. Read each email out loud.
3. Paste them in: say "help me load these into <tool>".

## To fill in
- 2026-11-04-client-win.md: [how long it took]
```

Use their real platform name. Free Mailchimp plan? Add: "Mailchimp's free plan can't schedule: send each one on its day."

## Step 6: preview and hand over

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/render-preview.mjs" "Email/months/<YYYY-MM>" --open
```

This writes `Email/months/<YYYY-MM>/preview.html` (see `skills/email-preview/SKILL.md`; no Node means you write it from the template yourself).

Reply, short:

```
Your November emails are ready: 10 emails, 4 weeks.
Email/months/2026-11/ · the preview is open.

Ratings: 6 at 10/10, 4 at 9/10 (average 9.6).
Fill in before you schedule: 12 brackets. The preview highlights each one.

Next: read each one out loud, fill the brackets, then say
"help me load these into Mailchimp".
```

## If they have almost nothing

No ideas, an empty proof bank, no stories: still write the month. Lean on how-tos from what they sell, nine-word emails, the **no clients yet** client win with honest placeholders, and a story drawn from their three answers. Then say in one line which three facts would lift the month most, for example "one result from someone you helped".

## Subject line style

Use the 12 patterns in `subject-lines.md`, 2 to 6 words, and label each option with its pattern.
