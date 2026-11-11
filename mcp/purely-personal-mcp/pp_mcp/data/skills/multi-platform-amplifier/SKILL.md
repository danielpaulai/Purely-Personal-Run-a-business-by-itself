---
name: multi-platform-amplifier
description: Take one LinkedIn post and instantly produce platform-native versions for X (Twitter thread), Instagram (caption), Reels/TikTok (60-90 sec script), and Threads. Each version preserves the user's voice + ICP anchor but adapts hook, format, length, and CTA to the platform's algorithm + culture. Use when the user wants to amplify one post across multiple platforms, batch a week of content from one idea, or maximize content ROI without writing 4 separate pieces. Triggers on "amplify this post", "turn this into a thread", "Instagram version", "Reels script", "Threads version", "multi-platform", "repurpose this", "1 post 4 platforms".
version: 1.0.0
author: daniel-paul
tags: [linkedin, twitter, instagram, reels, threads, content, ai-marketing-employee, repurpose]
---

# Multi-Platform Amplifier

The skill that takes ONE LinkedIn post and produces native versions for **X · Instagram · Reels · Threads**. each adapted to its platform's algorithm, format constraints, and audience culture. Same idea. Same voice. 4× the reach.

This is the second highest-use skill in the AI Marketing Employee toolkit (after `prospect-magnet`). The user spends 5 minutes writing one post; the AI Employee gives them a week of cross-platform content.

---

## Why This vs ChatGPT?

**Problem with raw ChatGPT:** Ask "turn this LinkedIn post into a Twitter thread" and you get a 7-tweet thread that's just the LinkedIn post sliced into chunks. Each tweet ends mid-thought. The hook doesn't work on X. The thread doesn't earn the swipe. And ChatGPT defaults to Instagram captions that are too long, Reels scripts that have no visual cues, and Threads versions that are just LinkedIn copy-pastes.

**This skill provides:**
1. **Platform-native rewriting**. not just chunking. The X thread has X-native hook patterns ("Most people get this wrong:"). The Instagram caption has Instagram-native format (hook + breakroom + CTA + 5-10 hashtags). The Reels script has visual + audio cues. Each version is built for the platform.
2. **Voice preservation across formats**. pulls from the user's Voice Snapshot + ICP so vocabulary, beliefs, and rhythm stay consistent even when the structure changes
3. **4 platform-specific frameworks**. each based on the high-performing content patterns for 2026
4. **Cross-platform CTA strategy**. same DM keyword + same offer across all 4 platforms so inbound is consolidated, not fragmented
5. **Visual side-by-side artifact**. 4-column comparison so the user can SEE how the same idea adapts to each platform's culture
6. **Hashtag intelligence**. Instagram + Threads versions include hashtag mixes (3 niche + 3 medium + 3 broad) improved for 2026 algorithm

**You can replicate this with ChatGPT if you:** memorize 4 platform-specific format guides, hashtag strategy, hook patterns per platform, length constraints, native CTA formats, and visual cue conventions for video. Then apply consistently while preserving voice. Takes 60-90 min per multi-platform set. This skill does it in 45 seconds.

---

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| The LinkedIn post | User input. ideally from `linkedin-post-writer` output | Ask: "Paste the LinkedIn post you want to amplify" |
| Voice Snapshot or Voice DNA | AI Marketing Employee Project Knowledge | STOP. run `voice-profile-builder` first |
| ICP (for CTA + hashtag targeting) | Project Knowledge | STOP. run ICP Builder first |
| DM keyword | Pulled from the LinkedIn post automatically | If not detected in post: ask "What DM keyword should the CTAs use?" |

---

## Mode

| Mode | What you get | Best for |
|------|---|---|
| `core` (default) | X thread + Instagram caption + Reels script · 3 platforms | Daily content amplification |
| `full` | Core + Threads version · 4 platforms | Full cross-platform week from one post |
| `video-first` | Reels/TikTok script + visual storyboard + voiceover script | When the content is video-native (talking head, screen recording) |
| `visual` ★ | Full mode + HTML 4-column side-by-side artifact with all platforms rendered as platform mockups (LinkedIn, X, Instagram, Reels) | Demos · screenshots · designer handoff · daily preview |

