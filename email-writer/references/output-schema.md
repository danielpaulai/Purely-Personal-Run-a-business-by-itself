# Output contract (shared by the room, the plugin and the tests)

Every AI call returns one JSON object. No text around it.

## Email object

```json
{
  "type": "client_win | story | nine_word | how_to | event_invite | eight_minute_edit",
  "sequence_step": 0,
  "name": "short internal name, e.g. 'Client Win · Cohort 01'",
  "subject_options": [
    { "text": "subject line", "angle": "moment | label | problem" }
  ],
  "recommended_subject": 0,
  "recommended_reason": "one short line",
  "preview_text": "40 to 90 characters",
  "body": "the full email body as plain text, paragraphs separated by a blank line, starting with the greeting and ending with the sign-off",
  "ps": "starts with 'PS', or empty string. Always empty for nine_word and event_invite",
  "cta": "the one ask, e.g. 'Reply Circle'",
  "side_idea": "a second idea saved for next week, or empty string",
  "fill_in": ["placeholders the founder must fill, e.g. '[client first name]', and checks, e.g. 'Confirm $49 is still the price'"]
}
```

- `sequence_step` is 1, 2 or 3 for event_invite emails, 0 for everything else.
- `recommended_subject` is the index (0, 1 or 2) into `subject_options`.
- The greeting uses `{{first_name}}` as the merge field, in the founder's language ("Hey {{first_name}}," in English, "Hallo {{first_name}}," in German). The 9-word email may skip the greeting.

## Task: emails
`{ "emails": [Email, ...] }`

## Task: ideas
`{ "ideas": [ { "title": "...", "angle": "one line: the link to their business", "recipe": "client_win | story | nine_word | how_to | event_invite", "source": "film | child | week | photo | offer | clients | other" } ] }` with exactly 30 ideas.

## Task: edit (the 8-minute email)
`{ "feedback": ["three short, kind, specific notes"], "email": Email }` with `type` = `eight_minute_edit`.
