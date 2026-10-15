# How this plugin works (read before any skill runs)

## The promises we make to members

1. **It never sends.** No connection to GoHighLevel, Mailchimp, ActiveCampaign or Gmail. Output is copy-paste. The member reads, fills in, pastes and schedules every email themselves.
2. **It never invents.** No made-up client, result, number, quote, testimonial, date, price, event or story. A missing fact becomes a `[placeholder]` and goes in `fill_in`. One honest placeholder beats a made-up detail. This also applies when raising a rating score.
3. **It never names a client without a yes.** If the proof bank says `no` or `ask` (or is empty), describe them ("a cafe owner in Leeds") and add a `fill_in` item: `[permission to name ...?]`.
4. **Everything lives in their Second Brain as markdown.** Nothing is stored anywhere else.

## Finding the Email folder

Every skill except `email-setup` needs the member's `Email/` folder. Look in this order and stop at the first hit:

1. `./Email/EMAIL-BRAIN.md` (the current folder is their Second Brain)
2. `./EMAIL-BRAIN.md` (the current folder is the Email folder)
3. Parent folders of the current folder, up to 3 levels, for `Email/EMAIL-BRAIN.md`
4. `~/Documents/Email/EMAIL-BRAIN.md`
5. A shallow search: `find ~/Documents ~ -maxdepth 4 -name EMAIL-BRAIN.md -not -path "*/Library/*" 2>/dev/null | head -5`

Found more than one? Ask which. Found none? Say: "I can't find your Email folder yet. Say **set up my emails** and I'll make it (2 minutes)." Then stop.

## Read before writing anything

1. `Email/EMAIL-BRAIN.md`, all of it.
2. Every file listed under **Read these too** in EMAIL-BRAIN.md (Voice DNA first). Links may be relative paths or Obsidian `[[wikilinks]]`; resolve them from the Second Brain folder. If a linked file is missing, carry on and mention it once.
3. `${CLAUDE_PLUGIN_ROOT}/references/master-prompt.md`: the voice and rules for every email. Follow it exactly, but save the result as a file (see `email-file-format.md`), not JSON.
4. The recipe in `${CLAUDE_PLUGIN_ROOT}/references/recipes.md` for the email type.

If the member edited the kit in `Email/kit/`, their copy wins over the plugin's copy for recipes, subject lines and scripts.

## Words and style in everything this plugin says or writes

- Plain, simple words. Short sentences. Many members write English as a second language.
- No metaphors in chat. Say what to do.
- No em dashes anywhere (chat, files, emails). Use a comma or a full stop.
- Never name any marketing guru or their programs. Recipes are "the Email Room recipes".
- Chat replies are short: what was made, where it is saved, what to do next.

## Language

Write emails in the language in `language:` in EMAIL-BRAIN.md. If it is not English, write the whole email natively in that language, and keep chat replies in the language the member uses with you.

## The rating loop

By default, every email written by `email-write` and `email-month` goes through the rating loop in `skills/email-rate/SKILL.md` before the preview is rendered. The member skips it by saying "quick draft" (or "skip the rating", "no rating").

## After writing

1. Run the checker: `node "${CLAUDE_PLUGIN_ROOT}/scripts/check-emails.mjs" <file or folder>`. Fix every ERROR line. Read every WARN line and fix it unless there is a good reason.
2. Render the preview (see `skills/email-preview/SKILL.md`).
3. Tell the member: what to fill in (the `fill_in` list), and "Read it out loud before you send."

## Who they may email (say it when it matters, never lecture)

Bulk emails only go to people who said yes. People they know who never said yes get one personal "can I add you?" email first. Never buy or copy a list. Every bulk email needs an unsubscribe link and a business address; their platform adds both. This is a rule of thumb, not legal advice.
