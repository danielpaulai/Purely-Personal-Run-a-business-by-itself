---
name: email-subjects
description: Ten subject lines for one email across three angles (moment, label, problem) and 12 patterns, or all in one pattern they name, each with a character count showing how it fits on a phone, plus a pick and preview text. Updates the email file if there is one. Trigger on "give me subject lines", "subject lines for this", "better subject line", "make it a confession subject", "is this subject line good".
---

# Subject lines

> **Where the kit is.** Every `${CLAUDE_PLUGIN_ROOT}/...` path in this skill (`references/`, `scripts/`, `templates/`, `agents/`) means: look in this skill's own folder first, then at `${CLAUDE_PLUGIN_ROOT}`. The Claude app's plugin upload keeps only skill folders, so a copy of the kit ships inside each one. A path under `skills/` is another skill: from this folder it is `../<that-skill>/SKILL.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first, then `${CLAUDE_PLUGIN_ROOT}/references/subject-lines.md` (the three angles, the rules and 30 examples) and the subject rules in `master-prompt.md`.

## Step 1: get the email

A file path, "my last email" (newest in `Email/drafts/`), an email in the current month folder they name, or pasted text. Read the whole email: a subject must be paid off by the email. If they only give a topic, ask for the email or two lines about what is in it.

## Step 2: write 10

**Their style comes first.** If they name a pattern ("give me confession subject lines", "something like an odd pair"), write all 10 in that pattern.

The 12 patterns are in `subject-lines.md`: odd pair, a character, confession, a number that stings, famous name + your business, short maxim, their words, callout, warning, life moment, question, plain label. Aim for 2 to 6 words. Label each option with its pattern.

Otherwise, the default spread:

- **4 moment:** zoom in on the most interesting or surprising moment in the email.
- **3 label:** a plain, honest label of what is inside. Boring and clear on purpose.
- **3 problem:** the reader's problem, in the reader's words.
- Special cases from `subject-lines.md`: a client win includes the result itself as one option; a 9-word email includes `{{first_name}}` or one plain word; an event invite includes the event name or the date.
- Sentence case, like a person. No clickbait the email does not pay off. No ALL CAPS, no "!!!", no fake "Re:" or "Fwd:". No em dashes. No invented facts (a number in a subject must be in the email).
- The point goes first: the first 33 characters must make sense alone.

Count the characters of each one carefully (count `{{first_name}}` as 6).

## Step 3: show them

```
Moment
1. My cousin's receipts were in a shoebox   38  amber
2. ...

Label
5. ...

Problem
8. Dreading your tax return?                25  green

Recommended: 8, "Dreading your tax return?" Short, in your reader's words, and the email answers it.
Preview text: She thought it would take a whole weekend. It took one evening. (63)

green = 33 or less, fits every phone
amber = 34 to 48, cut off in the Gmail app, so the first 33 characters must make sense alone
red   = over 48, cut off on most phones
```

Mark every red one clearly and offer a shorter version of it. Add one line: "On newer iPhones, Apple may show an AI summary instead of your preview text, so the first line of the email matters too."

## Step 4: save (if there is a file)

Ask "Which one?" (or use the recommended if they say "you pick"). Then update the email file's frontmatter: `subject` to the chosen one, `subject_options` to the chosen one plus the best of the other two angles (three in total, one per angle), `recommended_reason`, and `preview_text` if they took the new one. Run the checker on the file.

## Optional: rate it

If they ask "is this subject line good?" or "rate it", or the email is already rated, run the rating loop (`skills/email-rate/SKILL.md`) on the email file. The rater's `subject` and `preview` part scores are the answer; the rewrite step changes only `subject_options`, `subject` and `preview_text`. Then re-render the preview so they can see the subject at phone width (`skills/email-preview/SKILL.md`).
