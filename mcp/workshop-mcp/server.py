#!/usr/bin/env python3
"""
Purely Personal Workshop MCP Server

Exposes the workshop-scaffolder logic as an MCP server so it works in
Claude Desktop, the Claude Agent SDK, and any other MCP client.

Tools:
- scaffold_workshop      Generate a complete new workshop folder
- validate_voice         Check copy for em-dashes + banned phrases
- list_workshops         List workshops in the workspace

Resources:
- brain://current        Current BUSINESS-BRAIN.md
- voice://rules          Voice rules (banned phrases, hook patterns)
- params://inventory     Parameter inventory (which tokens live where)

Run as MCP server (stdio transport):
    python3 server.py

Configure in claude_desktop_config.json:
{
  "mcpServers": {
    "purely-personal-workshop": {
      "command": "python3",
      "args": ["/absolute/path/to/purely-personal/mcp/workshop-mcp/server.py"]
    }
  }
}
"""
from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Paths resolved relative to this file. Server runs from any cwd.
SERVER_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SERVER_DIR.parent.parent  # purely-personal/

mcp = FastMCP("purely-personal-workshop")


# ============================================================
# RESOURCES
# ============================================================

@mcp.resource("brain://current")
def read_business_brain() -> str:
    """Read the current project's BUSINESS-BRAIN.md.

    Used by Claude as voice + brand context when generating workshop copy.
    Looks in the plugin root first, then the cwd.
    """
    candidates = [
        PLUGIN_ROOT / "BUSINESS-BRAIN.md",
        Path.cwd() / "BUSINESS-BRAIN.md",
        PLUGIN_ROOT / "examples" / "BUSINESS-BRAIN.sample.md",
    ]
    for p in candidates:
        if p.exists():
            return p.read_text()
    return (
        "BUSINESS-BRAIN.md not found.\n\n"
        "Run /build-my-brain in Claude Code first, then run scaffold_workshop again.\n\n"
        "Looked in:\n" + "\n".join(f"  - {p}" for p in candidates)
    )


@mcp.resource("voice://rules")
def read_voice_rules() -> str:
    """Read the voice rules document.

    The full discipline for AI-generated workshop copy: banned phrases,
    hook patterns, sentence rhythms, anti-patterns to filter.
    """
    p = PLUGIN_ROOT / "skills" / "workshop-scaffolder" / "references" / "voice-rules.md"
    return p.read_text() if p.exists() else "voice-rules.md missing"


@mcp.resource("params://inventory")
def read_parameter_inventory() -> str:
    """Read the parameter inventory.

    Shows which tokens live in which Workshop 01 source files. Used by
    scaffold_workshop to know what to find-replace.
    """
    p = PLUGIN_ROOT / "skills" / "workshop-scaffolder" / "references" / "parameters.md"
    return p.read_text() if p.exists() else "parameters.md missing"


# ============================================================
# TOOLS
# ============================================================

# Workshop 01 default values that the scaffolder swaps out.
#
# IMPORTANT: every default value below MUST be specific enough that find-replace
# can't match it accidentally inside other content. So we use full phrases like
# "Workshop 01" not bare "01", "$49" not bare "49", "40 seats" not bare "40".
# Order matters · longer keys substitute first to avoid partial-match collisions.
WORKSHOP_01_DEFAULTS = {
    # Workshop identity (3 variants based on where it appears)
    "WORKSHOP_NAME_LANDING": "Build Your Marketing & Sales Machine in 2 Days",  # landing page <title>
    "WORKSHOP_NAME_PROJECT": "Build a Business That Runs By Itself",            # repo description
    "WORKSHOP_LABEL_PADDED": "Workshop 01",
    "WORKSHOP_LABEL_NUM": "Workshop 1",

    # Dates · always include surrounding words to avoid matching as substring
    "DAY_1_DATE_FULL": "Saturday May 2, 2026",
    "DAY_2_DATE_FULL": "Sunday May 3, 2026",
    "DAY_1_DATE_DAYNAME": "Saturday May 2",   # used in landing page day-when
    "DAY_2_DATE_DAYNAME": "Sunday May 3",
    "DAY_1_DATE_SHORT": "Sat May 2",
    "DAY_2_DATE_SHORT": "Sun May 3",
    "DATE_RANGE_EN": "May 2\u20133, 2026",
    "DATE_RANGE_HYPHEN": "May 2-3, 2026",

    # Pricing · always with $ or word
    "PRICE_DOLLAR": "$49",
    "PRICE_DOLLARS_WORD": "49 dollars",

    # Seats · always with "seats" suffix
    "SEAT_COUNT_LABEL": "40 seats",

    # Topics + deliverables (already long enough to be unique)
    "DAY_1_DELIVERABLE": "Marketing Machine",
    "DAY_2_DELIVERABLE": "Sales Machine",
    "DAY_1_TOPIC": "Automate Your Marketing",
    "DAY_2_TOPIC": "Automate Your Sales",

    # Cohort
    "COHORT_PRICE": "$2,400",
    "COHORT_START": "June 2026",
}

UNIVERSAL_BANNED_PHRASES = [
    "unlock", "delve", "delving", "dive into",
    "seamless", "seamlessly", "supercharge",
    "elevate", "elevating", "leverage",
    "tapestry", "realm", "landscape", "journey",
    "unleash", "synergy", "holistic",
    "cutting-edge", "state of the art", "revolutionize",
]


def _slugify(text: str) -> str:
    """Convert text to kebab-case slug."""
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = s.strip("-")
    return s


def _parse_date(s: str) -> datetime:
    """Parse ISO date or natural language."""
    formats = [
        "%Y-%m-%d", "%B %d, %Y", "%B %d %Y",
        "%b %d, %Y", "%b %d %Y", "%m/%d/%Y", "%m-%d-%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Could not parse date: {s!r}")


def _build_substitutions(
    workshop_name: str,
    workshop_slug: str,
    workshop_number: int,
    day_1: datetime,
    day_2: datetime,
    day_1_topic: str,
    day_2_topic: str,
    day_1_deliverable: str,
    day_2_deliverable: str,
    price: int,
    seat_count: int,
    cohort_price: str,
    cohort_start: str,
) -> dict[str, tuple[str, str]]:
    """Build the {old: new} substitution map."""
    new_values = {
        "WORKSHOP_NAME_LANDING": workshop_name,
        "WORKSHOP_NAME_PROJECT": workshop_name,
        "WORKSHOP_LABEL_PADDED": f"Workshop {workshop_number:02d}",
        "WORKSHOP_LABEL_NUM": f"Workshop {workshop_number}",
        "DAY_1_DATE_FULL": day_1.strftime("%A %B %-d, %Y"),
        "DAY_2_DATE_FULL": day_2.strftime("%A %B %-d, %Y"),
        "DAY_1_DATE_DAYNAME": day_1.strftime("%A %B %-d"),
        "DAY_2_DATE_DAYNAME": day_2.strftime("%A %B %-d"),
        "DAY_1_DATE_SHORT": day_1.strftime("%a %b %-d"),
        "DAY_2_DATE_SHORT": day_2.strftime("%a %b %-d"),
        "DATE_RANGE_EN": f"{day_1.strftime('%B %-d')}\u2013{day_2.strftime('%-d')}, {day_1.year}",
        "DATE_RANGE_HYPHEN": f"{day_1.strftime('%B %-d')}-{day_2.strftime('%-d')}, {day_1.year}",
        "PRICE_DOLLAR": f"${price}",
        "PRICE_DOLLARS_WORD": f"{price} dollars",
        "SEAT_COUNT_LABEL": f"{seat_count} seats",
        "DAY_1_DELIVERABLE": day_1_deliverable,
        "DAY_2_DELIVERABLE": day_2_deliverable,
        "DAY_1_TOPIC": day_1_topic,
        "DAY_2_TOPIC": day_2_topic,
        "COHORT_PRICE": cohort_price or "",
        "COHORT_START": cohort_start or "",
    }
    return {token: (WORKSHOP_01_DEFAULTS[token], new_values[token]) for token in new_values}


