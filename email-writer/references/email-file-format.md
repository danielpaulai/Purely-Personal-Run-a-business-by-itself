# The email file format

Every email this plugin writes is one markdown file. Every skill reads and writes this exact format, and the preview script (`scripts/render-preview.mjs`) and the checker (`scripts/check-emails.mjs`) read it too. Do not invent other fields or other layouts.

## Where files go

```
Email/
  EMAIL-BRAIN.md            who they are, offer, proof, stories, promise, platform
  ideas.md                  the idea list
  scoreboard.md             the Friday numbers
  drafts/                   single emails: <YYYY-MM-DD>-<type-slug>.md
  months/<YYYY-MM>/         a month of emails + calendar.md + preview.html
  sent/                     emails that went out (moved here by email-scoreboard)
  previews/                 preview HTML for single emails
  kit/                      the email kit (recipes, subject lines, rules...)
```

**File names:** `<YYYY-MM-DD>-<type-slug>.md`, where the date is the planned send day. Type slugs: `client-win`, `story`, `nine-word`, `how-to`, `event-invite-1`, `event-invite-2`, `event-invite-3`, `eight-minute`. Two of the same type on one day: add `-2`. Spare emails (written but not scheduled) go in the month folder as `spare-<type-slug>.md`.

## The file

```markdown
---
type: client_win
sequence_step: 0
name: "Client win · helped my cousin with her receipts"
date: 2026-11-04
status: draft
subject: "My cousin's receipts were in a shoebox"
subject_options:
  - text: "My cousin's receipts were in a shoebox"
    angle: moment
  - text: "How I sorted 6 months of receipts"
    angle: label
  - text: "Dreading your tax return?"
    angle: problem
recommended_reason: "The shoebox is a picture every shop owner knows."
preview_text: "She thought she'd need a whole weekend. It took one evening."
cta: "Reply \"shoebox\""
side_idea: "Why I ask for bank statements first"
fill_in:
  - "[how long it took]"
best_line: "A shoebox is not a system."
rating_rounds:
  - round: 1
    overall: 6
    honesty: pass
    scores: {subject: 7, preview: 6, opening: 8, one_idea: 7, voice: 6, shape: 8, ask: 9, phone: 9}
  - round: 2
    overall: 9
    honesty: pass
    scores: {subject: 9, preview: 9, opening: 9, one_idea: 9, voice: 9, shape: 9, ask: 10, phone: 10}
---
Hey {{first_name}},

I just got a message from my cousin...

Maya

PS Three ways I can help: ...
```

## The fields

| Field | Required | What it holds |
|---|---|---|
| `type` | yes | `client_win`, `story`, `nine_word`, `how_to`, `event_invite`, `eight_minute_edit` |
| `sequence_step` | yes | `1`, `2` or `3` for event_invite, `0` for everything else |
| `name` | yes | Short internal name. Never shown to readers. |
| `date` | yes | Planned send day, `YYYY-MM-DD`. Leave empty only for spares. |
| `status` | yes | `draft` (just written), `ready` (they read it out loud and filled every bracket), `scheduled` (loaded into their platform), `sent`, or `spare` |
| `subject` | yes | The chosen subject line, exactly as it will be sent |
| `subject_options` | yes | Three options, each with `text` and `angle` (`moment`, `label`, `problem`). `subject` must be one of them. |
| `recommended_reason` | yes | One short line: why that subject |
| `preview_text` | yes | The grey line after the subject. 40 to 90 characters. Continues the thought, never repeats the subject. |
| `cta` | yes | The one ask, e.g. `Reply "shoebox"` or `Book a call: <link>` |
| `side_idea` | no | A second idea that showed up. It also gets added to `ideas.md`. |
| `fill_in` | yes | Every `[placeholder]` in the subject, preview or body. Empty list `[]` when there are none. |
| `best_line` | no | The strongest line, from the rater. Rewrites keep it. |
| `rating_rounds` | no | One entry per rater pass: `round`, `overall`, `honesty`, `scores` (the eight parts). Empty `[]` or missing means not rated (a "quick draft"). |
| `idea` | no | The `ideas.md` line this email came from |
| `time` | no | Planned send time, `"08:00"` |

## The body

- Everything after the closing `---` is the email body, exactly as it will be pasted. Plain text. No markdown headings, no bold, no bullet lists unless the how-to tips need numbers.
- Paragraphs are separated by one blank line.
- It starts with the greeting (`Hey {{first_name}},`) and ends with the sign-off (the founder's first name). The nine-word email and event invite steps 1 and 3 may skip the greeting.
- The PS, when there is one, comes after the sign-off, on its own paragraph, starting with `PS`.
- The only merge field is `{{first_name}}`. The preview converts it for each platform: `{{contact.first_name}}` for GoHighLevel, `*|FNAME|*` for Mailchimp, `%FIRSTNAME%` for ActiveCampaign.
- Placeholders are square brackets: `[client first name]`. Every one must also be listed in `fill_in`.

## Writing the frontmatter safely

- Put every text value in double quotes. Inside a value, write a double quote as `\"`.
- One value per line. No multi-line values.
- Lists use `  - ` (two spaces, dash, space). An empty list is `[]`.
- `scores` is one line in curly brackets: `{subject: 7, preview: 6, ...}`.
- No em dashes anywhere, in any field.

## How the room's JSON maps to this file

`kit/master-prompt.md` and `kit/output-schema.md` were written for the Email Room, which returns JSON. In this plugin, write the same content into this file instead:

| Room JSON | This file |
|---|---|
| `type`, `sequence_step`, `name`, `preview_text`, `cta`, `side_idea`, `fill_in` | same name in the frontmatter |
| `subject_options` | `subject_options` (same `text` + `angle`) |
| `recommended_subject` (an index) | `subject` (the text of that option) |
| `recommended_reason` | `recommended_reason` |
| `body` | the body |
| `ps` | the last paragraph of the body, after the sign-off |
| `feedback` (edit task) | shown in chat, not saved in the file |

The rater's JSON (`references/rating-rubric.md`) maps like this: each pass becomes one `rating_rounds` entry (`round`, `overall`, `honesty`, `scores`), and `best_line` is saved once. The `fixes` are used for the rewrite and shown in chat, not saved.
