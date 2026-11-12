#!/usr/bin/env python3
"""Clean the bundled program skills for use inside the connector.

The skills are authored in Drive for a live cohort and a desktop setup. Bundled here they have known defects
(documented in AUDIT.md, "Skill bundle review"):

  1. banned-word lists garbled by a find-and-replace ("use, open up, big, help, path, go deep ...")
  2. post length targets that contradict each other (1300-1500 chars vs 150 words vs under 220 words)
  3. (scorer looseness is fixed in code, scoring.py)
  4. advice and examples that break the skills' own anti-invention rule, plus unsubstantiated claims
  5. sample copy that breaks the style rules (filler markers, "it's not X, it's Y", long carousel slides)
  6. references to files, skills and tools that do not exist in the connector (render.py, ~/.claude, ICP Builder ...)
  7. cohort-specific details (CET times, "Day 2 stage", attendee counts)

This script applies the fixes. It is idempotent: run it again after re-syncing a skill from Drive and the same fixes apply.
Every exact-text edit must either apply or already be applied; anything else is reported and the script exits non-zero,
so a changed upstream skill never silently skips a fix.

    python scripts/clean_skills.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "pp_mcp" / "data" / "skills"
problems: list[str] = []

CONNECTOR_TOOL = {
    "linkedin-post-writer": "write_post", "linkedin-carousel-builder": "write_carousel", "linkedin-cheatsheet-builder": "write_cheatsheet",
    "weekly-content-engine": "weekly_content_drop", "multi-platform-amplifier": "amplify_post (also write_tweet, write_ig_caption, write_reel_script)",
    "competitor-x-ray": "analyze_competitor", "prospect-magnet": "find_prospects", "invisibility-diagnostic": "score_post",
    "voice-profile-builder": "build_voice_profile", "ai-marketing-employee": "setup_marketing_employee", "first-post-coach": "first_post_coach",
    "homework-reviewer": "review_homework",
}
TOOL_CHAIN = {
    "linkedin-post-writer": "Score with score_post, then polish_post and de_ai_ify. Turn the idea into a carousel with write_carousel or a cheatsheet with write_cheatsheet, or spread it across platforms with amplify_post.",
    "linkedin-carousel-builder": "Write the matching post with write_post. Spread it with amplify_post.",
    "linkedin-cheatsheet-builder": "Write the matching post with write_post. Run the whole week at once with weekly_content_drop.",
    "weekly-content-engine": "Score each output with score_post, then polish_post and de_ai_ify.",
    "multi-platform-amplifier": "Start from a post scored 4/4 with score_post.",
    "competitor-x-ray": "Turn the content gaps into posts with write_post, and find who to talk to with find_prospects.",
    "prospect-magnet": "Start from a published post. Clean every message with de_ai_ify.",
    "invisibility-diagnostic": "Fix gaps with polish_post and de_ai_ify; review a batch with review_homework.",
    "voice-profile-builder": "Check the result with check_my_brain. Everything else (write_post, score_post ...) reads it.",
    "ai-marketing-employee": "Needs a Voice Profile first (build_voice_profile) and the Business Brain.",
    "first-post-coach": "Score every draft with score_post. Afterwards use weekly_content_drop for a full week.",
    "homework-reviewer": "Scores come from the same engine as score_post.",
}


def read(p: Path) -> str:
    return p.read_text()


def write(p: Path, s: str) -> None:
    p.write_text(s)


def edit(rel: str, old: str, new: str, *, all: bool = False, optional: bool = False) -> None:
    p = ROOT / rel
    s = read(p)
    if old in s:
        write(p, s.replace(old, new) if all else s.replace(old, new, 1))
    elif new in s or optional:
        return
    else:
        problems.append(f"{rel}: cannot find text to edit: {old[:80]!r}")


def edit_line(rel: str, contains: str, new_line: str | None) -> None:
    """Replace (or delete, when new_line is None) every line containing `contains`."""
    p = ROOT / rel
    lines = read(p).split("\n")
    hit = [i for i, l in enumerate(lines) if contains in l]
    if not hit:
        if new_line is not None and any(new_line == l for l in lines):
            return
        if new_line is None:
            return
        problems.append(f"{rel}: no line contains {contains[:70]!r}")
        return
    out = []
    for i, l in enumerate(lines):
        if i in hit:
            if new_line is not None:
                out.append(new_line)
        else:
            out.append(l)
    write(p, "\n".join(out))


def sub_regex(rel: str, pattern: str, repl: str, flags: int = re.M) -> None:
    p = ROOT / rel
    write(p, re.sub(pattern, repl, read(p), flags=flags))


def drop_sections(text: str, pattern: str, level: int) -> str:
    """Remove markdown sections whose heading (of exactly `level` hashes) matches `pattern`. Fence-aware."""
    rx = re.compile(pattern, re.I)
    out, skipping, fence = [], False, False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            if not skipping:
                out.append(line)
            continue
        m = None if fence else re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl, title = len(m.group(1)), m.group(2).strip()
            if skipping and lvl <= level:
                skipping = False
            if not skipping and lvl == level and rx.search(title):
                skipping = True
                continue
        if not skipping:
            out.append(line)
    return "\n".join(out)


def tidy(text: str) -> str:
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r"(\n---\s*){2,}", "\n---\n", text)
    return text.rstrip() + "\n"


# ----------------------------------------------------------------------------------------------------------------------
# 1. Garbled banned-word lists -> the program's real list (Day 1 default list + AI Pattern Blacklist)
# ----------------------------------------------------------------------------------------------------------------------
def fix_banned_lists() -> None:
    P = "linkedin-post-writer/prompts/"
    edit(P + "intent-driven.md", '- ✗ "use", "open up", "help", "improve"', '- ✗ "leverage", "unlock", "empower", "elevate"')
    edit(P + "intent-driven.md", '- ✗ "today"', '- ✗ "In today\'s fast-paced world"')
    edit(P + "intent-driven.md", '- ✗ "big", "change"', '- ✗ "game-changer", "transformative"')
    edit(P + "intent-driven.md", '- ✗ "go deep", "handle"', '- ✗ "dive deep", "navigate"')
    edit(P + "intent-driven.md", '- ✗ "whole", "fit"', '- ✗ "holistic", "seamless"')
    edit(P + "framework-heavy.md", '- ✗ "big", "use", "open up"', '- ✗ "game-changer", "leverage", "unlock"')
    edit("linkedin-cheatsheet-builder/prompts/listicles.md", '("big", "use")', '("game-changer", "leverage")')
    C = "linkedin-carousel-builder/prompts/"
    edit(C + "new-carousel.md", '- ✗ "use", "open up", "help", "improve", "handle"', '- ✗ "leverage", "unlock", "empower", "elevate", "navigate"')
    edit(C + "new-carousel.md", '- ✗ "today"', '- ✗ "In today\'s fast-paced world"')
    edit(C + "intent-carousel.md", '("use", "open up", "handle")', '("leverage", "unlock", "navigate")')
    edit("prospect-magnet/prompts/personalized-dm.md", '"use, open up, path, go deep"', '"leverage, unlock, journey, dive deep"')
    edit("linkedin-post-writer/SKILL.md", 'full of "use" and "open up"', 'full of "leverage" and "unlock"')
    edit("linkedin-post-writer/SKILL.md", "(use, open up, handle, improve, etc.)", "(leverage, unlock, navigate, elevate, etc.)")
    edit("invisibility-diagnostic/SKILL.md", "(use, open up, big, help, path, go deep)", "(leverage, unlock, game-changing, empower, journey, dive deep)")
    edit("multi-platform-amplifier/SKILL.md", "(use, open up, handle, etc.)", "(leverage, unlock, navigate, etc.)")
    edit("voice-profile-builder/SKILL.md",
         "`use, open up, big, help, path, go deep, handle, improve, solid, whole, fit, brainstorm, model, ecosystem, use, unleash`",
         "`leverage, unlock, game-changing, empower, journey, dive deep, navigate, optimize, robust, holistic, synergy, ideate, paradigm, ecosystem, harness, unleash`")


# ----------------------------------------------------------------------------------------------------------------------
# 2. One length standard: LinkedIn text posts are 1300-1500 characters (about 200-250 words)
# ----------------------------------------------------------------------------------------------------------------------
STD = "1300 to 1500 characters (about 200-250 words)"


def fix_lengths() -> None:
    edit("ai-marketing-employee/SKILL.md", "150 words. End with a question.", "1300 to 1500 characters. End with a question.", all=True)
    edit("ai-marketing-employee/SKILL.md", "Default output: 150-word LinkedIn post.", "Default output: 1300-1500 character LinkedIn post (about 200-250 words).")
    edit("first-post-coach/SKILL.md", "150 words. Use my Voice Profile", STD + ". Use my Voice Profile")
    edit("first-post-coach/SKILL.md", "> 150 words. End with", "> 1300 to 1500 characters. End with")
    edit("invisibility-diagnostic/SKILL.md", "- [ ] Under 220 words (sweet spot for LinkedIn)", "- [ ] 1300-1500 characters (the program standard for LinkedIn text posts, about 200-250 words)")
    edit("multi-platform-amplifier/SKILL.md", "150-word post", "1300-1500 character post")
    for rel in ("voice-profile-builder/SKILL.md",):
        sub_regex(rel, r"\b150[- ]word\b", "1300-1500 character")
    edit("linkedin-post-writer/SKILL.md", "1300-1500 chars exactly (LinkedIn algorithm sweet spot)", "1300-1500 chars (about 200-250 words), the program standard")


# ----------------------------------------------------------------------------------------------------------------------
# 4. Anti-invention: advice and claims
# ----------------------------------------------------------------------------------------------------------------------
BANNER = ("> **Illustrative only.** The names, numbers and results in the examples below are invented to show the format. "
          "Never reuse them. In real output use only facts from the operator's Business Brain or from the request, and leave a detail out rather than make one up.")


def fix_invention() -> None:
    edit_line("first-post-coach/SKILL.md", "real-feeling",
              '> "Rewrite line 2 to include the client\'s first name from your own notes (never invent one) and how many months they had been stuck. No real client story? Say what you did yourself."')
    edit_line("first-post-coach/SKILL.md", "47 likes, 8 DMs", "- User ships at 3/4 and tracks their own results over the next 24 hours.")
    edit_line("invisibility-diagnostic/SKILL.md", "Pattern-matched against 2,000+ scored posts",
              "4. **Four fixed binary tests**. Voice, POV, Specificity and Asking each score 0 or 1, so results are repeatable, not opinion.")
    edit_line("invisibility-diagnostic/SKILL.md", "Industry-aware examples", "5. **Worked examples** across industries show what a pass and a fail look like.")
    edit("linkedin-carousel-builder/SKILL.md", "(5+ Calls Booked in 1 Week)", "(What Changed in 1 Week)")
    edit("linkedin-carousel-builder/SKILL.md", "Content: 4 billion AI posts published daily. Same models", "Content: Same models")
    edit("linkedin-post-writer/SKILL.md", "Mehsum Sayani's 1.9M impressions in 4 months.", "A client story with a measured result taken from the operator's own notes.")
    edit("linkedin-carousel-builder/SKILL.md", "GBI Online cohort opens June 12.", "The operator's next programme opens (date taken from the Business Brain).")
    # footers and marketing claims
    for f in ROOT.glob("*/SKILL.md"):
        s = read(f)
        s = re.sub(r"^\*(?:Built|Calibrated|Production).*\*\s*$", "", s, flags=re.M)
        s = re.sub(r"\b(?:\d+|Two|Three|Four|Five) production-tested ", lambda m: m.group(0).replace("production-tested ", ""), s)
        s = s.replace("production-tested ", "")
        s = re.sub(r"\n- \*\*(?:Calibrated|Production)[^\n]*", "", s)
        write(f, s)
    # examples banner
    for f in ROOT.glob("*/SKILL.md"):
        s = read(f)
        if "Illustrative only" not in s:
            s = re.sub(r"^(##\s+Examples?[^\n]*\n)", r"\1\n" + BANNER.replace("\\", "\\\\") + "\n", s, count=1, flags=re.M)
            write(f, s)


# ----------------------------------------------------------------------------------------------------------------------
# 5. Sample copy that breaks the style rules
# ----------------------------------------------------------------------------------------------------------------------
NEW_POST_SAMPLE = '''I told a client last week to stop posting.

She had posted every day for six months. Mindset content, the kind everyone else writes. Eleven likes in total and no leads.

Her schedule was fine. Nothing she wrote sounded like her. She had performed "expert" for so long she forgot what she believed.

We rebuilt her voice profile in five minutes and put it in one Claude Project.

By Tuesday she published a post in her own voice. The first inbound DM in four months arrived that afternoon.

If your posts are not landing, read the last five out loud and count how many a stranger could have written.

Fix that once and keep it.

DM me "voice" and I will send you the worksheet I gave her.

---
(Illustrative sample, shortened. Real output is 1300-1500 characters, uses only facts from the Business Brain, and is scored with score_post.)'''


def fix_style() -> None:
    p = ROOT / "linkedin-post-writer/SKILL.md"
    s = read(p)
    m = re.search(r"\*\*Output \(sample\):\*\*\n```\n(.*?)\n```", s, re.S)
    if m and "Illustrative sample, shortened" not in m.group(1):
        s = s[: m.start(1)] + NEW_POST_SAMPLE + s[m.end(1):]
        write(p, s)
    elif not m and "Illustrative sample, shortened" not in s:
        problems.append("linkedin-post-writer/SKILL.md: sample post block not found")
    # filler / hype conversational markers
    for rel in ("linkedin-post-writer/prompts/story-flow.md", "linkedin-post-writer/prompts/framework-heavy.md"):
        s = read(ROOT / rel)
        s = s.replace('"Real talk:" ', "").replace('"Real talk:" / ', "").replace('/ "Real talk:"', "").replace('"Real talk:", ', "")
        s = s.replace('[Optional: "Real talk:" + reframe - 1 sentence]', "[Optional: one-sentence reframe in the operator's own words]")
        s = s.replace('optional "Real ', 'optional "')
        write(ROOT / rel, s)
    sub_regex("linkedin-post-writer/prompts/story-flow.md", r"Real talk:?\"?\s*/?\s*", "")
    sub_regex("linkedin-post-writer/prompts/framework-heavy.md", r"\"Real talk:\",\s*", "")
    # carousel slides: short
    for rel in ("linkedin-carousel-builder/prompts/new-carousel.md", "linkedin-carousel-builder/prompts/intent-carousel.md", "linkedin-carousel-builder/SKILL.md"):
        sub_regex(rel, r"\[2-3 sentences maximum, 10-15 words each\]", "[1-2 short sentences, 20 words maximum in total]")
        sub_regex(rel, r"6-8 words maximum", "6 words maximum")
    edit("multi-platform-amplifier/SKILL.md", "The problem wasn't her schedule. it was that nothing she wrote sounded like her.", "Her schedule was fine. Nothing she wrote sounded like her.", optional=True)


# ----------------------------------------------------------------------------------------------------------------------
# 6 + 7. Structure: drop sections that point at things that do not exist here, and cohort-specific sections
# ----------------------------------------------------------------------------------------------------------------------
DROP_L2 = [r"^Usage$", r"^Bundled (Files|Scripts)$", r"^GitHub( \+ source)? [Rr]eferences.*$", r"^Stage script.*$", r"^Apify Setup.*$",
           r"^Output [Ss]tructure \(`?visual`? mode\)$", r"^Why This vs `voice-extractor`\?$", r"^Why this exists$", r"^Chains [Ww]ith [Oo]ther [Ss]kills$"]


def restructure() -> None:
    for f in sorted(ROOT.glob("*/SKILL.md")):
        name = f.parent.name
        if name == "newsletter-writer":
            continue
        s = read(f)
        for pat in DROP_L2:
            s = drop_sections(s, pat, 2)
        s = drop_sections(s, r"visual", 3)  # "### Example 3. Visual mode ..."
        s = re.sub(r"^\|\s*`?visual`?\s*(?:★)?\s*\|[^\n]*\n", "", s, flags=re.M)  # mode-table rows
        s = re.sub(r"\n\*\*Use `visual` when:[^\n]*\n", "\n", s)
        s = tidy(s)
        if "## Use in the Purely Personal connector" not in s:
            s += (f"\n---\n\n## Use in the Purely Personal connector\n\nTool: `{CONNECTOR_TOOL[name]}`. It returns a work order built from this skill, locked to the operator's own "
                  f"Business Brain, ICP and Voice DNA. `visual` (HTML) modes are not available in the connector; ask for the Canva AI prompt instead.\n\n"
                  f"After the draft: {TOOL_CHAIN[name]}\n")
        write(f, s)


def fix_references() -> None:
    allsk = [f for f in ROOT.glob("*/SKILL.md") if f.parent.name != "newsletter-writer"] + [f for f in ROOT.glob("*/prompts/*.md")]
    for f in allsk:
        s = read(f)
        s = s.replace("STOP. run ICP Builder first", "STOP. ask the operator for their ICP (ICP.md or the Business Brain)")
        s = s.replace("STOP. run ICP Builder.", "STOP. ask the operator for their ICP (ICP.md or the Business Brain).")
        s = s.replace("(output of `voice-profile-builder` + ICP Builder)", "(the operator's ICP.md or the Business Brain)")
        s = s.replace("(output of ICP Builder · 13 questions across 3 sections)", "(the operator's ICP.md or the customer section of the Business Brain)")
        s = re.sub(r"\| ICP Builder(?: \(HTML fillable\))? \|", "| ICP.md |", s)
        s = s.replace("Re-run ICP Builder every 90 days", "Refresh your ICP every 90 days")
        s = s.replace("supreme_coder--linkedin-profile-scraper", "harvestapi/linkedin-profile-scraper")
        s = s.replace("supreme_coder/linkedin-profile-scraper", "harvestapi/linkedin-profile-scraper")
        s = s.replace("harvestapi--linkedin-profile-search", "harvestapi/linkedin-profile-search")
        s = s.replace("`de-ai-ify`", "the `de_ai_ify` tool")
        s = re.sub(r"\n[^\n]*(?:`content-multiplier`|`cold-outreach-sequence`)[^\n]*", "", s)
        s = re.sub(r"\n\|[^\n]*`workbook`[^\n]*", "", s)
        s = re.sub(r"\n[^\n]*(?:Apify token|APIFY_TOKEN)[^\n]*", "\n| Apify | The operator's own Apify connector (their account and credit) | STOP. ask them to connect Apify first |", s, count=1) \
            if "APIFY_TOKEN" in s or "Apify token" in s else s
        s = re.sub(r"\n[^\n]*(?:APIFY_TOKEN|Apify token|~/\.claude|scripts/find-prospects|render\.py)[^\n]*", "", s)
        write(f, tidy(s) if f.name == "SKILL.md" else s)
    edit_line("ai-marketing-employee/SKILL.md", "formatted for the workbook flow", "3. **3-step install guide**. Create the Project, add the Business Brain to Project knowledge, paste the Instructions.")
    edit_line("ai-marketing-employee/SKILL.md", "workbook export (JSON", None)
    edit("ai-marketing-employee/SKILL.md", "(parse from chat / clipboard / workbook export)", "(from the chat or the Business Brain)", optional=True)
    edit("ai-marketing-employee/SKILL.md", "Voice Profile + workbook intake data", "Voice Profile + business context", optional=True)
    edit("linkedin-post-writer/SKILL.md", "or use `content-multiplier`", "or run it several times", optional=True)
    edit("linkedin-post-writer/SKILL.md", "bundled as full Notion-extracted prompts, not just frameworks", "bundled as full prompts, not just frameworks", optional=True)


def fix_cohort() -> None:
    p = ROOT / "first-post-coach/SKILL.md"
    s = read(p)
    s = re.sub(r"^description:.*$", "description: Coach a user from blank page to a published 4/4 post in 10 minutes. Provides the brief template, real-time invisibility-diagnostic scoring, one-line edit suggestions, and a ship-it gate. Use when someone is writing their first AI-assisted post, or any first-attempt content session where the goal is to finish, not perfect. Triggers on \"help me write my first post\", \"first post help\", \"I'm stuck on a post\", \"I have 10 minutes to write a post\".", s, count=1, flags=re.M)
    s = re.sub(r"^tags:.*$", "tags: [coaching, content, voice, first-post]", s, count=1, flags=re.M)
    s = s.replace("The 10-minute coaching skill for Game 1 of the AI Employee Challenge.", "The 10-minute coaching skill for a first AI-assisted post.")
    s = s.replace("Live coach (Game 1 style)", "Live coach (timed)")
    s = s.replace("Game 1 of the Challenge, deadline-driven", "A first post under a time box")
    s = re.sub(r"Stop\. Game 1 is ONE post\. Five posts is a Day 2 lesson \(`content-multiplier`\)\. Hard pivot\.", "Stop. This session is ONE post. Use weekly_content_drop for a week of content afterwards. Hard pivot.", s)
    s = re.sub(r"\n\[If in Challenge cohort:\][^\n]*\n[^\n]*\n", "\n", s)
    s = re.sub(r"\n\| `homework-reviewer` \|[^\n]*", "", s)
    s = s.replace("Next: Day 2 (we multiply that one post into 5). Or run", "Next: run weekly_content_drop for a full week. Or run")
    s = re.sub(r"1\. \*\*Run during Game 1 of the Challenge\.\*\*[^\n]*", "1. **Use it for a first post.** The 10-minute cap exists to stop perfectionism eating shipping.", s)
    s = re.sub(r"2\. \*\*Use `audit` mode for peer review\.\*\*[^\n]*", "2. **Use `audit` mode for a colleague's draft.** Both of you can run it on the same post and compare scores.", s)
    s = re.sub(r"\bGame 1\b", "the first post", s)
    write(p, tidy(s))

    p = ROOT / "weekly-content-engine/SKILL.md"
    s = read(p)
    s = re.sub(r"^description:.*$", "description: One short idea in, three publish-ready outputs out: a long-form LinkedIn post, a 5-7 slide carousel, and a save-worthy cheatsheet, each with a Canva AI handoff prompt. Voice-locked to the operator's Voice DNA and ICP-locked to their ICP. Triggers on \"build my week of content\", \"give me my weekly drop\", \"weekly content engine\", \"I need posts for this week\".", s, count=1, flags=re.M)
    s = re.sub(r"^tags:.*$", "tags: [linkedin, content-system, weekly, canva]", s, count=1, flags=re.M)
    s = re.sub(r"\n[^\n]*(?:stage demo|Stage script|on stage|the stage)[^\n]*", "", s)
    s = re.sub(r"\n[^\n]*(?:React|\.jsx|widget|form artifact)[^\n]*", "", s)
    write(p, tidy(s))

    for f in ROOT.glob("*/SKILL.md"):
        if f.parent.name in ("newsletter-writer", "homework-reviewer"):
            continue
        s = read(f)
        s = s.replace("for the AI Employee Challenge", "for a Claude Project")
        s = re.sub(r"\n[^\n]*(?:CET|CEST|on stage|Day 2 lesson|Day 2 chat|Tomorrow on Day 2)[^\n]*", "", s)
        s = s.replace(" (Day 2 lesson)", "").replace(" (Day 2)", "").replace("Built for the AI Employee Challenge", "")
        write(f, tidy(s))


HOMEWORK = '''---
name: homework-reviewer
description: Bulk-score a batch of posts (a group's homework, a team's drafts, a content backlog), rank them with the Invisibility Diagnostic, and produce a shortlist with industry coverage, a shout-out list and a private coaching list. Use when asked to review the homework, rank the posts, find the best 10, or grade a batch. Triggers on "review the homework", "rank the posts", "find the best posts", "grade this batch", "compile the shortlist".
version: 1.1.0
author: daniel-paul
tags: [review, scoring, batch, invisibility-diagnostic]
---

# Homework Reviewer

Scores every post in a batch with the Invisibility Diagnostic (Voice, POV, Specificity, Asking), ranks them, and builds a shortlist a facilitator can use straight away. Works for any batch: a group's homework, a team's drafts, a backlog of old posts.

## Why not just paste 50 posts into a chat?
Pasted batches get inconsistent picks, no check that the shortlist covers different industries, and no list of who needs help. This skill scores every post the same way, ranks by score, and checks coverage.

## Inputs

| Input | Format |
|---|---|
| Posts | A JSON list of `{"name", "industry", "post"}`, **or** plain text with posts separated by a line containing only `---` (optionally `Name:` and `Industry:` lines at the top of each) |
| Batch context | Optional: how many to shortlist, the industries in the room |

## Modes

| Mode | What you get |
|---|---|
| `quick` | Top N only, with scores |
| `standard` (default) | Top N with the opening line of each, an industry coverage check, a next-15 shout-out list |
| `full` | Standard plus a coach list of posts scoring 0-1 with the one-line fix for each, and the full ranked list |

## Process

1. Parse and validate the posts. Report how many were read and skip empties.
2. Score each post 0-4 with the Invisibility Diagnostic (the `score_post` engine). Record the score, tier, character count and the fix lines.
3. Rank by score, then Specificity, then length.
4. Pick the top N, limiting any one industry to two places while the batch is large enough to allow it, so the shortlist is not all one niche.
5. Build the shout-out list (the next 15) and the coach list (posts scoring 0 or 1, each with its first fix line).
6. Order the top N for the read-aloud: open strong, build, finish on the post that teaches the most.

## Output

```
HOMEWORK REVIEW · <n> posts · 4/4: a · 3/4: b · 2/4: c · 0-1/4: d

SHORTLIST (top N, in reading order)
  1. <name> · <industry> · <score>/4 · "<opening line>"

INDUSTRY COVERAGE
CHAT SHOUT-OUTS (next 15)
COACH LIST (0-1/4, private check-in, with the one-line fix)
```

## Rules
- Scores are heuristic. A script cannot hear that a sentence is not the writer's. Read the top 10 yourself before using the shortlist.
- Never alter a participant's post, and never add a name, number or result that was not in it.
- Share names only with the facilitator unless the participants agreed to be read out.

## Limitations
- Scores posts as text; it does not see images or carousels.
- Industry coverage depends on the `industry` field you supply.
'''


def fix_residuals() -> None:
    """Second pass: intro paragraphs, mode tables, schedule hints and the last invented claims."""
    for f in list(ROOT.glob("*/SKILL.md")) + list(ROOT.glob("*/prompts/*.md")):
        if f.parent.name == "newsletter-writer" or f.name == "SKILL.md" and f.parent.name == "homework-reviewer":
            continue
        s = read(f)
        # prompt-file paths: they live in prompts/ inside the bundle
        s = s.replace("scripts/prompts/", "prompts/")
        # renderer / template references
        s = re.sub(r"\n[^\n]*template\.html[^\n]*", "", s)
        s = re.sub(r"\n[^\n]*`visual` *(?:→|->)[^\n]*", "", s)
        s = re.sub(r"\n[^\n]*\bvisual\b[^\n]*(?:HTML|artifact|render)[^\n]*", "", s, flags=re.I)
        s = s.replace("run ICP Builder", "ask for the operator's ICP (ICP.md or the Business Brain)")
        s = s.replace("User input or from workbook", "User input or the Business Brain")
        # lesson / schedule wording
        s = re.sub(r"First-time setup during Lesson \d live build", "First-time setup, built live", s)
        s = re.sub(r"First pass during Lesson \d live build", "First pass, built live", s)
        s = re.sub(r"use `quick` only during live Lesson \d when", "use `quick` only in a live session when", s)
        s = re.sub(r"\((?:live during Lesson \d|live build during Lesson \d)\)", "(built live)", s)
        s = re.sub(r"Day \d \((\w+)\):", r"\1:", s)
        s = re.sub(r"\n[^\n]*(?:Demo \d|holy shit|Day [12] AI Employee Challenge|For Day [12] of)[^\n]*", "", s)
        s = s.replace("most attendees run it after", "most people run it after").replace("(what attendees take home)", "(what you get)")
        s = re.sub(r"\n3\. \*\*Track your average over time\*\*[^\n]*", "\n3. **Track your average over time**. A rising average across your last 20 posts shows the voice work is landing.", s)
        s = s.replace("Follow Daniel Paul for AI workflows that sound like YOU. New post every Tuesday.", "Follow the operator for practical workflows on the topic. New post on a fixed day each week.")
        s = s.replace('(e.g. "— Daniel")', '(e.g. "— <first name>")')
        s = s.replace("(5+ Calls Booked in 1 Week)", "(What Changed in 1 Week)")
        s = s.replace("next cohort opens", "next programme opens")
        s = s.replace(" exactly like the 4 billion other AI-generated carousels published daily.", " exactly like every other AI-generated carousel.")
        s = re.sub(r"calibrated against high-performing Purely Personal cohort carousels \(", "(", s)
        s = s.replace("- 2-3 sentence content (10-15 words each)", "- 1-2 short sentences of content (20 words maximum in total)")
        s = s.replace("Every body slide 2-3 sentences max?", "Every body slide 1-2 short sentences, 20 words max?")
        s = s.replace("Does every body slide have 2-3 sentences max?", "Does every body slide have 1-2 short sentences (20 words max)?")
        s = s.replace("Content: [2-3 sentences, 10-15 words each]", "Content: [1-2 short sentences, 20 words maximum in total]")
        s = s.replace("- [ ] Each slide content 2-3 sentences", "- [ ] Each slide content 1-2 short sentences, 20 words max")
        s = s.replace("This is the skill that makes attendees say \"I am keeping this forever\" on Day 1.\n", "")
        write(f, s)
    for f in ROOT.glob("*/SKILL.md"):
        s = read(f)
        s = s.replace("(supreme_coder)", "(harvestapi)").replace("supreme_coder", "harvestapi")
        s = s.replace("and the ICP Builder", "and your ICP.md").replace("ICP Builder", "ICP.md")
        write(f, s)
    # competitor-x-ray: the profile scraper does not return posts. Posts come from the post scrapers; company pages need the company ones.
    edit_line("competitor-x-ray/SKILL.md", "to pull actual profile data + last 30 days of posts",
              "1. **Real scraped data**. uses Apify (`harvestapi/linkedin-profile-posts` for people, `harvestapi/linkedin-company-posts` for company pages, plus `harvestapi/linkedin-profile-scraper` / `harvestapi/linkedin-company` for profile and page details) to pull actual data + recent posts for each competitor")
    edit_line("competitor-x-ray/SKILL.md", "call `harvestapi/linkedin-profile-scraper` to pull profile + posts",
              "For each URL: a `linkedin.com/company/...` URL is a COMPANY PAGE (use `harvestapi/linkedin-company` for the page and `harvestapi/linkedin-company-posts` for its posts); a `linkedin.com/in/...` URL is a PERSON (use `harvestapi/linkedin-profile-scraper` for the profile and `harvestapi/linkedin-profile-posts` for the posts). Last 30 days for `standard`, 90 days for `deep`.")
    # frontmatter: descriptions and tags are served by list_skills, so they must be clean too
    for f in ROOT.glob("*/SKILL.md"):
        if f.parent.name == "newsletter-writer":
            continue
        s = read(f)
        s = re.sub(r" Built from analyzing 2,000\+[^\n]*?cohorts\.", "", s)
        s = s.replace("taught in the AI Employee Challenge ", "")
        s = s.replace('"extract my voice for the challenge", ', "")
        s = s.replace(", ai-employee-challenge,", ",")
        s = s.replace("[ai-employee-challenge, ", "[").replace(", ai-employee-challenge]", "]").replace(", ai-employee-challenge,", ",")
        s = s.replace("(a cohort's homework,", "(a group's homework,")
        write(f, s)
    # intro paragraphs that describe a live course
    edit_line("ai-marketing-employee/SKILL.md", "taught in Day 1 / Lesson 2",
              "The setup-helper for the AI Marketing Employee Project. Takes a Voice Profile + business context, generates personalized Project Instructions, and produces a 3-step manual install guide.")
    edit_line("invisibility-diagnostic/SKILL.md", "taught in Day 1 / Lesson 1", "Run it on every post before you publish. The point is the pre-publish edit.")
    edit_line("voice-profile-builder/SKILL.md", "taught in Day 1 / Lesson 2",
              "The 4-input voice extraction method. Built to feed straight into a Claude Project as Knowledge, no reformatting required.")
    edit_line("prospect-magnet/SKILL.md", "holy shit", None)
    edit_line("weekly-content-engine/SKILL.md", "keeping this forever", None)


def rewrite_homework() -> None:
    p = ROOT / "homework-reviewer/SKILL.md"
    if "version: 1.1.0" not in read(p):
        write(p, HOMEWORK + "\n---\n\n## Use in the Purely Personal connector\n\nTool: `review_homework`. It returns the ranked shortlist, coverage, shout-out list and coach list. Scores come from the same engine as score_post.\n")


def main() -> int:
    if not ROOT.exists():
        print("skills folder not found:", ROOT)
        return 2
    fix_banned_lists()
    fix_lengths()
    fix_invention()
    fix_style()
    restructure()
    fix_references()
    fix_cohort()
    fix_residuals()
    rewrite_homework()
    for f in ROOT.glob("*/SKILL.md"):  # final whitespace tidy
        write(f, tidy(read(f)))
    if problems:
        print("PROBLEMS (an upstream skill changed; update the cleaner):")
        for x in problems:
            print("  -", x)
        return 1
    print("skills cleaned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
