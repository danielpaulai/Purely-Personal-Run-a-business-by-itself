"""Lints for the bundled program skills. Each test is one defect from the skill-bundle review; if a skill is re-synced from Drive
without running scripts/clean_skills.py, these fail."""
import re
from pathlib import Path

import pytest

from pp_mcp import skills as sk
from pp_mcp import voice

ROOT = Path(sk.SKILLS_DIR)
FILES = sorted(p for p in ROOT.rglob("*.md") if p.parts[-3:-1] != ("newsletter-writer",) and "newsletter-writer" not in p.parts)


def body(p: Path) -> str:
    t = p.read_text()
    return re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S)  # ignore frontmatter metadata (author tag)


def served_text(name: str) -> str:
    return sk.skill_md(name)


# 1. garbled banned-word lists -------------------------------------------------------------------------------------------
GARBLE = {"use", "open up", "big", "help", "path", "go deep", "handle", "improve", "solid", "whole", "fit", "brainstorm", "model", "today", "change"}


def banned_list_lines(text: str):
    for l in text.split("\n"):
        if re.search(r"banned|AI tells?|forbidden|default screen|✗", l, re.I):
            yield l


def test_no_banned_list_contains_plain_everyday_words():
    bad = []
    for p in FILES:
        for l in banned_list_lines(body(p)):
            items = re.findall(r"[\"`]([^\"`]{2,40})[\"`]", l) + [x.strip() for x in re.findall(r"\(([^()]*,[^()]*)\)", l) for x in x.split(",")]
            for it in items:
                if it.strip().lower() in GARBLE:
                    bad.append((p.name, l.strip()[:110]))
    assert not bad, bad


def test_no_banned_list_repeats_a_word():
    for p in FILES:
        for l in banned_list_lines(body(p)):
            m = re.search(r"`([^`]+,[^`]+)`", l)
            if m:
                items = [x.strip().lower() for x in m.group(1).split(",")]
                assert len(items) == len(set(items)), (p.name, l[:140])


def test_every_skill_with_a_default_banned_screen_uses_the_programs_real_list():
    t = sk.skill_md("voice-profile-builder")
    for w in ("leverage", "unlock", "game-changing", "empower", "journey", "dive deep", "navigate"):
        assert w in t
    for l in ("invisibility-diagnostic", "multi-platform-amplifier", "linkedin-post-writer"):
        assert re.search(r"leverage, unlock", sk.skill_md(l)), l


def test_de_ai_ify_never_swaps_a_tell_for_another_tell_or_a_garbled_word():
    banned = {w.lower() for w in voice.BANNED_STEMS} | {"leverage", "unlock", "empower", "elevate", "navigate", "journey", "game-changing", "dive deep"}
    for src, dst in list(voice.SWAPS.items()):
        assert dst.lower() not in banned and dst.lower() not in {"open up", "big", "help", "path", "go deep", "handle"}, (src, dst)
    cleaned, _ = voice.mechanical_clean("We unlock potential, empower teams and navigate change. A game-changing, robust idea.")
    assert "open up" not in cleaned and "big " not in cleaned


# 2. one length standard -------------------------------------------------------------------------------------------------
def test_one_post_length_standard_everywhere():
    for p in FILES:
        t = body(p)
        assert not re.search(r"\b150[- ]words?\b", t), p.name
        assert not re.search(r"under 220 words", t, re.I), p.name
    assert voice.PLATFORMS["linkedin"][:2] == (1300, 1500)
    for n in ("linkedin-post-writer", "first-post-coach", "ai-marketing-employee", "invisibility-diagnostic", "voice-profile-builder"):
        assert re.search(r"1300", sk.skill_md(n)), n


# 4. anti-invention ------------------------------------------------------------------------------------------------------
FABRICATED = ["47 likes", "8 DMs", "2,000+", "5+ Calls", "4 billion", "1.9M", "GBI Online", "312 attendees", "real-feeling", "Mehsum", "production-tested",
              "Production-tested", "Calibrated against", "Pattern-matched against"]


def test_no_invented_proof_points_or_claims():
    for p in FILES:
        t = body(p)
        for f in FABRICATED:
            assert f not in t, (p.name, f)


def test_examples_are_labelled_illustrative_only():
    for p in ROOT.glob("*/SKILL.md"):
        if "newsletter" in str(p) or "homework" in str(p):
            continue
        t = p.read_text()
        if re.search(r"^##\s+Examples?", t, re.M):
            assert "Illustrative only" in t, p


