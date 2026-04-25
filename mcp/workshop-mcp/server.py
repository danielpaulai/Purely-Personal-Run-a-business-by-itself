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
# MAIN
# ============================================================

if __name__ == "__main__":
    mcp.run()
