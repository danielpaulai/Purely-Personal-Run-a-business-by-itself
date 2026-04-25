# Voice Rules

The discipline for all generated copy. The new workshop must sound like the same person as Workshop 01.

---

## Read BUSINESS-BRAIN.md first

Voice is not invented. Voice is read from the user's `BUSINESS-BRAIN.md`:

- **Tone** · 1–3 sentences describing the user's voice
- **Banned phrases** · exact strings that must never appear in output
- **Hook patterns** · 5 formulas the user uses to open posts/scripts
- **Example openings** · 3+ real excerpts that demonstrate the voice

If any of these are missing from the Brain, the user has not finished their `/build-my-brain` work. Stop and tell them.

---

## Universal banned phrases (always enforce, even if not in Brain)

Never use these. They're AI tells:

- `unlock`
- `delve`
- `delving`
- `dive into`
- `seamless` / `seamlessly`
- `supercharge`
- `elevate` / `elevating`
- `leverage` (as a verb)
- `tapestry`
- `realm`
- `landscape` (figurative)
- `journey` (when not literal)
- `unleash`
- `synergy`
- `holistic`
- `cutting-edge`
- `state of the art`
- `revolutionize`

If the user's Brain has additional banned phrases, merge with this list.

---

## Punctuation rules

### Em-dashes · banned

Replace with:
- Period: `Day 1 marketing. Day 2 sales.`
- Middle dot: `Day 1 marketing · Day 2 sales`
- Comma: `Day 1 marketing, Day 2 sales`

Example fix:
- ❌ `5 jobs — one person — and things slip` (em-dashes)
- ✅ `5 jobs · one person · and things slip` (middle-dot)
- ✅ `5 jobs by one person. Things slip.` (periods)

### Triple parallel structure · banned in headlines

The Brain says no parallel tricolons. Don't write:
- ❌ `Day 1: X. Day 2: Y. Day 3: Z.`

Two-part is fine:
- ✅ `Day 1: marketing. Day 2: sales.`

### Aphorisms · banned

Don't write:
- ❌ `One word: systems.`
- ❌ `Here's what nobody tells you.`
- ❌ `The secret? Discipline.`

Just say the thing.

---

## Sentence patterns to use

From Workshop 01's VSL (Danny's voice):

- **Short declarative.** "Last year I was doing 5 full-time jobs by myself."
- **Specific number + period.** "Cost: zero dollars a month."
- **Contrast pair.** "I wasn't lazy. I was one person doing 5 jobs."
- **List of three with commas.** "Marketing. Sales. Operations."
- **Repetition for rhythm.** "Content would slip. Prospecting would slip. Invoicing would slip."

Avoid:
- Long sentences with multiple clauses
- Adverb stacking ("really effectively properly")
- Vague qualifiers ("many", "lots", "several")

---

## Hook patterns (use one per opener)

From Workshop 01's Brain:

1. **Personal proof hook** · "Last year I was doing 5 full-time jobs by myself."
2. **Quiet truth hook** · "Most founders use AI like a search engine."
3. **Stat contrast hook** · "$200/month on AI tools. Still wrote at midnight."
4. **Contrarian hook** · "Claude isn't a search engine. Claude is a business partner." (note: this one was flagged in v1 as too AI · example of how subtle the banned-pattern detection has to be)
5. **Reframe hook** · "I wasn't lazy. I was one person doing 5 jobs."

For the new workshop's VSL, pick the hook pattern that best fits the user's CORE_HOOK from Q7. If unsure, use Personal Proof or Stat Contrast · those are the user's natural defaults.

---

## What to copy from the user's voice (the things AI gets wrong)

When generating prose, mimic these patterns from Workshop 01:

### 1. Specifics, not generalities
- ❌ "lots of time" / "many tools" / "several methods"
- ✅ "12 hours a week" / "$200/month" / "5 different tools"

### 2. Names + amounts in the first 30 seconds
- VSL opener literally names: 5 jobs, January, BUSINESS-BRAIN.md, 9 sections, 5 slash commands.
- Don't write a 30-second opener without a number, a date, and a noun (file/tool/place).

### 3. Reframe instead of explanation
- ❌ "It's important to have systems because they help you scale efficiently."
- ✅ "I wasn't lazy. I was one person doing 5 jobs."

### 4. Action verbs at sentence start
- ❌ "Then we'll go ahead and start building..."
- ✅ "We build."

### 5. The "while I sleep" / "before coffee" pattern
- VSL ends with "5 AI executives. Running every week. While I sleep."
- Use a comparable concrete-result phrase in the new VSL.

---

## Anti-patterns specific to AI-generated copy

When you generate the VSL, DMs, voiceover, etc., watch for these:

| Pattern | Why it's AI |
|---------|-------------|
| "Imagine a world where..." | AI clickbait |
| "What if I told you..." | AI clickbait |
| "Here's the thing:" | AI clickbait |
| "The truth is..." | AI clickbait |
| "Game-changing" / "game-changer" | hype, not voice |
| Adverb-noun pairs ("incredibly powerful tool") | AI fluff |
| "Streamline" / "optimize" / "transform" without specifics | AI fluff |
| Lists of 5+ items with no numbers | AI list-spam |
| "From X to Y" headlines | LinkedIn cliché |
| "I went from X to Y in N days" with a fake metric | invented testimonial |

If you catch yourself generating any of these, stop and rewrite using the user's voice patterns above.

---

## Validation step

After generating any copy, run this self-check:

1. Search for em-dash characters (Unicode U+2014). Replace with middle-dot `·` or period.
2. Search for each universal banned phrase. Rewrite if found.
3. Search for each Brain-specific banned phrase. Rewrite if found.
4. Count specifics in the first 100 words: at least 2 numbers, 1 named thing, 1 specific amount/date.
5. Check sentence length: no sentence over 30 words.
6. Check for tricolons: no `X. Y. Z.` parallel structure if all three are similar.
7. Check for aphorisms: no `Here's the [secret/thing/truth]` openers.

If any check fails, rewrite that section before outputting.

---

## When in doubt

Read 3 sample outputs from the existing Workshop 01:
- `purely-personal/campaign/vsl-script.md` (the VSL)
- `purely-personal/campaign/email-campaign.md` (Email A1, A2)
- `purely-personal/campaign/dm-outreach.md` (Segment A opener)

Match that voice. Match that pace. Match that level of specificity.

If the new workshop's hook is fundamentally different (e.g., user says "scale to 6 figures" instead of "stop being the bottleneck"), the prose adapts to the new hook · but the SOUND of the voice (sentence length, specificity, no em-dashes, hook patterns) stays the same.
