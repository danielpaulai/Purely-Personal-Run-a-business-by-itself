"""The 12 program skills, bundled, and the work-order compiler.

Each content tool in this server does the same thing: it takes one of the
twelve skills from the Build Your 1st AI Employee program, locks it to the
participant's Business Brain, ICP and Voice DNA, and returns a WORK ORDER
the calling Claude executes. The deterministic parts (scoring, polish,
de-AI, history, reports) run in code. Nothing here calls a model.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from .profile import Profile

DATA = Path(__file__).parent / "data"
SKILLS_DIR = DATA / "skills"

SKILL_NAMES = [
    "ai-marketing-employee", "voice-profile-builder", "linkedin-post-writer", "first-post-coach",
    "invisibility-diagnostic", "linkedin-carousel-builder", "linkedin-cheatsheet-builder",
    "competitor-x-ray", "prospect-magnet", "multi-platform-amplifier", "weekly-content-engine",
    "homework-reviewer",
]


@lru_cache(maxsize=None)
def skill_md(name: str) -> str:
    p = SKILLS_DIR / name / "SKILL.md"
    if not p.exists():
        raise KeyError(f"Unknown skill '{name}'. Known: {', '.join(SKILL_NAMES)}")
    return p.read_text()


@lru_cache(maxsize=None)
def prompt_file(name: str, file: str) -> str:
    p = SKILLS_DIR / name / "prompts" / file
    return p.read_text() if p.exists() else ""


def prompt_files(name: str) -> list[str]:
    d = SKILLS_DIR / name / "prompts"
    return sorted(x.name for x in d.glob("*.md")) if d.exists() else []


def frontmatter(name: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", skill_md(name), re.S)
    out = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
    return out


def skill_sections(name: str, *titles: str) -> str:
    """Pull '## Title' sections (case-insensitive prefix match) out of a SKILL.md."""
    md = skill_md(name)
    parts = re.split(r"(?m)^(?=## )", md)
    out = []
    for p in parts:
        head = p.split("\n", 1)[0].lstrip("# ").strip().lower()
        if any(head.startswith(t.lower()) for t in titles):
            out.append(p.strip())
    return "\n\n".join(out)


def catalogue() -> list[dict]:
    rows = []
    for n in SKILL_NAMES:
        fm = frontmatter(n)
        rows.append({"name": n, "version": fm.get("version", ""), "description": fm.get("description", ""),
                     "prompts": prompt_files(n)})
    return rows


# ----------------------------------------------------------------------------
# Work-order assembly
# ----------------------------------------------------------------------------
NEEDS_SETUP = """\
PURELY PERSONAL: I need YOUR documents before I can write in your voice.

This connector stores nothing and never falls back to anyone else's voice. You pass your own
Business Brain with each call (it already sits in your Claude Project knowledge).

Claude: read BUSINESS-BRAIN.md from the project knowledge and call this tool again with its FULL text in
`brain`. If ICP.md and VOICE-DNA.md are also there, pass them in `icp` and `voice_dna` (richer voice checks).
Do not shorten or paraphrase them. If there is no Business Brain yet, tell the user to build it first
(Day 1: ICP, then Voice DNA, then Business Brain) and stop.

Use check_my_brain(brain=...) to see how complete the documents are."""


def depersonalize(text: str) -> str:
    """Skills were authored with the creator's name in examples and as a default voice. A participant's
    order must never carry that: it would invite the model to fall back to someone else's voice."""
    lines = [l for l in text.split("\n") if "/references/" not in l and "bundled references" not in l.lower()]
    t = "\n".join(lines)
    t = re.sub(r"@danielpaulai\b", "@[operator handle]", t)
    t = re.sub(r"Daniel Paul(?:'s)?(?: · AI Trainer)?", lambda m: "the operator's" if m.group(0).endswith("'s") else "the operator", t)
    t = re.sub(r"Daniel's", "the operator's", t)
    t = re.sub(r"\bDaniel\b", "the operator", t)
    t = re.sub(r"\bDanny\b", "the operator", t)
    return t


def _box(title: str, body: str) -> str:
    return f"\n## {title}\n{body.strip()}\n"


