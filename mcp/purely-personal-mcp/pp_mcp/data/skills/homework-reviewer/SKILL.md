---
name: homework-reviewer
description: Bulk-score a batch of posts (a group's homework, a team's drafts, a content backlog), rank them with the Invisibility Diagnostic, and produce a shortlist with industry coverage, a shout-out list and a private coaching list. Use when asked to review the homework, rank the posts, find the best 10, or grade a batch. Triggers on "review the homework", "rank the posts", "find the best posts", "grade this batch", "compile the shortlist".
version: 1.1.0
author: daniel-paul
tags: [review, scoring, batch, invisibility-diagnostic]
---

# Homework Reviewer

Scores every post in a batch with the Invisibility Diagnostic (Voice, POV, Specificity, Asking), ranks them, and builds a shortlist a facilitator can use straight away. Works for any batch: a workshop's homework, a team's drafts, a backlog of old posts.

## Why not just paste 50 posts into a chat?
Pasted batches get inconsistent picks, no check that the shortlist covers different industries, and no list of who needs help. This skill scores every post the same way, ranks by score, and checks coverage.

## Inputs

| Input | Format |
|---|---|
| Posts | A JSON list of `{"name", "industry", "post"}`, **or** plain text with posts separated by a line containing only `---` (optionally `Name:` and `Industry:` lines at the top of each) |
| Batch context | Optional: how many to shortlist, the industries in the room |

## Modes

| Mode | What you get |
|---|---|
| `quick` | Top N only, with scores |
| `standard` (default) | Top N with the opening line of each, an industry coverage check, a next-15 shout-out list |
| `full` | Standard plus a coach list of posts scoring 0-1 with the one-line fix for each, and the full ranked list |

## Process

1. Parse and validate the posts. Report how many were read and skip empties.
2. Score each post 0-4 with the Invisibility Diagnostic (the `score_post` engine). Record the score, tier, character count and the fix lines.
3. Rank by score, then Specificity, then length.
4. Pick the top N, limiting any one industry to two places while the batch is large enough to allow it, so the shortlist is not all one niche.
5. Build the shout-out list (the next 15) and the coach list (posts scoring 0 or 1, each with its first fix line).
6. Order the top N for the read-aloud: open strong, build, finish on the post that teaches the most.

## Output

```
HOMEWORK REVIEW · <n> posts · 4/4: a · 3/4: b · 2/4: c · 0-1/4: d

SHORTLIST (top N, in reading order)
  1. <name> · <industry> · <score>/4 · "<opening line>"

INDUSTRY COVERAGE
CHAT SHOUT-OUTS (next 15)
COACH LIST (0-1/4, private check-in, with the one-line fix)
```

## Rules
- Scores are heuristic. A script cannot hear that a sentence is not the writer's. Read the top 10 yourself before using the shortlist.
- Never alter a participant's post, and never add a name, number or result that was not in it.
- Share names only with the facilitator unless the participants agreed to be read out.

## Limitations
- Scores posts as text; it does not see images or carousels.
- Industry coverage depends on the `industry` field you supply.

---

## Use in the Purely Personal connector

Tool: `review_homework`. It returns the ranked shortlist, coverage, shout-out list and coach list. Scores come from the same engine as score_post.
