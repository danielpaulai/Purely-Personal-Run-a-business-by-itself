# Loading emails into your platform

The plugin never connects to your platform and never sends. You paste, you check, you schedule.

Click paths below come from each tool's help pages (checked October 2026). **[CHECK]** marks a step we have not confirmed in a live account. Menus move: if a step does not match what you see, look for the nearest button with the same word, and tell Danny's team so we can fix this page.

## Before any platform: the same 5 checks

1. Every `[bracket]` is filled in. The preview highlights them, and the copy buttons ask before copying while any are left.
2. You read it out loud once.
3. It goes to your **newsletter** tag (or audience) only. Never to all your contacts.
4. You send a test to yourself first and read it on your phone.
5. You schedule it. You do not need to press send now.

Links: write them as full `https://` addresses in the plain text. Copy plain text only (the preview's copy buttons do this).

## The first name, and what happens when it is missing

The plugin writes `{{first_name}}`. The preview's copy buttons change it for you. Set a fallback once, so a contact with no first name does not see "Hey ,".

| | GoHighLevel | Mailchimp | ActiveCampaign |
|---|---|---|---|
| First name | `{{contact.first_name}}` | `*\|FNAME\|*` | `%FIRSTNAME%` |
| Fallback | Click the first name tag in the editor, set **Default Text** to "there" | Set a default first name ("there") in your audience fields | Check contacts without a first name before you send. Advanced: `%IF $FIRSTNAME != ''%Hey %FIRSTNAME%,%ELSE%Hey there,%/IF%` [CHECK: test it on yourself first] |

A subject that is only `{{first_name}}` (the 9-word email) goes blank for contacts with no name. Set the fallback before you schedule it.

## GoHighLevel

**Once, to make a plain text template** (so every email looks like a personal note):
Marketing > Emails > Templates > **+ New** > from scratch > **Plain Text**.

**Each email:**
1. Marketing > Email > **Campaigns** > **New Campaign**. Pick your plain text template.
2. In the preview, open the email and use **Copy for GoHighLevel**, or the three small buttons one at a time. Paste the **body** into the text area.
3. Click **Preview and Test Email** and send a test to yourself. Read it on your phone.
4. Click **Send or Schedule**. This screen holds the sender, the **subject**, the **preview text** and the recipients. Paste the subject and preview text here. [CHECK: where the preview text field sits for a plain text campaign]
5. Recipients: choose your **newsletter** tag (a tag filter or a smart list). [CHECK: whether the picker takes a tag directly]
6. Choose **Schedule**, set the day and time from your calendar.md, confirm.

Good to know:
- Sends go out in your sub-account's time zone.
- You can't change a schedule within 1 hour of the send.
- Skip **Batch** and **Smart Send** for now.
- Add a tag: Contacts > Tags > **Add Tag**. For many contacts: select them, then **Add Tag**.

**9-word emails:** send them as a campaign to the newsletter tag, or one at a time from **Conversations** to people you know, as a personal email.

## Mailchimp

1. **Create** > **Email** > **Plain text**.
2. **To:** your audience, then the **newsletter** tag (or a segment).
3. **Setup:** paste the **subject**, the **preview text**, and check **From** is your first name and your own domain address.
4. Click **Copy for Mailchimp** in the preview. Paste the body **above the footer** (Mailchimp adds the unsubscribe link and your address in the footer for you).
5. **Preview and Test**: send a test to yourself. Read it on your phone.
6. **Send** or **Schedule**.

**The free plan cannot schedule** (it allows 250 contacts and 500 sends a month). On the free plan, send each email on its day from your calendar.md, or move to Essentials to schedule.

## ActiveCampaign

1. **Campaigns** > **Create** > **Standard**.
2. **Recipients:** your list, filtered to the **newsletter** tag.
3. **Settings:** paste the **subject**, and the preview text into **preheader** (ActiveCampaign's name for preview text).
4. **Design:** use the **Email Designer** with **one text block**. Do not use **Text Only**: it has no preheader field, and the first name tag may not work there.
5. Click **Copy for ActiveCampaign** in the preview and paste the body into the text block.
6. Send a test to yourself. Read it on your phone.
7. **Campaign Summary**: schedule it for the day and time in your calendar.md.

## Other platforms

Use **Copy plain text** and replace `{{first_name}}` with your platform's first name tag. Search your platform's help for "merge tag" or "personalization".

## Event invite emails (the three-email set)

- **Email 1 (the invite):** schedule it to your newsletter tag like any other email.
- **Email 2 (the details):** do not schedule it. When someone replies "yes" or "tell me more", reply to them personally and paste email 2 into your reply. Tag them **event-yes**.
- **Email 3 (the check in):** three days after email 1, send it to your newsletter tag, leaving out people tagged **event-yes**. [CHECK: the exclude-a-tag filter in each tool]

## After you schedule

Change `status: draft` to `status: scheduled` in the email file (or say "I scheduled them" and the plugin will do it). On Friday, `email-scoreboard` moves the sent ones into `sent/`.

## Spam, in one line

Words rarely send you to spam. Who you send to matters most: only people who said yes, from your own domain.
