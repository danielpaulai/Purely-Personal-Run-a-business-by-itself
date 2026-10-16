---
name: email-paste
description: Step-by-step help to copy finished emails into the member's own GoHighLevel, Mailchimp or ActiveCampaign: the right first-name tag, the newsletter tag, a test to themselves and scheduling. Never connects to the platform and never sends. Trigger on "help me load this into GoHighLevel", "load my emails", "paste into Mailchimp", "put these in ActiveCampaign", "how do I schedule this".
---

# Load emails into the platform

> **Where the kit is.** Every `${CLAUDE_PLUGIN_ROOT}/...` path in this skill (`references/`, `scripts/`, `templates/`, `agents/`) means: look in this skill's own folder first, then at `${CLAUDE_PLUGIN_ROOT}`. The Claude app's plugin upload keeps only skill folders, so a copy of the kit ships inside each one. A path under `skills/` is another skill: from this folder it is `../<that-skill>/SKILL.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first, find the Email folder, then read `${CLAUDE_PLUGIN_ROOT}/references/platforms.md`. That page holds the click paths. Use them exactly, and keep every **[CHECK]** mark: it tells the member a step may look different in their account. Never invent a click path. If you are not sure of a step, mark it [CHECK].

This plugin has no connection to any platform and never sends. Say so once if they ask "can you just send it?": "I can't send, on purpose. Your name is on every email. Pasting takes about two minutes each."

## Step 1: which emails, which platform

- Emails: the ones they name, or the newest month folder, or the newest draft. Only `status: draft` or `ready` ones, in date order. Skip `spare` files unless they ask.
- Platform: `platform:` in EMAIL-BRAIN.md. Not set? Ask: "GoHighLevel, Mailchimp, ActiveCampaign, or something else?" and save the answer.
- Mailchimp: ask "Are you on the free plan?" The free plan cannot schedule. Then the plan is "send each one on its day".

## Step 2: get them ready

1. Run the checker on the files. Any ERROR? Fix it first.
2. Any `[brackets]` left (the `fill_in` lists)? List them by email and say: "Fill these in first, or readers will see the brackets." Offer to fill them now if they give you the facts.
3. Render the preview (`skills/email-preview/SKILL.md`) with `--platform <their tool>`. The copy buttons there convert `{{first_name}}` to their tool's tag, ask before copying while brackets are left, and show the fallback tip.

## Step 3: the steps, for their platform only

Give the steps from `platforms.md` for their tool, numbered, short, one action per line. Start with the one-time setup (GoHighLevel plain text template; the first-name fallback for every tool), then the steps for one email, then "repeat for each email". Include:
- the first-name tag for their tool, and the fallback step
- sending only to the **newsletter** tag
- a test to themselves, read on their phone
- schedule with the day and time from `calendar.md` (or the email's `date`)
- for event emails: email 2 is a personal reply, never scheduled; email 3 leaves out people who said yes

Then a short checklist with one line per email:

```
[ ] Mon 2 Nov   9-word       "{{first_name}}"                       set the first name fallback first
[ ] Wed 4 Nov   Client win   "My cousin's receipts were in a shoebox"
...
```

## Step 4: after

When they say "done", "I scheduled them" or similar: set `status: scheduled` in each file they loaded, and update the Status column in `calendar.md`. Say: "On Friday, say **Friday scoreboard** and I'll log what went out."

If a click path did not match what they saw, ask what they saw instead, help them find it, and add a short note under that platform in their `Email/kit/` copy if they keep one. Tell them to let Danny's team know so the plugin's guide can be fixed.
