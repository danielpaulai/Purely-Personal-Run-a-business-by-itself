---
name: email-write
description: Write one email (or the three-email event invite) from the member's EMAIL-BRAIN.md, following the Email Room master prompt and recipes exactly: client win, story, 9-word email, how-to or event invite. Three subject lines (moment, label, problem) with character counts, preview text, never invents facts (placeholders plus a fill-in list), runs the rating loop, saves to Email/drafts/ and renders the inbox preview. Trigger on "write a client win", "write a story email", "write a 9-word email", "nine word email", "write a how-to email", "write an event invite", "invite people to my workshop", "write an email about ...", "turn this idea into an email". Say "quick draft" to skip the rating.
---

# Write one email

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first, find the Email folder, and read everything it says to read before writing (EMAIL-BRAIN.md, the linked Voice DNA, `master-prompt.md`, the recipe in `recipes.md`). The file format is `${CLAUDE_PLUGIN_ROOT}/references/email-file-format.md`.

## Step 1: what kind of email

From what they said, pick one type: `client_win`, `story`, `nine_word`, `how_to`, `event_invite`. "Write an email about X" with no type: pick the recipe that fits X best and say which in one line. A fast draft they typed themselves goes to `email-fix` instead.

## Step 2: get the real facts (ask at most two short questions)

Use EMAIL-BRAIN.md, the idea they gave, and `ideas.md`. Only ask what the recipe truly needs and you do not have:

- **client_win:** which result from the proof bank? Check its "May I name them?" column. Not `yes`? Ask: "May I name them, or shall I describe them (like 'a cafe owner in Leeds')?" No clients yet: use the **no clients yet** version from the recipe (someone they helped for free, a friend, a beta tester, or their own result) and say so honestly in the email ("Last week I helped a friend who..."). Never make up a result: no result given means `[the result in numbers]` in the email and in `fill_in`.
- **story:** what happened, where, when? Use a story bank row if it fits. Do not add details they did not give.
- **nine_word:** pick a script from `nine-word-scripts.md` that fits the offer and has not been used in `sent/` or the last month folder. No question needed.
- **how_to:** what is the one thing to teach? Use what they already teach (offer, method parts, posts).
- **event_invite:** the event name, who it is for, date and time, place or link, price. Missing? Use the master prompt's placeholder (a free 45 minute online workshop) and put topic, date and time in `fill_in`. Write all three emails.

If something is still missing, do not stop to ask more: write it with a `[placeholder]` and add it to `fill_in`.

## Step 3: write it

Follow `master-prompt.md` exactly: the house style, the honesty rules, the recipe shape and length, the subject line rules, the preview text rules. For subject length, use the phone counts: 33 characters or less fits every phone, 34 to 48 is cut off in the Gmail app (so the first 33 characters must make sense alone), over 48 is too long. Put the point of the email in its first line: newer iPhones may show an AI summary instead of the preview text. Use their call to action exactly as given. Add the Three Ways PS from EMAIL-BRAIN.md when the recipe allows it (never on a 9-word email or event steps 1 and 3). No PS offers in EMAIL-BRAIN.md? No PS. Write in their clients' language.

Write the file in the email file format:
- `date`: the next good day from `cadence.md` for this type (Wednesday for a client win, Tuesday how-to, Thursday story, Monday 9-word) unless they named a day.
- `status: draft`
- three `subject_options` (`moment`, `label`, `problem`), `subject` = the strongest, `recommended_reason` in one line.
- `fill_in`: every `[placeholder]`, or `[]`.
- `side_idea`: a second idea that showed up, or `""`. Also append it to `ideas.md`.
- `idea`: the ideas.md line it came from, and tick that line (`- [x] ... → drafts/<file>`).

Save to `Email/drafts/<YYYY-MM-DD>-<type-slug>.md`. Event invites: three files, `-event-invite-1/2/3`, dated email 1 day, email 2 the same day (it is a reply), email 3 three days later.

## Step 4: check, then rate

1. `node "${CLAUDE_PLUGIN_ROOT}/scripts/check-emails.mjs" <file>`. Fix every ERROR. Fix WARN lines unless there is a good reason.
2. Unless they said "quick draft": run the rating loop in `${CLAUDE_PLUGIN_ROOT}/skills/email-rate/SKILL.md` on the file (the separate `email-rater` agent scores it, you rewrite from its fixes only, up to 3 rounds or a 10). The subject lines are part of the score: if the subject part is the weakest, the rewrite improves `subject_options` too.

## Step 5: preview and hand over

Render the preview (see `${CLAUDE_PLUGIN_ROOT}/skills/email-preview/SKILL.md`):

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/render-preview.mjs" "<the file>" --open
```

Then reply, short:

```
Saved: Email/drafts/2026-11-04-client-win.md  (rated 6 → 8 → 9)

Subject lines (pick one):
1. My cousin's receipts were in a shoebox (38, amber) ← recommended: <reason>
2. How I sorted 6 months of receipts (33, green)
3. Dreading your tax return? (25, green)
(green = fits every phone, amber = cut off in the Gmail app, red = over 48, too long)
Preview text: She thought it would take a whole weekend. (43)

Fill in before you send:
- [how long it took]

The preview is open. Read it out loud before you send.
```

Show the email body in chat only if they ask, or if the preview could not be opened.

## Subject line style

If EMAIL-BRAIN.md has a "Subject lines I love" section, every subject option follows that style (length, tone, casing, pattern), never those words. Otherwise use the 12 patterns in `subject-lines.md`, 2 to 6 words, and label each option with its pattern.