def test_first_post_coach_does_not_tell_users_to_invent_a_client():
    t = sk.skill_md("first-post-coach")
    assert "never invent" in t.lower() and "real-feeling" not in t


# 5. sample copy follows the style rules ---------------------------------------------------------------------------------
def test_sample_copy_has_no_filler_markers_or_negation_pivots():
    for p in FILES:
        assert not re.search(r"Real talk", body(p), re.I), p.name
    t = sk.skill_md("linkedin-post-writer")
    m = re.search(r"\*\*Output \(sample\):\*\*\n```\n(.*?)\n```", t, re.S)
    assert m
    sample = m.group(1).split("---")[0]
    bad = [x for x in voice.find_tells(sample, []) if x.kind in ("contrast-frame", "em-dash", "banned-word", "banned-phrase", "banned-transition", "banned-closing", "tidy-moral")]
    assert not bad, [b.render() for b in bad]


def test_carousel_slides_are_short():
    for rel in ("new-carousel.md", "intent-carousel.md"):
        t = (ROOT / "linkedin-carousel-builder/prompts" / rel).read_text()
        assert "2-3 sentences" not in t and "10-15 words each" not in t
    t = (ROOT / "linkedin-carousel-builder/prompts/new-carousel.md").read_text()
    assert "20 words maximum" in t and "6 words maximum" in t


# 6. nothing points at things that do not exist here ---------------------------------------------------------------------
DANGLING = ["render.py", "~/.claude", "scripts/", "template.html", "ICP Builder", "workbook", "cold-outreach-sequence", "content-multiplier",
            "supreme_coder", "APIFY_TOKEN", "Apify token", ".jsx", "de-ai-ify", "find-prospects.py", "voice-extractor", "Notion-extracted"]


def test_no_references_to_missing_files_skills_or_tools():
    for p in FILES:
        t = body(p)
        for d in DANGLING:
            assert d not in t, (p.relative_to(ROOT), d)


def test_visual_html_modes_are_gone_but_explained():
    for p in ROOT.glob("*/SKILL.md"):
        if "newsletter" in str(p):
            continue
        t = body(p)
        assert not re.search(r"^\|\s*`?visual`?", t, re.M), p
        assert "Output Structure (`visual`" not in t and "Output structure (`visual`" not in t and "(visual mode)" not in t, p
        assert "## Use in the Purely Personal connector" in t, p


def test_actors_named_are_the_verified_harvestapi_ones():
    t = sk.skill_md("prospect-magnet") + sk.skill_md("competitor-x-ray")
    assert "harvestapi/linkedin-profile-scraper" in t and "supreme_coder" not in t


# 7. built for the program's own cohort ----------------------------------------------------------------------------------
COHORT = [r"\bCET\b", r"\bCEST\b", r"Day 2", r"Day 1", r"\bon stage\b", r"\bstage\b", r"attendee", r"Game 1", r"AI Employee Challenge", r"Ilef", r"Eduardo", r"\bDaniel\b", r"\bcoordinator\b", r"Lesson \d", r"\bcohort\b"]


@pytest.mark.parametrize("pat", COHORT)
def test_no_cohort_specific_details_in_the_bundle(pat):
    hits = [(p.relative_to(ROOT).as_posix(), m.group(0)) for p in FILES for m in re.finditer(pat, body(p), re.I if pat in (r"\bstage\b", r"attendee", r"\bcohort\b") else 0)]
    assert not hits, hits[:8]


# the served work orders (what Claude is actually given) ------------------------------------------------------------------
def test_work_orders_contain_none_of_the_defects(maya):
    leak = re.compile("|".join(re.escape(x) for x in FABRICATED) + r"|Real talk|render\.py|ICP Builder|content-multiplier|\bCET\b|Day 2|Game 1|\bstage\b", re.I)
    calls = [("write_post", {"topic": "t"}), ("write_carousel", {"topic": "t"}), ("write_cheatsheet", {"topic": "t"}), ("weekly_content_drop", {}),
             ("amplify_post", {"post": "x"}), ("analyze_competitor", {"competitor_urls": "https://linkedin.com/company/a"}), ("find_prospects", {}),
             ("first_post_coach", {}), ("setup_marketing_employee", {}), ("build_voice_profile", {}), ("write_newsletter", {"topic": "t"})]
    for tool, args in calls:
        out = maya.call(tool, **args)
        m = leak.search(out)
        assert not m, (tool, m.group(0), out[max(0, m.start() - 80): m.end() + 80])
