---
name: linkedin-cheatsheet-builder
description: Build LinkedIn cheatsheets using one of 3 Purely Personal templates. Listicles (6 main points × 4 takeaways, intent-driven), Comparison (X vs Y / Bad vs Good / Think vs Reality tables), or Dos-and-Don'ts (Classic / Side-by-Side / Numbered Countdown). Every cheatsheet is voice-matched, save-worthy, and designer-ready. Use when creating saveable LinkedIn reference content, building comparison tables, listing best practices, or producing high-utility content that earns repeated saves. Triggers on "build a cheatsheet", "cheatsheet about", "make a comparison table", "dos and don'ts", "listicle for LinkedIn", "reference graphic".
version: 1.0.0
author: daniel-paul
tags: [linkedin, cheatsheet, content, voice, ai-marketing-employee, comparison, dos-donts]
---

# LinkedIn Cheatsheet Builder

Three templates for LinkedIn cheatsheets, sourced from Purely Personal's Content Prompts library. Every cheatsheet is intent-driven, voice-matched, and built for one specific reader behavior: **save + reference + share**.

This skill runs inside the AI Marketing Employee Project. Voice Profile auto-loads from Project Knowledge.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "make me a cheatsheet" and you get a generic numbered list with no structure, no intent, no progression. Reads as "5 tips" content. Nobody saves it. Nobody shares it.

**This skill provides:**
1. **3 distinct cheatsheet formats**. Listicles (base), Comparison (3 sub-variants), Dos-and-Don'ts (3 sub-variants) = 7 actual structural templates
2. **5 intent-driven progression frameworks** (Listicles). each intent has a specific 6-point logical path so the cheatsheet reads as ONE argument, not 6 separate posts
3. **Format selection decision tree**. when to use which format based on the content shape
4. **Strict design-friendly output**. head/sub/main-point/takeaway structure with → arrows (not bullets) so designer pastes directly to Canva
5. **Niche specificity requirement**. refuses generic language when niche-specific terms exist
6. **Technical terms preserved**. client's industry vocabulary stays exact ("API integration," "EMR integration," etc.)
7. **Save-worthiness check**. every line passes "So what?" test (could the reader DO something specific?)

**You can replicate this with ChatGPT if you:** memorize 3 formats × 5 intents × progression frameworks × format selection rules × format-specific structures × forbidden patterns. This skill does it in 90 seconds.