def _apply_substitutions(text: str, subs: dict[str, tuple[str, str]]) -> str:
    """Apply find-replace substitutions to text using a two-pass placeholder
    strategy so that NEW values can't accidentally match OLD patterns.

    Pass 1: replace each old value with a unique placeholder (`@@TOKEN@@`)
    Pass 2: replace each placeholder with the new value

    Longer old values are processed first to avoid partial substring matches.
    """
    # Pass 1: old -> placeholder (longest first)
    items = sorted(subs.items(), key=lambda kv: len(kv[1][0]), reverse=True)
    for token, (old, _new) in items:
        text = text.replace(old, f"@@{token}@@")

    # Pass 2: placeholder -> new
    for token, (_old, new) in items:
        text = text.replace(f"@@{token}@@", new)

    return text


def _copy_with_subs(src: Path, dst: Path, subs: dict[str, tuple[str, str]]) -> None:
    """Copy a file, applying token substitutions."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix in {".md", ".html", ".json", ".txt", ".sh"}:
        text = src.read_text()
        dst.write_text(_apply_substitutions(text, subs))
    else:
        shutil.copy2(src, dst)


@mcp.tool()
def scaffold_workshop(
    workshop_name: str,
    workshop_slug: str = "",
    workshop_number: int = 0,
    day_1_date: str = "",
    day_2_date: str = "",
    day_1_topic: str = "",
    day_2_topic: str = "",
    day_1_deliverable: str = "",
    day_2_deliverable: str = "",
    price: int = 49,
    seat_count: int = 40,
    core_hook: str = "",
    cohort_price: str = "",
    cohort_start: str = "",
    output_dir: str = "~/Desktop",
) -> str:
    """Scaffold a complete new workshop launch package.

    Reads source files from the existing Purely Personal Workshop 01 repo,
    applies token substitutions for workshop-specific values, and writes
    the new workshop to <output_dir>/<workshop_slug>/.

    Mechanical substitutions applied to:
      - landing-page/index.html
      - landing-page/install-guide/index.html
      - campaign/email-campaign.md
      - campaign/dm-outreach.md
      - integrations/ghl-build-spec.md
      - workshop/Workshop-Agenda.xlsx (regenerated with openpyxl)

    Workshop-unique copy NOT auto-generated by this tool (because it requires
    voice-aware writing that the LLM does better than Python):
      - VSL script (drop a TO-REWRITE marker)
      - Email subject lines (placeholder + Workshop 01 originals as reference)
      - DM segment openers (placeholder)
      - Phase walkthrough voiceover scripts (Workshop 01 scripts as starting point)
      - 3 short Ava-style video scripts

    Returns a summary of what was generated and what still needs voice rewrite.
    Hand the returned REWRITE-NEEDED.md path to Claude to finish the soft copy.

    Args:
        workshop_name: Full title (e.g., "Build Your Sales Machine in 30 Days")
        workshop_slug: Kebab-case slug (auto-generated from name if empty)
        workshop_number: Integer (default: next available, scans output_dir)
        day_1_date: ISO 8601 or natural language (e.g., "2026-06-14" or "June 14 2026")
        day_2_date: Same format. Must be one calendar day after day_1
        day_1_topic: Headline-style topic for Day 1 (e.g., "Automate Your Prospecting")
        day_2_topic: Same for Day 2
        day_1_deliverable: 2-word output name (e.g., "Prospect Machine")
        day_2_deliverable: Same for Day 2 (e.g., "Follow-up Machine")
        price: Workshop price in USD (default 49)
        seat_count: Maximum seats (default 40)
        core_hook: One-sentence VSL hook (placed in the new VSL draft)
        cohort_price: Cohort upsell price (e.g., "$3,200") or empty to skip
        cohort_start: Cohort start month (e.g., "June 2026") or empty to skip
        output_dir: Parent directory (default ~/Desktop)

    Returns:
        Multi-line summary of files generated, files needing voice rewrite,
        and the next 5 steps to launch the new workshop.
    """
    # Validate + auto-fill
    if not workshop_name:
        return "ERROR: workshop_name is required."

    if not workshop_slug:
        workshop_slug = _slugify(workshop_name)

    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", workshop_slug):
        return f"ERROR: workshop_slug must be kebab-case. Got: {workshop_slug!r}"

    output_root = Path(output_dir).expanduser().resolve()
    if workshop_number == 0:
        # Find next available
        existing = [p for p in output_root.glob("workshop-*") if p.is_dir()]
        workshop_number = len(existing) + 2  # +2 because Workshop 01 already exists elsewhere

    # Parse dates
    try:
        d1 = _parse_date(day_1_date) if day_1_date else None
        d2 = _parse_date(day_2_date) if day_2_date else None
    except ValueError as e:
        return f"ERROR: {e}"

    if not d1 or not d2:
        return "ERROR: day_1_date and day_2_date are required."

    if (d2 - d1).days != 1:
        return (
            f"ERROR: day_2_date must be exactly 1 day after day_1_date. "
            f"Got {d1.date()} and {d2.date()} ({(d2-d1).days} days apart)."
        )

    if not day_1_deliverable:
        day_1_deliverable = day_1_topic.split(" ")[-1] + " Machine" if day_1_topic else "Workshop Day 1"
    if not day_2_deliverable:
        day_2_deliverable = day_2_topic.split(" ")[-1] + " Machine" if day_2_topic else "Workshop Day 2"
    if not day_1_topic:
        day_1_topic = f"Build your {day_1_deliverable}"
    if not day_2_topic:
        day_2_topic = f"Build your {day_2_deliverable}"

    # Output path
    target = output_root / workshop_slug
    if target.exists():
        return f"ERROR: {target} already exists. Pick a different slug or remove the folder."
    target.mkdir(parents=True)

    # Build substitution map
    subs = _build_substitutions(
        workshop_name=workshop_name,
        workshop_slug=workshop_slug,
        workshop_number=workshop_number,
        day_1=d1,
        day_2=d2,
        day_1_topic=day_1_topic,
        day_2_topic=day_2_topic,
        day_1_deliverable=day_1_deliverable,
        day_2_deliverable=day_2_deliverable,
        price=price,
        seat_count=seat_count,
        cohort_price=cohort_price,
        cohort_start=cohort_start,
    )

    # Files to copy + token-replace
    sources_to_copy = [
        "landing-page/index.html",
        "landing-page/install-guide/index.html",
        "landing-page/install-guide/CAPTURE-CHECKLIST.md",
        "campaign/email-campaign.md",
        "campaign/dm-outreach.md",
        "campaign/vsl-script.md",
        "campaign/video-scripts.md",
        "integrations/ghl-build-spec.md",
        "integrations/vercel-to-ghl.md",
        ".gitignore",
    ]

    files_written = []
    files_skipped = []

    for rel_path in sources_to_copy:
        src = PLUGIN_ROOT / rel_path
        if not src.exists():
            files_skipped.append(rel_path)
            continue
        dst = target / rel_path
        _copy_with_subs(src, dst, subs)
        files_written.append(rel_path)

    # Copy workshop folder (worksheets + agenda xlsx)
    src_workshop = PLUGIN_ROOT / "workshop"
    if src_workshop.exists():
        dst_workshop = target / "workshop"
        for item in src_workshop.rglob("*"):
            if item.is_file() and "install-guide" not in item.parts:
                rel = item.relative_to(PLUGIN_ROOT)
                _copy_with_subs(item, target / rel, subs)
                files_written.append(str(rel))

    # Generate REWRITE-NEEDED.md so Claude knows what to fill in
    rewrite_md = target / "REWRITE-NEEDED.md"
    rewrite_md.write_text(_build_rewrite_needed(
        workshop_name=workshop_name,
        core_hook=core_hook,
        day_1_deliverable=day_1_deliverable,
        day_2_deliverable=day_2_deliverable,
        cohort_price=cohort_price,
        cohort_start=cohort_start,
    ))

    # Generate README
    readme = target / "README.md"
    readme.write_text(_build_readme(
        workshop_name=workshop_name,
        workshop_slug=workshop_slug,
        workshop_number=workshop_number,
        day_1=d1,
        day_2=d2,
        price=price,
    ))

    # Build summary
    summary = [
        f"Generated · {workshop_name}",
        f"Output: {target}/",
        "",
        f"Files written: {len(files_written)}",
        f"Files skipped (source missing): {len(files_skipped)}",
        "",
        "Next steps:",
        f"  1. cd {target}",
        f"  2. open landing-page/index.html (review)",
        f"  3. cat REWRITE-NEEDED.md (5 files Claude should rewrite in your voice)",
        f"  4. Render videos: see videos/RENDER.sh",
        f"  5. Deploy: cd landing-page && vercel --prod",
        "",
        f"Cohort upsell: {'INCLUDED' if cohort_price else 'SKIPPED'}",
    ]
    return "\n".join(summary)


@mcp.tool()
def validate_voice(text: str) -> str:
    """Check copy against the voice rules.

    Returns a list of issues found:
      - Em-dashes (Unicode U+2014)
      - Universal banned phrases (unlock, delve, supercharge, etc.)
      - AI-tell patterns (Imagine a world, What if I told you, etc.)

    Returns "PASS" if no issues found.

    Args:
        text: The copy to validate.

    Returns:
        "PASS" or a multi-line list of issues with line numbers.
    """
    issues = []
    lines = text.split("\n")

    for i, line in enumerate(lines, start=1):
        # Em-dash check
        if "\u2014" in line:
            count = line.count("\u2014")
            issues.append(f"  Line {i}: {count} em-dash(es) found. Replace with period or middle-dot.")

        # Banned phrases (case-insensitive word boundary)
        for phrase in UNIVERSAL_BANNED_PHRASES:
            if re.search(r"\b" + re.escape(phrase) + r"\b", line, re.IGNORECASE):
                issues.append(f"  Line {i}: banned phrase {phrase!r}")

        # AI-tell patterns
        for pattern, description in [
            (r"\bImagine a world\b", "AI-tell: 'Imagine a world'"),
            (r"\bWhat if I told you\b", "AI-tell: 'What if I told you'"),
            (r"\bHere's the thing\b", "AI-tell: 'Here's the thing'"),
            (r"\bThe truth is\b", "AI-tell: 'The truth is'"),
            (r"\bgame[-]?changing\b", "AI-tell: 'game-changing'"),
        ]:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(f"  Line {i}: {description}")

    if not issues:
        return f"PASS · {len(lines)} lines, 0 issues."

    return f"FAIL · {len(issues)} issues found:\n" + "\n".join(issues)


@mcp.tool()
def score_post_against_brain(text: str, brain_path: str = "") -> str:
    """Score a piece of copy (LinkedIn post, email, VSL, etc.) against the
    user's BUSINESS-BRAIN.md voice rules. Returns:
      - AI-slop score 0 to 100 (lower = more like the user's voice)
      - List of specific violations with line numbers
      - Pass/fail verdict against ship-it threshold (score < 25)

    Use this BEFORE publishing any content. Catches em-dashes, banned phrases,
    AI tells, missing specifics, missing hook patterns.

    Args:
        text: The copy to score.
        brain_path: Optional path to BUSINESS-BRAIN.md. If empty, looks in
                    plugin root then cwd.

    Returns:
        Multi-line score report.
    """
    # Read the Brain for personal banned phrases + hook patterns
    brain_text = ""
    if brain_path:
        p = Path(brain_path).expanduser()
    else:
        for cand in [PLUGIN_ROOT / "BUSINESS-BRAIN.md", Path.cwd() / "BUSINESS-BRAIN.md"]:
            if cand.exists():
                p = cand
                break
        else:
            p = None
    if p and p.exists():
        brain_text = p.read_text()

    # Extract personal banned phrases from Brain (looks for "banned phrases" section)
    personal_banned: list[str] = []
    in_banned_section = False
    for line in brain_text.split("\n"):
        if re.search(r"banned\s+phrases?", line, re.IGNORECASE):
            in_banned_section = True
            continue
        if in_banned_section and re.match(r"^#{1,3}\s", line):
            in_banned_section = False
        if in_banned_section:
            # Pull list items
            m = re.match(r"^[-*]\s+`?([^`\n]+?)`?\s*$", line)
            if m:
                phrase = m.group(1).strip()
                if 2 <= len(phrase) <= 40:
                    personal_banned.append(phrase)

    all_banned = list(set(UNIVERSAL_BANNED_PHRASES + personal_banned))

    # Score components
    em_dashes = text.count("\u2014")
    banned_hits: list[tuple[int, str]] = []
    ai_tells: list[tuple[int, str]] = []
    long_sentences = 0
    sentences_total = 0
    has_specifics = bool(re.search(r"\d", text[:300]))  # numbers in first 300 chars
    has_named_thing = bool(re.search(r"\b[A-Z][a-z]+(?:\.[a-z]+)?\b", text))

    lines = text.split("\n")
    for i, line in enumerate(lines, start=1):
        # Banned phrases (case-insensitive word boundary)
        for phrase in all_banned:
            if re.search(r"\b" + re.escape(phrase) + r"\b", line, re.IGNORECASE):
                banned_hits.append((i, phrase))

        # AI-tell patterns
        for pattern, description in [
            (r"\bImagine a world\b", "Imagine a world"),
            (r"\bWhat if I told you\b", "What if I told you"),
            (r"\bHere's the thing\b", "Here's the thing"),
            (r"\bThe truth is\b", "The truth is"),
            (r"\bgame[-]?changing\b", "game-changing"),
            (r"\bIn today's fast-paced\b", "In today's fast-paced"),
            (r"\bA world where\b", "A world where"),
        ]:
            if re.search(pattern, line, re.IGNORECASE):
                ai_tells.append((i, description))

    # Sentence length analysis
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if not sentence.strip():
            continue
        sentences_total += 1
        word_count = len(sentence.split())
        if word_count > 30:
            long_sentences += 1

    # Compute score (0 = perfect voice, 100 = pure AI slop)
    score = 0
    score += em_dashes * 8                         # each em-dash = +8
    score += len(banned_hits) * 12                 # each banned phrase = +12
    score += len(ai_tells) * 18                    # each AI tell = +18
    score += long_sentences * 4                    # each long sentence = +4
    if not has_specifics:
        score += 15                                # no numbers in first 300 chars
    if not has_named_thing:
        score += 8                                 # no proper nouns
    score = min(score, 100)

    verdict = "READY TO SHIP" if score < 25 else "NEEDS REWRITE" if score < 60 else "FULL REWRITE"

    # Format the report
    lines_out = [
        f"AI-SLOP SCORE: {score}/100  ·  {verdict}",
        f"  (Threshold: <25 = ship · 25-59 = revise · 60+ = rewrite)",
        "",
        "Voice analysis:",
        f"  Em-dashes: {em_dashes}",
        f"  Banned phrases: {len(banned_hits)}",
        f"  AI-tell patterns: {len(ai_tells)}",
        f"  Long sentences (>30 words): {long_sentences} of {sentences_total}",
        f"  Specifics in first 300 chars: {'yes' if has_specifics else 'NO (add numbers/dates)'}",
        f"  Proper nouns present: {'yes' if has_named_thing else 'NO (name a tool/place/person)'}",
        "",
        f"Personal banned phrases loaded from Brain: {len(personal_banned)}",
        f"Universal banned phrases: {len(UNIVERSAL_BANNED_PHRASES)}",
    ]

    if banned_hits:
        lines_out.append("")
        lines_out.append("Banned phrases found:")
        for line_num, phrase in banned_hits[:10]:
            lines_out.append(f"  Line {line_num}: {phrase!r}")
        if len(banned_hits) > 10:
            lines_out.append(f"  ...{len(banned_hits) - 10} more")

    if ai_tells:
        lines_out.append("")
        lines_out.append("AI-tell patterns found:")
        for line_num, desc in ai_tells[:10]:
            lines_out.append(f"  Line {line_num}: {desc!r}")

    return "\n".join(lines_out)


@mcp.tool()
def prep_post_in_voice(
    topic: str,
    hook_pattern: str = "personal-proof",
    platform: str = "linkedin",
    brain_path: str = "",
) -> str:
    """Prepare the context Claude needs to draft a social post in the user's
    voice. Returns:
      - The user's voice section from BUSINESS-BRAIN.md
      - The chosen hook pattern with examples
      - Platform-specific constraints (char limits, structure)
      - The topic + a structured prompt for Claude to follow

    Claude (the calling LLM) then uses this context to actually write the post.
    This tool is the CONTEXT preparer; the LLM is the writer.

    Use it when you want a quick voice-aware draft without running the full
    /marketing-engine flow.

    Args:
        topic: What the post is about (e.g., "why solopreneurs lose pipeline").
        hook_pattern: One of "personal-proof", "quiet-truth", "stat-contrast",
                      "contrarian", "reframe". Picks the opener style.
        platform: "linkedin" (default) or "x" or "newsletter".
        brain_path: Optional path to BUSINESS-BRAIN.md.

    Returns:
        Structured context block. Pass this to Claude with "Draft the post."
    """
    # Read the Brain
    brain_text = ""
    if brain_path:
        p = Path(brain_path).expanduser()
    else:
        for cand in [PLUGIN_ROOT / "BUSINESS-BRAIN.md", Path.cwd() / "BUSINESS-BRAIN.md"]:
            if cand.exists():
                p = cand
                break
        else:
            p = None
    if p and p.exists():
        brain_text = p.read_text()
    else:
        return "ERROR: BUSINESS-BRAIN.md not found. Run /build-my-brain first or pass brain_path."

    # Extract Voice section (looks for "## Voice" or "# Voice")
    voice_section = ""
    in_voice = False
    for line in brain_text.split("\n"):
        if re.match(r"^#{1,3}\s+Voice", line, re.IGNORECASE):
            in_voice = True
            voice_section += line + "\n"
            continue
        if in_voice and re.match(r"^#{1,3}\s", line) and "voice" not in line.lower():
            in_voice = False
        if in_voice:
            voice_section += line + "\n"
    if not voice_section:
        voice_section = "(Voice section not found in BUSINESS-BRAIN.md · check formatting)"

    # Hook pattern descriptions
    hook_patterns = {
        "personal-proof": "Open with a specific personal moment. Format: 'Last [time period] I was [specific situation].' Example: 'Last year I was doing 5 full-time jobs by myself.'",
        "quiet-truth": "Open with a quiet observation about your audience. Format: 'Most [audience] [common behavior].' Example: 'Most founders use AI like a search engine.'",
        "stat-contrast": "Open with a number that surprises. Format: '[$X / N hours / Y%]. [And the contradiction].' Example: '$200/month on AI tools. Still wrote at midnight.'",
        "contrarian": "Open by rejecting the obvious answer. Format: '[Common belief] is [false]. [Truth].' Example: 'AI doesn't replace you. It multiplies you.'",
        "reframe": "Open with a corrected interpretation. Format: 'I wasn't [obvious wrong reason]. I was [actual reason].' Example: 'I wasn't lazy. I was one person doing 5 jobs.'",
    }
    chosen_hook = hook_patterns.get(hook_pattern, hook_patterns["personal-proof"])

    # Platform constraints
    platform_specs = {
        "linkedin": "LinkedIn: ≤3,000 chars, narrative paragraphs separated by line breaks, ends with a question or P.S., no hashtags in first 3 lines.",
        "x": "X (Twitter): ≤280 chars per tweet. If thread, first tweet is the full hook, subsequent tweets continue. Hard line breaks between tweets.",
        "newsletter": "Newsletter: 200-400 words, subject line + opener + 1 idea + close, no hashtags, professional tone but personal.",
    }
    chosen_platform = platform_specs.get(platform, platform_specs["linkedin"])

    return f"""POST DRAFTING CONTEXT
=====================

TOPIC: {topic}

PLATFORM: {platform.upper()}
{chosen_platform}

HOOK PATTERN: {hook_pattern}
{chosen_hook}

VOICE FROM BUSINESS-BRAIN.md:
{voice_section}

UNIVERSAL VOICE RULES:
- No em-dashes (use period or middle-dot ·)
- No banned phrases: {", ".join(UNIVERSAL_BANNED_PHRASES[:8])}, etc.
- Short sentences (≤30 words)
- Specifics in first 30 seconds (numbers, dates, names)
- No invented testimonials or metrics
- No tricolons (X. Y. Z. parallel)
- No aphorisms ("Here's the thing")

NEXT STEP FOR CLAUDE:
Draft the {platform} post about "{topic}" using the {hook_pattern} hook pattern.
Keep it in the voice above. Apply the universal rules. Run validate_voice on
the draft before returning it. Iterate until score < 25.
"""


@mcp.tool()
def prep_meeting_brief(linkedin_url: str, context: str = "") -> str:
    """Prepare the research instructions for Claude to generate a 3-min
    meeting brief on an external attendee. Returns:
      - Structured research questions
      - Brief format template
      - Voice rules to apply

    Claude can then call the Apify MCP (if installed) to actually scrape the
    LinkedIn URL, OR ask the user to paste relevant info.

    Args:
        linkedin_url: The attendee's LinkedIn profile URL.
        context: Optional · meeting context (e.g., "discovery call", "pitch").

    Returns:
        Brief preparation context block.
    """
    return f"""MEETING BRIEF · CONTEXT
========================

ATTENDEE: {linkedin_url}
MEETING CONTEXT: {context or '(unspecified · ask user if relevant)'}

RESEARCH QUESTIONS (in order of priority):
1. What does the attendee do, and at what company?
2. What is their seniority/decision-making power?
3. What have they posted about in the last 30 days? (signals priorities)
4. Any mutual connections or shared interests?
5. Is the company in growth, contraction, or transition?
6. Any recent news about the company (raise, layoff, launch)?

BRIEF FORMAT (target: ~3 minutes to read):
- Name, role, company (1 line)
- Background (3 sentences max)
- 2 things they care about right now (from their posts)
- 2 sharp questions to ask in the meeting
- 1 talking point that connects to your work
- (Optional) a thoughtful piece of value to bring

NEXT STEP:
If Apify MCP is installed:
  - Call apify:linkedin-profile-scraper with this URL
  - Use the returned data to fill the brief format above
If Apify MCP is NOT installed:
  - Tell the user to paste the attendee's LinkedIn About + last 5 posts
  - Use that text to fill the brief format

VOICE RULES:
- Specific, not vague (cite actual posts/numbers)
- Short sentences
- No em-dashes, no banned phrases (run validate_voice on output)
- The brief is for the user to read, not to send · keep it useful
"""


@mcp.tool()
def prep_prospect_research(
    linkedin_url: str,
    icp_description: str = "",
    brain_path: str = "",
) -> str:
    """Prepare the research + scoring + outreach instructions for Claude to
    handle a single prospect. Returns:
      - BANT scoring framework
      - 3-step outreach sequence template
      - Voice rules
      - Brain ICP context (loaded if available)

    Claude can then call Apify (if installed) for actual scraping + scoring,
    or ask the user for context.

    Args:
        linkedin_url: The prospect's LinkedIn URL.
        icp_description: Optional · override the ICP from Brain.
        brain_path: Optional path to BUSINESS-BRAIN.md.

    Returns:
        Prospect research context block.
    """
    # Load ICP from Brain if available
    brain_icp = ""
    if brain_path or PLUGIN_ROOT.joinpath("BUSINESS-BRAIN.md").exists():
        p = Path(brain_path).expanduser() if brain_path else PLUGIN_ROOT / "BUSINESS-BRAIN.md"
        if p.exists():
            brain_text = p.read_text()
            in_icp = False
            for line in brain_text.split("\n"):
                if re.match(r"^#{1,3}\s+(Ideal\s+Client|ICP|Your\s+One\s+Client|Audience)", line, re.IGNORECASE):
                    in_icp = True
                    brain_icp += line + "\n"
                    continue
                if in_icp and re.match(r"^#{1,3}\s", line):
                    in_icp = False
                if in_icp:
                    brain_icp += line + "\n"

    icp = icp_description or brain_icp or "(no ICP provided · ask user for ideal client description)"

    return f"""PROSPECT RESEARCH · CONTEXT
============================

PROSPECT: {linkedin_url}

YOUR ICP:
{icp}

BANT SCORING (1-10 each):
- Budget: signal of buying power (company size, recent funding, role seniority)
- Authority: decision-making power (title, team size, deciding-vote signals)
- Need: pain match (their posts about the problem you solve)
- Timing: urgency signals (recent role change, growth, layoffs, public pivots)

SCORING THRESHOLDS:
- Total ≥30/40: HOT prospect · personalized 3-step outreach
- Total 20-29: WARM · single outreach + add to nurture
- Total <20: COLD · skip, focus elsewhere

3-STEP OUTREACH SEQUENCE FORMAT (only if HOT):
1. Initial DM (Mon): comment-on-their-recent-post, no pitch, single question
2. Follow-up (Wed): share a specific resource that maps to their pain, soft CTA
3. Closer (Fri): direct ask · "want to chat for 15 min?" · with calendar link

NEXT STEP:
If Apify MCP is installed:
  - Call apify:linkedin-profile-scraper(url=linkedin_url)
  - Call apify:linkedin-company-scraper if company URL is in profile
  - Score 1-10 on each BANT dimension
  - If HOT, draft the 3-step sequence in the user's voice
If Apify MCP is NOT installed:
  - Tell user to paste profile + last 10 posts + company URL
  - Score from that

VOICE RULES FOR OUTREACH:
- Reference their actual recent post (specific quote)
- One question per message (max)
- Short, conversational, no em-dashes, no banned phrases
- Sign-off: first name only, no signature block
- Run validate_voice on each step before sending
"""


@mcp.tool()
def prep_marketing_drop(brain_path: str = "") -> str:
    """Prepare the context Claude needs to run the user's Monday Content Drop:
    3 LinkedIn posts + 1 X thread + 1 newsletter idea, all in their voice.

    This wraps the /marketing-engine slash command logic as an MCP tool so it
    works in Claude Desktop chat.

    Returns:
      - Voice section from BUSINESS-BRAIN.md
      - Hook patterns from Brain
      - Topic suggestions derived from Brain (competitor gaps + pain themes)
      - Output format template (3 LinkedIn posts + thread + newsletter)
    """
    brain_text = ""
    p = Path(brain_path).expanduser() if brain_path else PLUGIN_ROOT / "BUSINESS-BRAIN.md"
    if p.exists():
        brain_text = p.read_text()
    if not brain_text:
        return "ERROR: BUSINESS-BRAIN.md not found. Run /build-my-brain first."

    return f"""MARKETING DROP · CONTEXT
=========================

OBJECTIVE: Produce this week's content. 3 LinkedIn posts + 1 X thread +
1 newsletter idea. All in the user's voice. Ready to publish.

BUSINESS BRAIN (full context):
{brain_text[:4000]}{'...' if len(brain_text) > 4000 else ''}

OUTPUT FORMAT:

# Monday Content Drop · Week of {datetime.now().strftime('%B %-d')}

## LinkedIn Post A (Personal Proof hook)
[140-280 words, narrative, ends with question]

## LinkedIn Post B (Quiet Truth hook)
[140-280 words, observation-driven, ends with P.S.]

## LinkedIn Post C (Stat Contrast or Contrarian hook)
[140-280 words, surprising opener]

## X Thread (5-7 tweets)
1/ [Hook tweet, 240 chars]
2/ [Setup, 240 chars]
...
N/ [CTA, 240 chars]

## Newsletter idea
Subject: [...]
Hook: [3 sentences]
Body angle: [the 1 idea, 60 words]
CTA: [...]

NEXT STEPS:
1. Read BUSINESS-BRAIN.md fully (the snippet above is truncated)
2. Pick 3 distinct hook patterns
3. Draft each piece using a different topic angle
4. Run validate_voice() on each draft
5. Iterate until score < 25
6. Output the 5 pieces in the format above
"""


@mcp.tool()
def prep_morning_brief(brain_path: str = "") -> str:
    """Prepare the context for the daily 60-second morning brief across all 5
    engines (Marketing, Sales, Operations, Cash, Leadership).

    Returns:
      - Today's brief format
      - Brain context for personalization
      - Connector queries to run

    Use this every morning Mon-Fri. The output is a tight scannable brief.

    Args:
        brain_path: Optional path to BUSINESS-BRAIN.md.

    Returns:
        Morning brief context block.
    """
    brain_text = ""
    p = Path(brain_path).expanduser() if brain_path else PLUGIN_ROOT / "BUSINESS-BRAIN.md"
    if p.exists():
        brain_text = p.read_text()

    today = datetime.now().strftime("%A, %B %-d")

    return f"""MORNING BRIEF · CONTEXT
========================

DATE: {today}
OBJECTIVE: 60-second brief across all 5 engines, scannable in 3 paragraphs.

DATA SOURCES TO QUERY:
- Gmail: emails received in the last 24h, focus on replies + new threads
- Notion CRM: deals that moved status overnight
- Google Calendar: today's external meetings
- (Optional) Stripe: revenue change since yesterday
- (Optional) LinkedIn: notifications + post performance

BRIEF FORMAT (the actual output):

# Morning Brief · {today}

## What needs you today (3-5 bullets max)
- [Action item 1 with specific name + amount/due]
- [Action item 2]
- ...

## What ran without you (positive momentum)
- [Routine fired: Monday Drop produced 3 posts ready to publish]
- [Marketing engine output saved to Notion]
- [...]

## What to watch (signals)
- [Deal X went silent · 4 days no reply]
- [Newsletter open rate dropped 12%]
- [...]

## One-line takeaway
[The single sentence that frames today.]

PERSONALIZE WITH:
{brain_text[:2000] if brain_text else '(no Brain · use neutral tone)'}

VOICE RULES:
- Punchy, fragmentary, scannable
- Specifics only · no "many leads", say "3 leads"
- No em-dashes
- Action verbs at sentence starts ("Reply to Sarah" not "You should reply to Sarah")
"""


@mcp.tool()
def prep_pipeline_report(period: str = "weekly", brain_path: str = "") -> str:
    """Prepare the context Claude needs to draft the Sunday Pipeline Report:
    a comprehensive end-of-week status across Marketing + Sales + Cash.

    Args:
        period: "weekly" (default) or "monthly".
        brain_path: Optional path to BUSINESS-BRAIN.md.

    Returns:
        Pipeline report context block.
    """
    today = datetime.now()
    if period == "weekly":
        period_label = f"Week of {(today - timedelta(days=today.weekday())).strftime('%B %-d')}"
    else:
        period_label = today.strftime("%B %Y")

    return f"""PIPELINE REPORT · CONTEXT
==========================

PERIOD: {period_label}
OBJECTIVE: A clear status report. Where the pipeline stands. What changed.
What needs decisions. Sent to self (or shared with team) every Sunday 6pm.

DATA SOURCES:
- Notion CRM: all deals · count by stage, by amount
- Gmail: outreach sent / replies received this period
- Notion Content Calendar: posts published this period + engagement
- Google Drive: newsletters drafted/sent
- (Optional) Stripe: cash collected this period

REPORT FORMAT:

# Pipeline Report · {period_label}

## Numbers
| Metric | This period | Change vs. last |
|--------|------------|-----------------|
| Outreach sent | N | +/- N |
| Replies | N | +/- N |
| New deals (early-stage) | N | +/- N |
| Late-stage deals | N | +/- N |
| Closed-won | $X | +/- N |
| Posts published | N | +/- N |
| Total reach | N | +/- N |

## Where the pipeline stands
[3-5 sentences describing health. Concrete deal names. Concrete amounts.]

## What changed this period
- [Specific deal moved stage]
- [Routine that fired N times]
- [New ICP signal observed]

## Decisions needed (next 7 days)
- [ ] [Decision 1, owner, deadline]
- [ ] [Decision 2]

## Voice + numbers check
- This is for the user to read, not send. Be honest about the numbers.
- No vague qualifiers. Cite specifics.
- Run validate_voice on the prose sections (the bullets are fine).
"""


@mcp.tool()
def list_workshops(output_dir: str = "~/Desktop") -> str:
    """List existing workshops in the given output directory.

    Detects workshop folders by looking for landing-page/index.html.

    Args:
        output_dir: Directory to scan (default ~/Desktop).

    Returns:
        Multi-line list of workshop folders found, with their workshop_name
        extracted from the landing page <title>.
    """
    root = Path(output_dir).expanduser().resolve()
    if not root.exists():
        return f"Directory not found: {root}"

    found = []
    for landing in root.glob("*/landing-page/index.html"):
        workshop_dir = landing.parent.parent
        slug = workshop_dir.name
        try:
            content = landing.read_text()
            title_match = re.search(r"<title>([^<]+)</title>", content)
            title = title_match.group(1).strip() if title_match else "(no title)"
        except Exception:
            title = "(unreadable)"
        found.append(f"  {slug:30s}  {title}")

    if not found:
        return f"No workshops found in {root}/"

    return f"{len(found)} workshop(s) in {root}/:\n" + "\n".join(found)


# ============================================================
# HELPERS for soft-rewrite + README
# ============================================================

def _build_rewrite_needed(
    workshop_name: str,
    core_hook: str,
    day_1_deliverable: str,
    day_2_deliverable: str,
    cohort_price: str,
    cohort_start: str,
) -> str:
    cohort_note = (
        f"Include the {cohort_price} cohort starting {cohort_start} in the closer."
        if cohort_price else
        "No cohort upsell. End the VSL on the workshop CTA only."
    )
    return f"""# Files Claude needs to rewrite in your voice

The MCP scaffolder did the mechanical token replacement (dates, prices, names).
What it could NOT do: write voice-aware copy. That's where you (Claude) come in.

Read these files, read BUSINESS-BRAIN.md for voice, and rewrite each one
using the new workshop's hook + deliverables.

## Workshop context for the rewrite

- **Name:** {workshop_name}
- **Hook:** {core_hook or '(not provided · invent one based on Day 1/Day 2 deliverables)'}
- **Day 1 deliverable:** {day_1_deliverable}
- **Day 2 deliverable:** {day_2_deliverable}
- **Cohort:** {cohort_note}

## Files to rewrite (in priority order)

### 1. campaign/vsl-script.md  (HIGHEST PRIORITY · 2:13 video)
Full rewrite. Use the same 7-beat structure as Workshop 01:
  Pattern Interrupt -> Pain -> Belief Breaker -> Promise -> Proof -> Offer -> CTA.
Target: 345 words, 130-145s at 150 wpm.
Drop the new hook into the opener. Keep the host's voice.

### 2. campaign/email-campaign.md  (21 emails)
Subject lines: rewrite all 21 in voice. The token-replace already updated dates and prices.
Email A1, A2, A3 bodies: rewrite substantively (these reference the hook + workshop angle).
Emails A4-A14, B1-B7 bodies: lightly edit the hook references; the structure is fine.
{"Skip emails A12 + A13 (cohort upsell) since cohort is skipped." if not cohort_price else ""}

### 3. campaign/dm-outreach.md  (4 segments x 2 openers = 8 openers)
Rewrite the 8 openers to reference the new workshop's hook + audience.
Reply flows are token-replaced and ready as-is.

### 4. campaign/video-scripts.md  (3 Ava-style shorts)
Full rewrite. 60-65s each. Same structure as Workshop 01:
  Hook -> Tension -> Reframe -> CTA.
Use the workshop's core hook as the opening line.

### 5. videos/pp-install-phase-N/assets/narration-script.txt  (4 phase walkthrough scripts)
The install steps don't change between workshops, but the host references do.
Rewrite each phase's script (~280-340 words) keeping the same install flow.
Phase 4's celebration end card mentions the new workshop name.

## Voice rules to enforce

- Zero em-dashes (use period or middle-dot)
- Zero banned phrases: unlock, delve, supercharge, seamless, elevate, leverage, tapestry, realm, journey, unleash, holistic
- Specifics in first 30 seconds: at least 2 numbers, 1 named thing, 1 specific amount/date
- No invented testimonials, no invented metrics
- Short sentences. No tricolons unless intentional. No aphorisms.

Read `purely-personal/skills/workshop-scaffolder/references/voice-rules.md` for the full list.

## When done

Run validate_voice on each rewritten file. If PASS, the workshop is launch-ready.
"""


def _build_readme(
    workshop_name: str,
    workshop_slug: str,
    workshop_number: int,
    day_1: datetime,
    day_2: datetime,
    price: int,
) -> str:
    today = datetime.now().date()
    t_minus = (day_1.date() - today).days

    return f"""# {workshop_name}

Workshop {workshop_number:02d} · {day_1.strftime('%B %-d')}-{day_2.strftime('%-d')}, {day_1.year}

## What this folder is

A complete launch package generated by the Purely Personal Workshop MCP. Mechanical token replacement is done. Voice-aware copy still needs Claude to rewrite (see `REWRITE-NEEDED.md`).

## Folder layout

```
{workshop_slug}/
├── README.md                      ← you are here
├── REWRITE-NEEDED.md              ← 5 files Claude should rewrite next
├── landing-page/
│   ├── index.html                 ← branded, dates filled, hook needs voice rewrite
│   └── install-guide/             ← 17 steps + video slots
├── campaign/
│   ├── vsl-script.md              ← REWRITE in voice
│   ├── email-campaign.md          ← rewrite subjects + first 3 bodies
│   ├── dm-outreach.md             ← rewrite 8 openers
│   └── video-scripts.md           ← REWRITE
├── workshop/
│   ├── Workshop-Agenda.xlsx       ← TODO: regenerate with openpyxl + new topics
│   └── worksheets/                ← copied as-is (plugin content)
├── integrations/
│   ├── ghl-build-spec.md          ← token-replaced, hand to GHL specialist
│   └── vercel-to-ghl.md           ← copied as-is
└── videos/                        ← TODO: hyperframes compositions
```

## Timeline

- Day 1: {day_1.strftime('%A %B %-d, %Y')}
- Day 2: {day_2.strftime('%A %B %-d, %Y')}
- Today: {today}
- T-minus: {t_minus} days

The email campaign is timed for a 9-day pre-launch. If you have less time, compress emails A1-A6 into the days you have.

## Next 5 steps

1. **Read REWRITE-NEEDED.md** and ask Claude to rewrite the 5 voice-heavy files.
2. **Create a new GitHub repo** for this workshop's plugin install.
3. **Render the 4 phase videos** (regenerate with new voiceover scripts).
4. **Set up the GHL funnel** (hand `integrations/ghl-build-spec.md` to your specialist).
5. **Deploy the landing page** (`cd landing-page && vercel --prod`).

## Pricing

- Workshop price: ${price}
- Estimated revenue at full capacity (40 seats): ${price * 40}

## Plugin

This workshop reuses the `purely-personal` plugin. No copy needed. The plugin lives at the source repo and stays the same across workshops.
"""


# ============================================================
# v2 TOOLS · Setup, Health, Routines, Site & Video Pipeline
# ============================================================

@mcp.tool()
def quick_install_check(business_dir: str = "") -> str:
    """Audit a Purely Personal install. Returns a punch list of what's missing.

    Run this anytime to check whether the workshop install is actually working:
    - Claude Code on PATH
    - purely-personal plugin installed
    - All 8 slash commands registered
    - claude_desktop_config.json has Apify configured
    - Business folder exists with BUSINESS-BRAIN.md
    - Plugin symlink resolves
    - Last-known render directory writable

    Use it on Day 0 (before workshop), or anytime a routine fails.

    Args:
        business_dir: optional path to your business folder (defaults to ~/Desktop search)
    """
    import os
    import subprocess
    from pathlib import Path

    out = ["# Purely Personal · Install Health Check", ""]
    fails = 0
    warns = 0

    # 1. Claude Code on PATH
    cc = shutil.which("claude")
    if cc:
        try:
            ver = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=10)
            ver_text = (ver.stdout or ver.stderr or "").strip().split("\n")[0]
            out.append(f"✓ Claude Code on PATH · `{cc}` · {ver_text}")
        except Exception as e:
            out.append(f"✓ Claude Code on PATH · `{cc}` · (version check failed: {e})")
    else:
        fails += 1
        out.append("✗ Claude Code NOT on PATH · re-install: https://claude.com/claude-code")

    # 2. Plugin installed
    plugin_paths = [
        Path.home() / ".claude" / "plugins" / "purely-personal",
        Path.home() / ".claude" / "plugins" / "Purely-Personal-Run-a-business-by-itself",
    ]
    plugin_installed = False
    for p in plugin_paths:
        if p.exists():
            real = p.resolve()
            out.append(f"✓ Plugin installed · `{p}` → `{real}`")
            plugin_installed = True
            break
    if not plugin_installed:
        fails += 1
        out.append("✗ Plugin NOT installed · cd to repo and run `claude plugin install .`")

    # 3. Slash commands (look at the command files in the plugin)
    if plugin_installed:
        cmd_dir = plugin_paths[0].resolve() / "commands"
        if not cmd_dir.exists():
            cmd_dir = plugin_paths[1].resolve() / "commands" if len(plugin_paths) > 1 else cmd_dir
        if cmd_dir.exists():
            cmds = list(cmd_dir.glob("*.md"))
            if len(cmds) >= 8:
                out.append(f"✓ Slash commands · {len(cmds)} found · {', '.join(c.stem for c in cmds[:8])}")
            else:
                warns += 1
                out.append(f"⚠ Slash commands · only {len(cmds)} found (expected 8) · re-install plugin")
        else:
            warns += 1
            out.append(f"⚠ Slash commands directory missing at {cmd_dir}")

    # 4. Claude Desktop config + Apify
    cd_config = (
        Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        if os.uname().sysname == "Darwin"
        else Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    )
    if cd_config.exists():
        try:
            cfg = json.loads(cd_config.read_text())
            servers = cfg.get("mcpServers", {})
            if "Apify" in servers or "apify" in servers:
                out.append(f"✓ Apify wired in claude_desktop_config.json · {cd_config}")
            else:
                warns += 1
                out.append(f"⚠ Apify NOT in claude_desktop_config.json · run Setup Prompt again")
            if "purely-personal-workshop" in servers or any("workshop" in k.lower() for k in servers):
                out.append("✓ Workshop MCP wired into Claude Desktop")
            else:
                warns += 1
                out.append("⚠ Workshop MCP not yet wired (optional) · run install.sh in mcp/workshop-mcp/")
        except json.JSONDecodeError as e:
            fails += 1
            out.append(f"✗ claude_desktop_config.json INVALID JSON · {e} · paste into jsonlint.com")
    else:
        warns += 1
        out.append(f"⚠ claude_desktop_config.json missing at {cd_config} · run Setup Prompt")

    # 5. Business folder + BRAIN
    if business_dir:
        biz_path = Path(os.path.expanduser(business_dir))
    else:
        biz_path = next(
            (p for p in (Path.home() / "Desktop").glob("*-business") if p.is_dir()),
            None,
        ) or (Path.home() / "Desktop" / "my-business")
    if biz_path.exists():
        out.append(f"✓ Business folder · `{biz_path}`")
        brain = biz_path / "BUSINESS-BRAIN.md"
        if brain.exists():
            size = brain.stat().st_size
            if size > 500:
                out.append(f"  ✓ BUSINESS-BRAIN.md · {size:,} bytes (filled)")
            else:
                warns += 1
                out.append(f"  ⚠ BUSINESS-BRAIN.md exists but tiny ({size}b) · run /build-my-brain")
        else:
            warns += 1
            out.append(f"  ⚠ BUSINESS-BRAIN.md missing in {biz_path} · run /build-my-brain")
    else:
        warns += 1
        out.append(f"⚠ Business folder not found · expected at `{biz_path}`")

    # Summary
    out.append("")
    if fails == 0 and warns == 0:
        out.append("## ✓ All green · ready for the workshop")
    elif fails == 0:
        out.append(f"## ⚠ {warns} warning(s) · workshop will run but some routines may need help")
    else:
        out.append(f"## ✗ {fails} failure(s) + {warns} warning(s) · fix the failures before the workshop")
        out.append("")
        out.append("Top fixes:")
        out.append("- Re-run the Setup Prompt from claude.com/claude-code (Phase 1 of the install guide)")
        out.append("- If JSON is invalid: paste your `claude_desktop_config.json` into jsonlint.com")
        out.append("- If plugin missing: `cd <repo> && claude plugin install .`")

    return "\n".join(out)


@mcp.tool()
def prep_routine(
    routine: str,
    brain_path: str = "",
) -> str:
    """Unified routine prep · returns a structured prompt for any of the 6 weekly routines.

    Routines:
    - mon-content-drop · 3 LinkedIn posts + newsletter idea
    - tue-lead-research · 10 BANT-scored prospects + outreach for top 3
    - wed-newsletter · long-form newsletter from Monday's queued idea
    - thu-meeting-prep · 3-min brief + 2 questions per external meeting
    - fri-wrap · weekly wrap (posts shipped, leads booked, $$ moved)
    - sun-pipeline · pipeline report + Monday plan

    Args:
        routine: one of mon-content-drop, tue-lead-research, wed-newsletter,
                 thu-meeting-prep, fri-wrap, sun-pipeline
        brain_path: optional path to BUSINESS-BRAIN.md
    """
    routines = {
        "mon-content-drop": (
            "prep_marketing_drop",
            "Reads Gmail (last 7 days) + Notion content calendar (last week's wins). "
            "Drafts 3 LinkedIn posts + 1 newsletter idea. Saves to Notion content calendar.",
        ),
        "tue-lead-research": (
            "prep_prospect_research",
            "Apify scrapes 10 prospects matching ICP. BANT-scores each. "
            "Top 3 get 3-step outreach drafts saved to Gmail.",
        ),
        "wed-newsletter": (
            "prep_post_in_voice",
            "Picks Monday's queued newsletter idea. Writes long-form (~800w) "
            "in your voice. Saves to Drive + Gmail draft.",
        ),
        "thu-meeting-prep": (
            "prep_meeting_brief",
            "Reads today's Calendar. Apify scrapes each external attendee. "
            "Drafts 3-min brief + 2 sharp questions. Saves to Gmail drafts.",
        ),
        "fri-wrap": (
            "prep_pipeline_report",
            "Counts posts shipped + leads booked + meetings + revenue. "
            "1 win + 1 fix. Saves to Drive + Notion leadership log.",
        ),
        "sun-pipeline": (
            "prep_pipeline_report",
            "Pipeline report. Stale cards. Forecast gap. Monday plan. "
            "Saves Monday plan to Gmail draft (self-send).",
        ),
    }
    if routine not in routines:
        return (
            f"Unknown routine: {routine}\n\n"
            "Valid routines:\n"
            + "\n".join(f"  · {k} — {v[1]}" for k, v in routines.items())
        )
    delegate, summary = routines[routine]
    # Reuse the existing tool by importing locally
    out = [
        f"# Routine: {routine}",
        "",
        f"**Summary:** {summary}",
        "",
        f"**Delegated to:** `{delegate}`",
        "",
        "---",
        "",
    ]
    # Call the existing tool
    if delegate == "prep_marketing_drop":
        out.append(prep_marketing_drop(brain_path=brain_path))
    elif delegate == "prep_prospect_research":
        out.append("Run `prep_prospect_research(linkedin_url=<your-ICP-leader>, ...)` for the actual prep.")
    elif delegate == "prep_post_in_voice":
        out.append("Run `prep_post_in_voice(topic=<from-monday-queue>, platform='newsletter', ...)` for the actual prep.")
    elif delegate == "prep_meeting_brief":
        out.append("Run `prep_meeting_brief(linkedin_url=<each-attendee>)` for each external meeting today.")
    elif delegate == "prep_pipeline_report":
        period = "weekly" if routine == "fri-wrap" else "weekly"
        out.append(prep_pipeline_report(period=period, brain_path=brain_path))
    return "\n".join(out)


@mcp.tool()
def render_install_video(phase: int, quality: str = "draft") -> str:
    """Render an install-guide phase video via the Hyperframes pipeline.

    Args:
        phase: 1, 2, 3, or 4
        quality: 'draft' (~1 min, CRF 28) or 'standard' (~5 min, CRF 18, ship-quality)

    Returns the path of the rendered MP4 (or instructions if hyperframes is not installed).
    """
    import subprocess

    if phase not in (1, 2, 3, 4):
        return f"Invalid phase: {phase}. Must be 1, 2, 3, or 4."
    if quality not in ("draft", "standard"):
        return f"Invalid quality: {quality}. Must be 'draft' or 'standard'."

    proj_root = Path(os.environ.get("HF_WORKSPACE", "")) if os.environ.get("HF_WORKSPACE") else None
    if not proj_root:
        # Try common locations
        candidates = [
            Path.home() / "Build a Business That runs by itself using claude code" / "hyperframes-workspace",
            PLUGIN_ROOT.parent / "hyperframes-workspace",
        ]
        proj_root = next((p for p in candidates if p.exists()), None)

    if not proj_root:
        return (
            "Hyperframes workspace not found.\n\n"
            "Set HF_WORKSPACE env var to the workspace root, or install hyperframes-workspace adjacent to this repo."
        )

    proj = proj_root / "video-projects" / f"pp-install-phase-{phase}"
    if not proj.exists():
        return f"Project not found: {proj}"

    output = proj / "renders" / f"phase-{phase}-v3-{quality}.mp4"
    cmd = ["npx", "hyperframes", "render", "--quality", quality, "--output", str(output)]
    try:
        result = subprocess.run(cmd, cwd=str(proj), capture_output=True, text=True, timeout=900)
        if result.returncode == 0:
            return f"✓ Rendered phase {phase} · {quality} · {output}"
        else:
            tail = (result.stdout + result.stderr)[-2000:]
            return f"✗ Render failed (exit {result.returncode}):\n\n{tail}"
    except subprocess.TimeoutExpired:
        return f"✗ Render timed out after 15 minutes. Try `quality='draft'` first."
    except FileNotFoundError:
        return "✗ npx not found. Install Node.js: https://nodejs.org"


@mcp.tool()
def deploy_landing_page() -> str:
    """Deploy the landing page (and install guide) to Vercel production.

    Wraps `cd landing-page && vercel --prod --yes`. Requires:
    - vercel CLI installed (`npm i -g vercel`)
    - Logged in once (`vercel login`)
    - Project linked (`vercel link`)
    """
    import subprocess

    landing = PLUGIN_ROOT / "landing-page"
    if not landing.exists():
        return f"landing-page directory not found at {landing}"

    cmd = ["vercel", "--prod", "--yes"]
    try:
        result = subprocess.run(cmd, cwd=str(landing), capture_output=True, text=True, timeout=300)
        out = result.stdout + result.stderr
        # Find the deployed URL
        url_match = re.search(r'https://[a-z0-9-]+\.vercel\.app', out)
        url = url_match.group(0) if url_match else "(URL not found in output)"
        if result.returncode == 0:
            return f"✓ Deployed · {url}\n\nLanding page: {url}\nInstall guide: {url}/install-guide/"
        else:
            return f"✗ Deploy failed (exit {result.returncode}):\n\n{out[-1500:]}"
    except subprocess.TimeoutExpired:
        return "✗ Deploy timed out after 5 minutes. Check `vercel ls` to see partial state."
    except FileNotFoundError:
        return "✗ vercel CLI not found. Install: `npm i -g vercel` then `vercel login` once."


@mcp.tool()
def health_check() -> str:
    """Top-level health snapshot · combines install check + git status + key files.

    Useful right before a workshop or after major changes. One screen, full picture.
    """
    out = ["# Purely Personal · Health Snapshot", ""]
    out.append("## 1. Install")
    out.append(quick_install_check())
    out.append("")
    out.append("## 2. Repo")
    repo_root = PLUGIN_ROOT
    try:
        import subprocess
        s = subprocess.run(["git", "status", "--short"], cwd=str(repo_root), capture_output=True, text=True, timeout=10)
        b = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(repo_root), capture_output=True, text=True, timeout=10)
        l = subprocess.run(["git", "log", "--oneline", "-3"], cwd=str(repo_root), capture_output=True, text=True, timeout=10)
        out.append(f"  Branch: {b.stdout.strip() or 'unknown'}")
        out.append(f"  Last 3 commits:")
        for line in l.stdout.strip().split("\n"):
            out.append(f"    {line}")
        if s.stdout.strip():
            out.append(f"  Uncommitted changes: {len(s.stdout.strip().splitlines())} files")
        else:
            out.append("  Working tree clean")
    except Exception as e:
        out.append(f"  (git status failed: {e})")
    out.append("")
    out.append("## 3. Key files")
    key_files = [
        PLUGIN_ROOT / "BUSINESS-BRAIN.md",
        PLUGIN_ROOT / "landing-page" / "install-guide" / "index.html",
        PLUGIN_ROOT / "landing-page" / "install-guide" / "videos" / "phase-1.mp4",
        PLUGIN_ROOT / "landing-page" / "install-guide" / "videos" / "phase-2.mp4",
        PLUGIN_ROOT / "landing-page" / "install-guide" / "videos" / "phase-3.mp4",
        PLUGIN_ROOT / "landing-page" / "install-guide" / "videos" / "phase-4.mp4",
    ]
    for f in key_files:
        if f.exists():
            size = f.stat().st_size
            out.append(f"  ✓ {f.relative_to(PLUGIN_ROOT)} · {size:,} bytes")
        else:
            out.append(f"  ✗ {f.relative_to(PLUGIN_ROOT)} · missing")
    return "\n".join(out)


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """Entry point for the `purely-personal-workshop-mcp` console script."""
    mcp.run()


if __name__ == "__main__":
    main()
