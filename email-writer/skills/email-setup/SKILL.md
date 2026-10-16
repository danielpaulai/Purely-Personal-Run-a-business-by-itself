---
name: email-setup
description: Sets up the member's Email folder in their Second Brain (or ~/Documents/Email): EMAIL-BRAIN.md with who they help, offer, call to action, proof, stories, language, weekly promise and platform, plus ideas.md, drafts/, months/ and sent/. Imports the Email Brain and emails downloaded from the Email Room. Trigger on "set up my emails", "set up the email plugin", "import my email brain", "update my email brain".
---

# Email setup

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first. The file this skill fills is `${CLAUDE_PLUGIN_ROOT}/references/email-brain-template.md`. Takes about 5 minutes. Ask one short question at a time, in plain words.

## Step 1: find their Second Brain

Look for it, in this order:
1. The current folder, if it has any of: `BUSINESS-BRAIN.md`, `voice-dna-*.md`, `positioning-*.md`, `icp-*.md`, a `.obsidian/` folder, or many `.md` files.
2. Ask: "Where is your Second Brain folder? You can drag the folder into this chat, or type its path."
3. No Second Brain? Use `~/Documents/Email/` and say: "No problem. I'll keep your emails in Documents/Email. You can move the folder later."

If an `Email/EMAIL-BRAIN.md` already exists there, do not start again. Say what is already filled in and offer to update the empty parts.

## Step 2: make the folder

Run:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/make-email-folder.mjs" "<second brain folder>"
```

It creates `Email/` with `EMAIL-BRAIN.md`, `ideas.md`, `scoreboard.md`, `README.md`, `drafts/`, `months/`, `sent/`, `previews/` and `kit/` (recipes, subject lines, 9-word scripts, rules, cadence, glossary, finding ideas). It never overwrites a file. It prints what it made.

**No Node?** Make the same files by hand: copy `email-brain-template.md` to `Email/EMAIL-BRAIN.md`, and copy `recipes.md`, `subject-lines.md`, `nine-word-scripts.md`, `rules.md`, `cadence.md`, `glossary.md` from `${CLAUDE_PLUGIN_ROOT}/references/` into `Email/kit/` (and `ideas.md` as `Email/kit/finding-ideas.md`). Write `ideas.md` and `scoreboard.md` as the script would (see the script for the exact text).

## Step 3: import from the Email Room

Ask: "Did you download your Email Brain from the Email Room?" If yes, look for it in the Second Brain folder and `~/Downloads/` (`EMAIL-BRAIN*.md`, or a downloaded folder that has one, plus any `ideas.md` and email `.md` files with it). Ask before reading Downloads.

The room gives two downloads: `EMAIL-BRAIN.md` (starts with `# EMAIL BRAIN ·`) and `my-emails-<date>.md` (all the room's emails in one file). Import both with:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/room-import.mjs" --email-dir "<Email folder>" --brain "<EMAIL-BRAIN.md>" --emails "<my-emails-....md>" --month <YYYY-MM>
```

- It converts the room's EMAIL-BRAIN.md into the plugin's format (frontmatter, proof bank table with the "May I name them?" column, story bank, Three Ways PS), saves the room's writing sample as `Email/voice-sample.md` and links it, and adds the room's idea bank to `ideas.md`.
- It splits the emails into one file each in `Email/months/<YYYY-MM>/`, turning "Week 2 Tue" into real dates (week 1 starts on the first Monday). Ask which month they plan to send them in; default is next month. Emails beyond week 4 become spares.
- If EMAIL-BRAIN.md was already filled in, the room version is saved as `EMAIL-BRAIN.imported.md`: merge it into EMAIL-BRAIN.md (keep both sides' facts, ask if two disagree). Keep both files and tell them EMAIL-BRAIN.md is the one in use.
- Then read the imported EMAIL-BRAIN.md and check it with them: the room asks fewer questions than this setup, so Step 5 will still have gaps to fill.
- Run the checker on the imported month and render the preview, so they see their room emails straight away.

## Step 4: link, do not copy, their Second Brain files

Find and list under **Read these too** in EMAIL-BRAIN.md, as relative paths from the Email folder (use `[[wikilinks]]` too if the folder has `.obsidian/`):
- Voice DNA: `voice-dna-*.md`, `*voice*.md`
- Offer: `*offer*.md`, `business-inbox-*.md`
- Positioning: `positioning-*.md`, `icp-*.md`, `messaging-*.md`
- Business Brain: `BUSINESS-BRAIN.md`
- Sample emails: any folder of past emails or newsletters

Read them now and pre-fill what they answer (who they help, the result, the offer, the language, words they use). Show what you filled and ask "Is that right?" Never copy whole files into EMAIL-BRAIN.md.

## Step 5: fill the gaps

Ask only for what is still empty, one at a time, short:

1. "Who do you help, in one line?"
2. "What result do you help them get?"
3. "What do you sell, and what is the one thing you ask people to do? (reply, book a call, join a workshop)"
4. "Three ways people can work with you, smallest to biggest? This becomes your PS." (Skip is fine. Then no PS.)
5. "Any client results? No clients yet is fine: someone you helped for free, a friend, or your own result." For each one: before, what you did, after, and **"May I name them in emails? yes, no, or ask them first."**
6. "Two or three small moments you'd be happy to share? A trip, a mistake, something a client said." (The coffee test: would you say it to a client over coffee?)
7. "Which language do your clients read?"
8. "How many emails a week can you promise for the next 30 days? One is great." Default 1. Never push for more.
9. "Which tool do you send with: GoHighLevel, Mailchimp, ActiveCampaign, or something else?" And their sender email if they know it.
10. "What may I read to find email ideas? Your Second Brain notes? Your calendar, if it is connected?" Write the answer under **My platform** as "May read: ...".

Write every answer into EMAIL-BRAIN.md, both in the frontmatter (`name`, `business`, `sender_email`, `platform`, `emails_per_week`, `language`, `updated`) and in the matching section. Only write what they said. Empty stays empty.

## Step 6: finish

Say, short:

```
Your Email folder is ready: <path>
- EMAIL-BRAIN.md: filled in (3 things still empty: ...)
- The kit is in Email/kit/

Five things you can say to me:
1. "add an idea: ..."
2. "write a client win" (or story, 9-word email, how-to, event invite)
3. "write next month's emails"
4. "fix my email" (paste your 8-minute draft)
5. "show me my emails"

I never send anything. You read it out loud, paste it and schedule it.
```

If they have no list yet, add one line: "No list yet? Start with people who already know you. Send each one a personal 'can I add you to my weekly email?' first."
