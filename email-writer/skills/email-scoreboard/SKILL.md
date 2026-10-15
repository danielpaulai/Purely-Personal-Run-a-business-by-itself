---
name: email-scoreboard
description: The Friday scoreboard. Asks for four numbers (emails sent, replies, new subscribers, calls booked), appends them to Email/scoreboard.md, moves the emails that went out into Email/sent/, and gives one upgrade for next week. Never says "missed". Trigger on "Friday scoreboard", "log my numbers", "how did my emails do", "my email numbers", "scoreboard", "weekly email check-in".
---

# Friday scoreboard

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first and find the Email folder. Read `Email/scoreboard.md` (create it with the header from `scripts/make-email-folder.mjs` if it is missing), EMAIL-BRAIN.md (`emails_per_week`), and this week's emails (files dated Monday to Sunday of this week in `Email/months/` and `Email/drafts/`).

## Step 1: the four numbers (one message)

Pre-fill what you can see: emails dated this week with `status: scheduled` or `sent` count as sent. Then ask:

```
Friday scoreboard, week of 2 Nov.
I count 2 emails sent this week. Right?
1. Emails sent:
2. Replies (any reply counts, even "thanks"):
3. New subscribers:
4. Calls booked:
```

Accept rough numbers and "don't know" (write `?`). Do not ask about open rates. If they offer one, say once: "Open rates are unreliable now. Compare only with your own past weeks. Replies and calls matter most."

## Step 2: save

Append one row to the table in `Email/scoreboard.md`:

```
| 2026-11-02 | 2 | 5 | 3 | 1 | Send a 9-word email on Monday |
```

`Week of` is that week's Monday. The last column is the one upgrade (Step 4).

Move each email that went out this week from its folder into `Email/sent/` (keep the file name, set `status: sent`), and update its row in `calendar.md` if there is one. Ask before moving if you are not sure it went out.

## Step 3: what the numbers say (two lines, kind and true)

- Compare with their promise (`emails_per_week`) and the last 3 rows. Never use the words "missed", "failed" or "behind". Fewer sent than promised: "Next one goes out Monday." Zero sent: "Just send the next one. The spare in your month folder is ready."
- Name one real good thing from the numbers or their emails (a reply, a new subscriber, an email they wrote even if it did not go out).

## Step 4: one upgrade for next week

Exactly one, specific, doable in under 15 minutes. Pick the first that fits:

1. Sent fewer than promised: "Send the spare on Monday" (name the file), or "Promise 1 a week for now."
2. Sent, but 0 replies two weeks running: "Send a 9-word email on Monday" (suggest the script, not used in 6 weeks).
3. Replies but 0 calls: "End your next email with one easy ask: <their call to action>", or reply to every reply personally and invite a short call.
4. No new subscribers two weeks running: "Put your signup link in your LinkedIn profile and your next post."
5. All good: "Add a PS with your three ways to help," or "Write next week's client win while it is fresh."

Write it in the last column, and say it in one line. Then: "Say **write next month's emails** when you're ready for more."
