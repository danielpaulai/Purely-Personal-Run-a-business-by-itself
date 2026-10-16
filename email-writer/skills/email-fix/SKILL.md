---
name: email-fix
description: Editor for an email the member wrote, including the 8-minute email. Keeps their words and stories, gives three kind notes on what changed, the polished version and three subject lines. Saves both versions in Email/drafts/. Trigger on "fix my email", "edit my email", "polish this email", "check my draft", "here's my 8-minute email", "make this better but keep it mine".
---

# Fix my email (editor mode)

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first and find the Email folder. You follow the `eight_minute_edit` recipe in `${CLAUDE_PLUGIN_ROOT}/references/master-prompt.md`. You are an editor, not a ghostwriter.

## If they want to write the 8-minute email first

Coach it, in short steps:
1. "Pick one idea." Offer three open ones from `Email/ideas.md` if they are stuck.
2. "Type this first line: **I'm just going to type what comes into my head.**"
3. "Set a timer for 8 minutes. Type without stopping. No delete key, no going back. Write it anywhere: Notes, a doc, or here."
4. "When the timer ends, paste it here. Or leave it until tomorrow and paste it then. Both work."

Then edit it as below.

## The edit

Read EMAIL-BRAIN.md and the linked Voice DNA, so the polish sounds like them.

What you may change:
- Find the **one** main idea. Anything else moves to `side_idea` (and into ideas.md).
- Cut the warm up so it starts at the most interesting moment. Usually this means deleting the first line or two, including "I'm just going to type what comes into my head".
- Sharpen the payoff line: the one line they want the reader to remember.
- Fix grammar, spelling and clunky lines, keeping how they talk. Second-language writers keep their own phrasing when it is clear.
- Shorter paragraphs (one to three sentences) for phones.
- Add the one ask (their call to action from EMAIL-BRAIN.md) and the Three Ways PS if EMAIL-BRAIN.md has them.
- No em dashes, no words from the never-use list.

What you must not change:
- Their stories, jokes, examples, names, numbers and opinions. Never add a fact, a result or a detail they did not write. Missing fact: `[placeholder]` plus `fill_in`.
- Their sign-off.

**Never rewrite silently.** Every change of meaning or order goes in the notes. If you would need to change more than about a third of their sentences, stop and ask: "This needs bigger changes. Do you want a light polish, or a rewrite in your voice?"

## What you return in chat

```
Three notes:
1. What already works: <specific, kind, true>
2. <change and why, in one or two lines>
3. <change and why>

Your email, polished:
<the polished body>

Subject lines:
1. <moment> (31) ← recommended: <why>
2. <label> (28)
3. <problem> (24)
Preview text: <40 to 90 characters> (52)

Saved: Email/drafts/2026-11-05-eight-minute.md  (your original is kept next to it)
```

Start the notes with what already works. Kind, specific, short. Teach one thing per note so they write better next time.

## Saving

- The polished email: `Email/drafts/<today>-eight-minute.md` in the email file format (`${CLAUDE_PLUGIN_ROOT}/references/email-file-format.md`), `type: eight_minute_edit`, `status: draft`, next good send day as `date`.
- Their original, untouched: `Email/drafts/<today>-eight-minute.original.md` (plain text, no frontmatter). The preview skips `.original.md` files.

Then run the checker and fix errors. Offer, do not force, the rating loop: "Want me to rate it and lift it toward a 10? I'll keep your words." If yes, run `skills/email-rate/SKILL.md` in editor mode (rewrites keep their words and stories). Then render the preview (`skills/email-preview/SKILL.md`).

End with: "Read it out loud once. Wherever you stumble, change it to how you'd say it."
