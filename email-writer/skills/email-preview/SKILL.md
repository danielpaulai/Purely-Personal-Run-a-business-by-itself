---
name: email-preview
description: Render any email file, or a whole month folder, into one self-contained HTML page that looks like a real inbox and open it: an inbox list (avatar, sender, bold subject, grey preview text, day), click to read the full plain-text email, a Phone view that shows how subjects cut off, the rating badge and climb, and per-email copy buttons for GoHighLevel, Mailchimp and ActiveCampaign that convert the first-name merge field. Trigger on "show me my emails", "preview my emails", "preview this email", "how does it look in the inbox", "open my month", "show it on a phone".
---

# Email preview

Read `${CLAUDE_PLUGIN_ROOT}/references/plugin-rules.md` first and find the Email folder.

## What to render

- "Show me my emails" with no detail: the newest folder in `Email/months/`. If there is none, `Email/drafts/`.
- One email: that file.
- A month: `Email/months/<YYYY-MM>/`.
- "Everything": the `Email/` folder (it reads drafts, months and sent, and skips `kit/` and `previews/`).

Only files with frontmatter that has a `type:` line count as emails (see `${CLAUDE_PLUGIN_ROOT}/references/email-file-format.md`). `calendar.md`, `README.md` and `.original.md` files are skipped.

## Render it (Node 18 or newer)

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/render-preview.mjs" "<file or folder>" --open
```

- A folder writes `<folder>/preview.html`. One file writes `Email/previews/<name>.html`.
- The sender name, sender email and platform come from EMAIL-BRAIN.md. Override with `--from "Maya" --email maya@... --platform mailchimp`.
- `--out <path>` writes somewhere else. `--no-fonts` drops the Google Fonts link (offline use).
- It prints the path, the number of emails, the things to fill in, and checker errors. Mention the errors.

If `--open` does not open it (some apps cannot), give the full path and say "Double-click this file to open it in your browser."

Check Node first if unsure: `node --version`. 18 or newer is needed.

## No Node? Write the page yourself

1. Read `${CLAUDE_PLUGIN_ROOT}/templates/preview-template.html`.
2. Build the data object for the `__EMAIL_DATA__` placeholder, as one line of JSON:

```json
{
  "title": "November 2026",
  "generated": "2026-10-15T09:00:00Z",
  "sender": { "name": "Maya", "email": "maya@example.com", "initial": "M" },
  "platform": "mailchimp",
  "emails": [{
    "id": 0, "file": "2026-11-04-client-win.md", "type": "client_win", "typeLabel": "Client win",
    "sequence_step": 0, "name": "...", "date": "2026-11-04", "time": "", "status": "draft",
    "subject": "...", "subjectChars": 38,
    "subject_options": [{ "text": "...", "angle": "moment", "chars": 38, "chosen": true }],
    "recommended_reason": "...", "preview_text": "...", "cta": "...", "side_idea": "",
    "fill_in": ["[how long it took]"], "best_line": "...",
    "rating_rounds": [{ "round": 1, "overall": 6, "honesty": "pass", "scores": {} }],
    "body": "the body exactly as in the file, with \n line breaks",
    "checks": []
  }]
}
```

`platform` is `gohighlevel`, `mailchimp`, `activecampaign` or `other`. `typeLabel`: Client win, Story, 9-word, How-to, Event invite, 8-minute email. Count `{{first_name}}` as 6 characters. Put the emails in date order, spares last. In the JSON, write every `<` as `<`.
3. Replace `__EMAIL_DATA__` with the JSON and `__PAGE_TITLE__` with `<title> · Email preview`. Change nothing else in the template.
4. Save it where the script would, and give them the path.

## What they will see (tell them in one or two lines)

- **Desktop:** an inbox list. Click an email to read it as it will arrive. Brackets to fill in are highlighted.
- **Phone:** the same inbox in a phone frame, so they can see where each subject gets cut off.
- **Beside each email:** the rating and how it climbed, the subject options with coloured counts (green fits every phone, amber is cut off in the Gmail app, red is too long), how it looks on a phone, the fill-in list, and the copy buttons.
- **Copy for GoHighLevel / Mailchimp / ActiveCampaign:** copies the subject, preview text and email with the first name tag changed for that tool. The small buttons copy one field at a time. If brackets are still in the email, it asks before copying. After copying, it shows the first-name fallback tip for that tool.

Then: "Read each one out loud before you paste it."
