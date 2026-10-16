---
name: email-rate
description: The rating loop. A separate rater scores an email 1 to 10 (eight parts, an honesty gate, fixes), the writer rewrites from those fixes only, and the rater scores again, up to 3 rounds or a 10. Never invents facts to raise a score. Trigger on "rate my email", "score this email", "make it a 10", "how good is this email", "rate my month". Also used by email-write and email-month.
---

# Email rate: lift an email to a 10, honestly

> **Where the kit is.** Every `${CLAUDE_PLUGIN_ROOT}/...` path in this skill (`references/`, `scripts/`, `templates/`, `agents/`) means: look in this skill's own folder first, then at `${CLAUDE_PLUGIN_ROOT}`. The Claude app's plugin upload keeps only skill folders, so a copy of the kit ships inside each one. A path under `skills/` is another skill: from this folder it is `../<that-skill>/SKILL.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first. The standard is `${CLAUDE_PLUGIN_ROOT}/references/rating-rubric.md`. The rater is the plugin agent `email-rater` (`${CLAUDE_PLUGIN_ROOT}/agents/email-rater.md`). The writer is you, following `${CLAUDE_PLUGIN_ROOT}/references/master-prompt.md`.

**The one rule that makes this work:** the writer never grades its own work. Every score comes from a fresh `email-rater` run that did not write the email.

## When to skip

Skip the loop and say "Saved as a quick draft, not rated." when the member says "quick draft", "skip the rating", "no rating", or "just write it". Leave `rating_rounds: []`.

## Step 0: get the email as a file

- A file path or "rate my last email": use that file (newest in `Email/drafts/` if they say "last").
- "Rate my month": every email file in the newest `Email/months/<YYYY-MM>/` (or the month they name).
- Pasted text: save it first as `Email/drafts/<today>-<type-slug>.md` in the format in `${CLAUDE_PLUGIN_ROOT}/references/email-file-format.md`. Work out the type from its shape; ask only if you truly cannot tell. Keep their words exactly.

## Step 1: get the numbers

Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/check-emails.mjs" <file> --json`. Keep `subject_chars`, `preview_chars`, `words` and the WARN/ERROR lines for the rater. No Node? Count the characters and words yourself, carefully, and pass them on.

## Step 2: rate (round 1)

Start the `email-rater` agent (subagent type `email-writer:email-rater`). If that agent isn't available (an app upload keeps only skills), start a fresh general-purpose subagent instead and give it the whole of `agents/email-rater.md` from the kit as its instructions; it must not be the one that wrote the email. Give it a prompt with:
- the email file path
- the rubric path: `${CLAUDE_PLUGIN_ROOT}/references/rating-rubric.md`
- the EMAIL-BRAIN.md path (it reads the linked Voice DNA itself)
- the checker numbers and warnings
- `round: 1`

Several emails (a month)? Start one rater per email **in the same message**, so they run side by side.

Save the result into the email's frontmatter, as in the file format:

```yaml
best_line: "the rater's best_line"
rating_rounds:
  - round: 1
    overall: 6
    honesty: pass
    scores: {subject: 7, preview: 6, opening: 8, one_idea: 7, voice: 6, shape: 8, ask: 9, phone: 9}
```

Check the rater's math: `overall` must be the lowest part score, plus at most 1 only when every other part is 9 or 10, and 4 or lower if honesty failed. If it is wrong, use the rubric's number and note it.

## Step 3: stop or rewrite

Stop when any of these is true:
- `overall` is 10.
- This was round 3.
- Every remaining fix needs a fact only the member has (a real result, a name, a date). Then the honest move is a placeholder, not a rewrite.

Otherwise rewrite, as the writer:
1. Use **only** the rater's fixes, most important first. Change nothing else.
2. Keep `best_line` word for word.
3. Follow `master-prompt.md` and the recipe for the type (`recipes.md`). Keep the founder's voice and words. If the email came from `email-fix`, you are an editor: keep their words and stories.
4. **Never invent a fact to raise a score.** If a fix asks for a number, a result, a name, a quote or a date that is not in EMAIL-BRAIN.md, put a `[placeholder]` in and add it to `fill_in`. If that does not help, skip the fix and tell the member it needs them.
5. If a fix is about the subject or preview, rewrite `subject_options` (still three angles: moment, label, problem, each under 45 characters where possible) and the `preview_text`, and set `subject` to the strongest.
6. Save the file. Keep the previous version in mind so you can go back to it.
7. Run the checker again. Fix every ERROR before the next round.

## Step 4: rate again (rounds 2 and 3)

Start a **new** `email-rater` run each round (never reuse the last one, so it carries no memory of its own earlier scores). Give it the same inputs, the new round number, and last round's fixes so it can check they were done. Append the new round to `rating_rounds`.

If a round scores **lower** than the one before, put the previous version back, do not keep the lower round, stop, and say so in one line.

**Except for honesty.** If the rater fails the honesty gate, never go back to an earlier version: the invented detail is usually in the earlier version too (raters catch different things). Keep the round in `rating_rounds` (the honest history), remove the invented detail or turn it into a `[placeholder]`, and rate again. An email that failed honesty in its last round is never handed over as finished: if round 3 still fails, remove the detail yourself and tell the member exactly what you cut and why.

## Step 5: tell the member

Short, plain:

```
Rated 6 → 8 → 9 in 3 rounds. Honesty: pass.
Best line: "A shoebox is not a system."
What still stands between this and a 10:
- [the remaining fix, one line]
Only you can do these:
- Fill in [how long it took] with the real number.
```

Then hand back to the skill that called you (it renders the preview), or, if the member asked for the rating directly, render the preview yourself (see `skills/email-preview/SKILL.md`). The preview shows the final score and the climb as a badge.

## If the agent cannot be started

Some apps cannot start plugin agents. Then rate as a **separate step**: finish and save the email first, then do a fresh pass that reads only `rating-rubric.md`, EMAIL-BRAIN.md and the saved file, and score it as the rater, strictly, as if someone else wrote it. Tell the member: "Rated in this chat, not by the separate rater."