**Default: `core`**. covers 80% of use cases. Switch to `full` when launching a campaign, `video-first` when content is video-native.

---

## Platform Adaptation Rules

### LinkedIn (source. already exists, used as anchor)
- 150-word post · framework/story/intent-driven
- Voice + POV + Specificity + Asking (4/4 on Invisibility Diagnostic)
- DM keyword in last 2 lines

### X / Twitter Thread (5-7 tweets)
- **Hook tweet:** 1 sentence, under 240 chars, contrarian or curiosity-driven
- **Body tweets:** 1 idea per tweet · max 280 chars · short sentences
- **Closing tweet:** Recap + DM keyword + "Follow @[handle] for more on [niche]"
- **No hashtags in threads** (X algorithm 2026 deprioritizes them)
- Hook patterns: "Most [niche] get this wrong:" / "I just [outcome]. Here's how:" / "Stop [common action]. Do this instead:"

### Instagram Caption (1,500-2,200 chars, longer = better in 2026)
- **Hook line:** First 125 chars (above-the-fold before "more")
- **White space + line breaks** every 1-2 sentences (mobile-readability is the algorithm signal)
- **Story-driven** even if educational (Instagram users want narrative)
- **DM CTA + question CTA** (double CTA. Instagram allows both)
- **Hashtag mix:** 9-12 tags · 3 niche (under 50K posts) + 3 medium (50K-500K) + 3 broad (500K+) · placed at end after a "." separator line

### Reels / TikTok Script (60-90 seconds)
- **Hook (0-3 sec):** Visual + audio · "Most coaches [common mistake]" said while pointing to camera
- **Setup (3-15 sec):** Problem context + visual proof (text overlay)
- **Body (15-60 sec):** 3-5 quick beats · cuts every 2-3 sec · visual cues per beat
- **CTA (60-75 sec):** "DM me [keyword] for the [thing]" said clearly + text overlay
- **End screen (75-90 sec):** Logo + handle + "follow for more"
- Format: 9:16 vertical
- Captions/subtitles MANDATORY (80% of viewers watch muted)

### Threads (Meta's X competitor, growing fast in 2026)
- Similar to X but allows 500 chars per post (vs 280 on X)
- More casual tone · Threads culture is "less polished than X, more thoughtful than IG"
- Hook patterns: "I'm seeing a pattern:" / "Genuine question:" / "Hot take you'll disagree with:"
- 1-3 follow-up posts (Threads users like single posts more than long threads)
- Soft CTA · "DM if this resonates" works better than aggressive asks

---

## Process

### Phase 1. Validate inputs
1. LinkedIn post provided? If not → ask.
2. Voice Snapshot in Project Knowledge? If not → STOP, run `voice-profile-builder`.
3. ICP in Project Knowledge? If not → STOP, run ICP Builder.
4. Extract DM keyword from LinkedIn post (look for "DM me 'X'" pattern). If not found → ask.

### Phase 2. Extract the core idea
1. Identify the central insight / story / framework in the LinkedIn post
2. Extract: hook line · POV line · 1 specific (name + number) · CTA keyword

### Phase 3. Adapt per platform