def lock_blocks(p: Profile, depth: str = "standard") -> str:
    v, c = p.voice, p.customer
    parts = []
    who = [f"Operator: {p.name or '(name not set)'}", f"Publishing language: {p.language or 'English'}",
           f"Primary platform: {p.platform or 'linkedin'}"]
    if p.handle:
        who.append(f"Handle: {p.handle}")
    parts.append(_box("1. WHO THIS IS FOR", "\n".join(who)))

    if p.brain:
        if depth == "full":
            parts.append(_box("2. THE BUSINESS BRAIN (source of truth; it wins any disagreement)", p.brain))
        else:
            parts.append(_box("2. THE BUSINESS BRAIN", "The Business Brain is the full text you passed in `brain=` on this call. It is the source of truth and wins any "
                                                       "disagreement with the ICP or Voice DNA. Everything below was read from it; re-read it before writing."))
    elif p.icp or p.voice_dna:
        parts.append(_box("2. THE BUSINESS BRAIN", "No combined Brain saved. Use the ICP and Voice DNA below as the Brain."))

    voice_lines = []
    if v["word_bank"]:
        voice_lines.append("Word bank (these must appear naturally): " + ", ".join(v["word_bank"][:30]))
    if v["signature_phrases"]:
        voice_lines.append("Signature phrases (use one or two, never forced): " + " | ".join(v["signature_phrases"][:10]))
    if v["rules"]:
        voice_lines.append("Personal writing rules:\n" + "\n".join(f"  {i}. {r}" for i, r in enumerate(v["rules"][:8], 1)))
    if v["rhythm"]:
        voice_lines.append("Sentence rhythm: " + re.sub(r"\s+", " ", v["rhythm"])[:400])
    if v["test_line"]:
        voice_lines.append("THE TEST (every piece must pass it): " + v["test_line"])
    if not voice_lines:
        voice_lines.append("(No parsed voice markers; infer voice from the documents below and say what you assumed.)")
    parts.append(_box("3. VOICE LOCK (from your Voice DNA)", "\n".join(voice_lines)))

    cust = []
    if c["persona"]:
        cust.append("The one person: " + re.sub(r"\s+", " ", c["persona"])[:700])
    if c["their_words"]:
        cust.append("Phrases they actually use (hooks come from these):\n" + "\n".join(f"  - {x}" for x in c["their_words"][:12]))
    if c["objections"]:
        cust.append("Why they say no:\n" + "\n".join(f"  - {x}" for x in c["objections"][:6]))
    if c["themes"]:
        cust.append("Themes to own: " + "; ".join(c["themes"][:6]))
    if not cust:
        cust.append("(No parsed customer markers; take the customer from the ICP/Brain below.)")
    parts.append(_box("4. CUSTOMER LOCK (from your ICP)", "\n".join(cust)))

    if depth == "full":
        if p.icp:
            parts.append(_box("4b. FULL ICP DOCUMENT", p.icp))
        if p.voice_dna:
            parts.append(_box("3b. FULL VOICE DNA DOCUMENT", p.voice_dna))

    banned = v["banned"]
    rules = [
        "No em dashes. No en-dash-as-dash. Use a period or a comma.",
        "Never invent a client, result, number, date, testimonial or quote. Use only what is in the Brain or in this request. If something is missing, write around it; never put a placeholder in square brackets.",
        "Banned (yours): " + (", ".join(banned[:40]) if banned else "none parsed; apply the universal AI Pattern Blacklist"),
        "Universal blacklist always applies: no contrast frames ('not X, but Y'), no negative stacks, no rhetorical-question openers, no tidy moral at the end, no 'Moreover/Furthermore', no corporate filler (leverage, unlock, delve, seamless...).",
        "If the Brain, ICP and Voice DNA disagree: the Brain wins; say so in one line.",
    ]
    if p.guard_rails:
        rules.insert(1, "NEVER CLAIM (hard guard rails from the operator's own documents):\n  " + "\n  ".join(f"- {g}" for g in p.guard_rails))
    parts.append(_box("5. HARD RULES", "\n".join(f"- {r}" for r in rules)))
    return "".join(parts)


def work_order(
    *, title: str, skill: str, p: Profile, method: str, inputs: dict, task: str, contract: str,
    checks: list[str] | None = None, depth: str = "standard",
) -> str:
    fm = frontmatter(skill)
    head = (
        f"# WORK ORDER: {title}\n"
        f"Skill: {skill} v{fm.get('version', '1.0.0')} · Purely Personal program skill\n"
        "You are the operator's AI employee. Execute this order now. Do not summarise it, do not "
        "narrate it, do not ask questions unless a required input below is truly missing. "
        "Deliver exactly the OUTPUT CONTRACT."
    )
    body = lock_blocks(p, depth)
    body += _box(f"6. SKILL METHOD ({skill})", depersonalize(method))
    body += _box("7. INPUTS FOR THIS RUN", "\n".join(f"- {k}: {v}" for k, v in inputs.items() if v not in (None, "", [])))
    body += _box("8. TASK", task)
    body += _box("9. OUTPUT CONTRACT", contract)
    same = "brain=/icp=/voice_dna=<the same documents you passed above>"
    chk = list(checks) if checks is not None else [
        f"Call score_post(text=<draft>, {same}). Anything under 4/4: add the missing element, re-score. Max 2 rounds.",
        f"Call polish_post(text=<draft>, platform=<platform>, {same}).",
        f"Call de_ai_ify(text=<draft>, {same}), then read it once as the operator and cut any sentence they would not say aloud.",
    ]
    if checks is not None and not any("de_ai_ify" in c for c in chk):
        chk.append(f"Call de_ai_ify(text=<anything you will publish or send>, {same}).")
    body += _box("10. BEFORE YOU DELIVER", "\n".join(f"{i}. {c}" for i, c in enumerate(chk, 1)))
    return head + "\n" + body