---

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| Voice Profile | AI Marketing Employee Project Knowledge | STOP. run `voice-profile-builder` first |
| Topic | User input | Ask: "What's the cheatsheet about?" |
| Format | User input (or recommend via decision tree) | Default to Listicles |
| Reference Context | User input or Project Knowledge | Anti-hallucination: refuse without sufficient source |
| Sub-variant (Comparison/Dos-Don'ts) | User input or inferred | Apply decision tree |

---

## Mode

| Mode | Bundled prompt | Best for |
|------|-------------|----------|
| `listicles` (default) | `prompts/listicles.md` | Standard 6-point cheatsheet with intent-driven progression. Most common format. |
| `comparison` | `prompts/comparison.md` | Comparison table. 3 sub-variants: X vs Y / Bad vs Good / Think vs Reality |
| `dos-and-donts` | `prompts/dos-and-donts.md` | Right vs wrong practices. 3 sub-variants: Classic / Side-by-Side / Numbered Countdown |

**Default: `listicles`**. works for 60% of topics. Switch when:
- Topic is a comparison → `comparison` mode
- Topic is practices/methods → `dos-and-donts` mode

---

## Format Selection Decision Tree

Run before picking a mode:

1. **Is this a comparison between two equivalent things?** → `comparison` mode → Format 1 (X vs Y)
2. **Is this showing right vs wrong (where each wrong has a clear right)?** → `comparison` mode → Format 2 (Bad vs Good) OR `dos-and-donts` mode → Format 2 (Side-by-Side)
3. **Is this debunking common beliefs?** → `comparison` mode → Format 3 (Think vs Reality)
4. **Are mistakes worth ranking by severity?** → `dos-and-donts` mode → Format 3 (Numbered Countdown)
5. **Are practices distinct (no 1:1 pairing)?** → `dos-and-donts` mode → Format 1 (Classic)
6. **Is this a teaching/insight piece with logical progression?** → `listicles` mode (intent drives progression)

---

## Process

### Phase 1. Validate inputs
1. Voice Profile present?
2. Topic + reference context sufficient?
3. Mode picked (run decision tree if not)?
4. Sub-variant picked (Comparison / Dos-Don'ts only)?

### Phase 2. Load bundled prompt
- `listicles` → `prompts/listicles.md`
- `comparison` → `prompts/comparison.md`
- `dos-and-donts` → `prompts/dos-and-donts.md`

### Phase 3. Apply prompt template
Follow the bundled prompt exactly:
- **Listicles:** Choose intent → apply progression framework → write Head + Sub + 6 main points × 4 takeaways
- **Comparison:** Pick sub-variant → select 6-8 categories → fill table → add closing element (Similarities / Keywords / Bottom Line)
- **Dos-and-Don'ts:** Pick sub-variant → write content per format → add closing element (Bottom Line / The Shift / Wake-Up Call)

### Phase 4. QA checks
Apply format-specific quality checks (8-12 per format). See bundled prompts for full lists.

Key universal checks:
- Could the client defend every line?
- Are technical terms preserved exactly?
- Could a designer paste this to Canva with zero clarification?
- Does the cheatsheet earn the SAVE action?

### Phase 5. Deliver
Markdown-formatted cheatsheet, designer-ready.


---

## Output Structures

### Listicles output:
```
HEAD: [8-10 word title]
SUBHEADING: [10-12 word "why care now"]

MAIN POINT 1: [6-8 word headline]
→ [Takeaway 1 - 10-12 words]
→ [Takeaway 2]
→ [Takeaway 3]
→ [Takeaway 4]

MAIN POINT 2: [...]
→ [...]
[...]

[6 main points × 4 takeaways = 24 takeaways total]
```

### Comparison output (Format 1: X vs Y):
```
[Title]: [Concept X] vs. [Concept Y]

| Category | [X] | [Y] |
|---|---|---|
| [Cat 1] | • [point]<br>• [point] | • [point]<br>• [point] |
[6-8 rows]

**Similarities:** [3-4 bullets]
```

### Dos-and-Don'ts output (Format 3: Numbered Countdown):
```
[N] [Topic] Mistakes Killing Your [Outcome] (Ranked)

| # | The Mistake | Why It's Not Working | What to Do Instead | The Result |
|---|---|---|---|---|
| #5 | ... | ... | ... | ... |
| #4 | ... | ... | ... | ... |
| #3 | ... | ... | ... | ... |
| #2 | ... | ... | ... | ... |
| #1 | ... | ... | ... | ... |

🎯 The Wake-Up Call: [12-18 words urgent message]
```

---

## Examples

> **Illustrative only.** The names, numbers and results in the examples below are invented to show the format. Never reuse them. In real output use only facts from the operator's Business Brain or from the request, and leave a detail out rather than make one up.

### Example 1. Listicles · Educating intent

**Input:** Topic: "The 6-step process to install an AI Marketing Employee." Intent: Educating.

**Output:**
```
HEAD: The 6-Step Process to Install Your AI Marketing Employee
SUBHEADING: From voice profile to first 4/4 post — in 30 minutes.

MAIN POINT 1: Capture your voice from 4 inputs
→ Paste 20 past LinkedIn posts written by you (even the flops)
→ Add 3 transcribed voice notes (the rambling ones)
→ Include 10 DM replies you sent to actual clients
→ Drop your top 10 FAQ + answers as you'd actually say them

MAIN POINT 2: [...]

[... 6 main points × 4 takeaways]
```

### Example 2. Comparison · Bad vs Good

**Input:** Topic: "Bad vs Good LinkedIn carousels." Format 2.

**Output:** 6-row table comparing 6 carousel mistakes with their fixes, plus negative/positive keyword tags.

### Example 3. Dos-and-Don'ts · Numbered Countdown

**Input:** Topic: "5 LinkedIn voice mistakes killing your inbound." Format 3.

**Output:** 5-row priority table with The Mistake / Why / What Instead / Result + 🎯 Wake-Up Call.

---

## Limitations

- **Won't design the visual layout.** Output is structured content + design notes. Designer (Canva/Figma) does layout.
- **Won't padding to hit count.** If only 4 main points are strong, the skill writes 4 and notes "padded to 6 would weaken the cheatsheet."
- **Won't invent practices/data.** Anti-hallucination applies. refuses without source.
- **Won't mix formats.** One format per cheatsheet. Mixing dilutes the impact.

---

## Pro Tips

1. **Listicles + Educating intent is the most reliable.** Default to this combo when unsure.
2. **Comparison tables get the most saves.** The "Bad vs Good" format especially. People love seeing what they're doing wrong.
3. **Numbered Countdown is best for urgency.** Use when you want to drive action, not just teach.
4. **Always end with a closing element.** Bottom Line / Shift / Wake-Up Call. The closing line is what people quote when they share.
5. **Niche specificity beats clever copy.** "B2B SaaS founders" beats "founders". Be specific in title.
6. **Save the cheatsheet output.** Designer can re-use the markdown if you want to refresh the cheatsheet in 90 days.

---

## Quality Checklist (built into Phase 4)

- [ ] Format choice matches the content shape (decision tree run)
- [ ] Head is 8-10 words (Listicles) or per format (Comparison/Dos)
- [ ] Subheading / closing element present
- [ ] All takeaways start with → arrow (NOT bullets, NOT "Key takeaway")
- [ ] Every line is specific enough to be wrong
- [ ] Technical terms preserved exactly
- [ ] Niche-specific language (not generic "professionals")
- [ ] Designer-ready (no extra commentary)
- [ ] Voice match: client could publish without editing

---

## Canva AI handoff

After generating the cheatsheet content, append the Canva AI design prompt from `prompts/canva-cheatsheet.md` to the output. The user copies the cheatsheet copy into the `[PASTE CHEATSHEET COPY HERE]` block, pastes the whole prompt into Canva AI, and gets a polished editorial-style cheatsheet in under 5 minutes.

The Canva prompt is brand-locked to Purely Personal (red #e90d41, off-white #f7f7f8, near-black #0a0a0a, Rethink Sans + Inter + JetBrains Mono). It produces:
- Vertical 1080x1350 format (LinkedIn-optimal)
- Strong title at the top with a 4px red underline
- Numbered sections with thin-line custom icons
- Editorial composition (Monocle / NYT briefing feel)
- Thin red strip at the bottom with author name + handle

Always emit this prompt as a separate "Copy Canva AI prompt" block at the bottom of the cheatsheet output. Same pattern as `weekly-content-engine`.

---
## Use in the Purely Personal connector


After the draft: Write the matching post with write_post. Run the whole week at once with weekly_content_drop.