For each platform (X · Instagram · Reels · Threads):
1. Rewrite hook using platform-native pattern
2. Restructure body using platform format constraints
3. Adapt CTA to platform conventions
4. Add platform-specific elements (hashtags for IG/Threads, visual cues for Reels, character limits for X)
5. Preserve voice (vocabulary + rhythm from Voice Snapshot)
6. Preserve POV (use one of the user's top 3 beliefs as anchor)

### Phase 4. Quality check each version
For each platform, verify:
- [ ] Voice matches Voice Snapshot
- [ ] POV anchored to one of user's beliefs
- [ ] Platform-native hook (not LinkedIn hook reused)
- [ ] Platform-native CTA (consistent DM keyword across all)
- [ ] Length within platform sweet spot
- [ ] No banned words from Voice Snapshot
- [ ] No AI tells (use, open up, handle, etc.)

### Phase 5. Render output

**Text mode:** 4 platforms in markdown with clear separators.
**Visual mode:** HTML artifact with 4 mockup cards (LinkedIn / X / Instagram / Reels) side-by-side.

### Phase 6. Suggest next steps

> *"Multi-platform set ready. Suggested deployment cadence:*
> *Day 0 (Monday): publish LinkedIn original*
> *Day 1 (Tuesday): publish X thread*
> *Day 2 (Wednesday): publish Instagram caption*
> *Day 3 (Thursday): publish Threads version*
> *Day 4 (Friday): publish Reels (highest production cost → end of week)*
> *Same DM keyword across all 4 = consolidated inbound."*

---

## Output Structure (`core` mode, text)

```
MULTI-PLATFORM AMPLIFIER
Source post: "[first 80 chars of LinkedIn post]..."
Voice: [user name] · ICP: [ICP summary]
DM keyword: [keyword]

═══════════════════════════════════════════
🐦 X / TWITTER THREAD (6 tweets)
═══════════════════════════════════════════

1/6 [hook tweet, under 240 chars]

2/6 [body tweet]

3/6 [body tweet]

4/6 [body tweet]

5/6 [body tweet]

6/6 [closing + DM CTA + follow ask]

═══════════════════════════════════════════
📸 INSTAGRAM CAPTION (1,847 chars)
═══════════════════════════════════════════

[Hook line — first 125 chars]

[Body with line breaks every 1-2 sentences...]

[Story/lesson...]

[Double CTA — DM keyword + question]

.
.
.
#niche1 #niche2 #niche3
#medium1 #medium2 #medium3
#broad1 #broad2 #broad3

═══════════════════════════════════════════
🎬 REELS / TIKTOK SCRIPT (75 sec)
═══════════════════════════════════════════

[0-3 sec — HOOK]
Visual: [direction]
Audio: "[spoken line]"
Text overlay: "[on-screen text]"

[3-15 sec — SETUP]
Visual: [direction]
Audio: "[spoken line]"
Text overlay: "[on-screen text]"

[15-45 sec — BODY · 3 beats]
[Beat 1: visual + audio + overlay]
[Beat 2: ...]
[Beat 3: ...]

[45-75 sec — CTA + END]
Visual: [direction]
Audio: "DM me '[keyword]' for [thing]"
Text overlay: "DM '[keyword]'"

[End screen: logo + handle]

═══════════════════════════════════════════
NEXT MOVES:
- Deploy cadence: 1 platform/day across 5 days (consolidated inbound)
- Same DM keyword across all 4 → consolidated tracking
- Run prospect-magnet on the LinkedIn version to add outbound layer
```

## Output Structure (`visual` mode)

HTML artifact: 4 platform mockup cards (LinkedIn / X / Instagram / Reels) side-by-side with the rewritten content rendered in platform-native styling. Each card has a "Copy" button. KPI strip at top showing reach multiplier (1 → 4 platforms = ~4× audience reach for same content effort).

See `scripts/render.py` + `scripts/template.html`.

---

## Examples

### Example 1: Coach niche, core mode

**Input LinkedIn post:**
> "I told a coaching client to stop posting daily. She'd been posting for 6 months. 11 likes total. The problem wasn't her schedule. it was that nothing she wrote sounded like her. DM 'voice' for the worksheet."

**Output (X thread, 6 tweets):**
```
1/6 Most coaches think posting daily is the answer.
It's not.
A client of mine posted daily for 6 months. 11 likes total.

2/6 Here's what we changed:
Stop posting until your voice is locked.

3/6 Voice profile from 4 inputs:
- 20 of your real past posts
- A 90-sec rambling voice note
- 10 DM replies you sent clients
- Your top 10 FAQ answers

4/6 Run those through Claude with the right prompt.
Get back a Voice DNA doc.
Paste it as Project Knowledge.

5/6 Now every post sounds like YOU.
The client I told to stop?
First inbound DM in 4 months by Tuesday.

6/6 DM me 'voice' if you want the worksheet I gave her.
Follow for more on AI Marketing Employees → @danielpaulai
```

**Output (Instagram caption):** Same idea, 1,800-char story-driven version with line breaks every 2 sentences + 9 hashtag mix.

**Output (Reels script):** 75-sec video script with cuts every 3 sec, text overlays per beat, hook → setup → 3 beats → CTA.

### Example 2: B2B SaaS, video-first mode

**Input LinkedIn post:** SDR replacement story (replace 7 SDR emails with one AI agent).

**Output:** Full 90-sec Reels script with visual storyboard (screen recording of Claude + b-roll suggestions + voiceover script + on-screen metrics overlay).

---

## Chains With Other Skills

| Upstream | How |
|---|---|
| `linkedin-post-writer` | Provides the source LinkedIn post |
| `voice-profile-builder` (or Voice Snapshot) | Required. provides voice consistency across platforms |
| ICP Builder | Required. provides CTA + hashtag targeting context |

| Downstream | How |
|---|---|
| `prospect-magnet` | Run on the LinkedIn version → 10 prospects + DMs (closes content → pipeline loop) |
| `invisibility-diagnostic` | Score the LinkedIn version (other platforms have different scoring rubrics) |
| Day 2 Writing Assistant (deployed) | Run weekly to auto-amplify your Monday post across all 4 platforms on a schedule |

**Suggested chain after output:**
> *"Multi-platform set ready. Next: run `prospect-magnet` on the LinkedIn version to add the outbound layer. Deploy across 5 days (LinkedIn Mon → Reels Fri). Same DM keyword across all = consolidated inbound."*

---

## Limitations

- **Won't generate the actual Reels video.** Output is the script + storyboard + overlay text. User shoots/edits.
- **Won't post for the user.** Output is paste-ready text. User posts manually (intentional. prevents auto-spam at scale).
- **Hashtag intelligence is heuristic.** Uses 2026 Instagram algorithm patterns. Re-check quarterly as platforms shift.
- **No image generation.** For Instagram + Threads visuals, chain to a separate image-prompt skill or use Canva/Figma.

---

## Pro Tips

1. **Deploy across 5 days, not 1.** Don't post all 4 platforms simultaneously. feels spammy + same prospects see the same idea on multiple feeds. Spread across 5 days = 5 separate impressions = compound reach.
2. **Same DM keyword across all.** "DM 'voice'" on every platform = consolidated tracking. Don't fragment with platform-specific keywords.
3. **Pair with prospect-magnet.** LinkedIn post → multi-platform amplification → prospect-magnet outbound. That's the full content engine.
4. **Reels scripts → use a teleprompter.** Read the script naturally, don't memorize. Lower production value, higher authenticity.
5. **Quarterly platform refresh.** Re-read this SKILL.md every 90 days. platform algorithms shift. 2027 hashtag strategy will differ from 2026.

---

## GitHub References

- [**social-media-content-repurposer** (onewave-ai/claude-skills)](https://agentskills.so/skills/onewave-ai-claude-skills-social-media-content-repurposer). community Claude skill that handles cross-platform repurposing · this skill extends with voice/ICP integration
- [**ai-video-repurposing-tools** (jevb51)](https://github.com/jevb51/ai-video-repurposing-tools). survey of 18 AI video tools · informs Reels script structure
- [**Repurpose** (yongliang-wu · AAAI 2025)](https://github.com/yongliang-wu/Repurpose). academic dataset + benchmark for video repurposing · informs platform-native adaptation rules

---

## Bundled Files

```
~/.claude/skills/multi-platform-amplifier/
├── SKILL.md                          (this file)
└── scripts/
    ├── render.py                     (JSON → HTML 4-platform mockup)
    └── template.html                 (visual artifact template)
```

---

*Built for the AI Marketing Employee's content multiplier loop. The skill that turns 1 post into 4× reach without 4× the writing time.*
