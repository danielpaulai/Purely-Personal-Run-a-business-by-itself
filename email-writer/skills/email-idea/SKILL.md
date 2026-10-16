---
name: email-idea
description: Catch and find email ideas. "Add an idea: ..." saves it to Email/ideas.md with the date and an email type. "Find me ideas" reads ideas.md, Second Brain notes and the proof and story banks, and suggests 10 ideas tied to the member's business. Trigger on "add an idea", "save this idea", "email idea", "find me ideas", "I have nothing to write about".
---

# Email ideas

> **Where the kit is.** Every `${CLAUDE_PLUGIN_ROOT}/...` path in this skill (`references/`, `scripts/`, `templates/`, `agents/`) means: look in this skill's own folder first, then at `${CLAUDE_PLUGIN_ROOT}`. The Claude app's plugin upload keeps only skill folders, so a copy of the kit ships inside each one. A path under `skills/` is another skill: from this folder it is `../<that-skill>/SKILL.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first, then find the Email folder. Background for you: `${CLAUDE_PLUGIN_ROOT}/references/ideas.md` (the places ideas pile up and "something you saw + your business = an email").

## The ideas.md line format

```
- [ ] 2026-10-15 · story · The client who kept receipts in a shoebox · from: week
```

`- [ ]` open, `- [x]` used. Fields, split by ` · `: date added, suggested type (`client_win`, `story`, `nine_word`, `how_to`, `event_invite`), the idea in one line, where it came from (`film`, `child`, `week`, `photo`, `clients`, `offer`, `calendar`, `notes`, `other`). When an email uses an idea, the writer ticks it and adds ` → <email file>`.

## "Add an idea: ..."

1. Pick the type that fits best:
   - a client result or someone they helped → `client_win`
   - something that happened, a moment, a mistake → `story`
   - a question to ask the list → `nine_word`
   - something they could teach in three tips → `how_to`
   - an event, workshop, call or launch → `event_invite`
2. Tidy the idea into one clear line in their words. Do not add facts.
3. Append it to the end of `Email/ideas.md`. Several ideas at once? One line each.
4. Reply in one or two lines: `Saved: "<idea>" as a <type> idea. You have <n> open ideas.` If it is a strong one, add: "Want me to write it now while you still care about it?"

If it names a client, add ` · ask before naming` to the line.

## "Find me ideas"

Read only what you can actually reach, and say what you read:
1. `Email/ideas.md`: open ideas (do not suggest repeats).
2. `Email/EMAIL-BRAIN.md`: proof bank and story bank rows not yet used, the offer, upcoming events.
3. The Second Brain: notes changed in the last 14 days (skip the `Email/` folder). `find "<brain>" -name "*.md" -mtime -14 -not -path "*/Email/*"`. Read titles first, open the promising ones.
4. The calendar, only if a calendar connector is available and EMAIL-BRAIN.md says it may read it: event titles from the last 7 days and the next 14 days. Calls, workshops and launches make good ideas. Never put a client's name in an idea from the calendar without "ask before naming".
5. `Email/sent/` and the last month folder: so you do not repeat a topic from the last 6 weeks.

Do not claim to read their phone photos, chats or email. Instead, end with: "Your phone photos are the best idea place. Scroll the last week, then tell me 'add an idea: ...' for anything that made you stop."

Then suggest **10 ideas**, a mix of types (at least 2 stories, 1 client win or helped-someone, 2 how-tos, 2 nine-word questions, and an event invite if an event is coming). Each one in this shape:

```
1. [story] The shoebox of receipts my cousin handed me
   Why it works: every shop owner has a shoebox. Lesson: a box is not a system.
   From: your note "Jo's receipts" (12 Oct)
```

Every idea must come from something real you read or they told you, plus the link to their business. No invented events, clients or results.

Ask: "Which ones should I save? Say the numbers, or 'all'." Append the chosen ones to ideas.md in the line format. Then offer: "Want me to write one now?"

## If ideas.md does not exist

The Email folder is not set up. Say: "Say **set up my emails** first, it takes 5 minutes." If they insist, create `Email/ideas.md` with a one-line header and save the idea anyway.
