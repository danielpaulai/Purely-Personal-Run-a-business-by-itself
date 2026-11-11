"""The Invisibility Diagnostic (0-4): Voice, POV, Specificity, Asking.

Implements the invisibility-diagnostic skill as code so scoring is repeatable.
The Voice test is personalised: it checks the post against the participant's
own word bank, signature phrases and customer phrases, and against the AI
pattern blacklist. A heuristic cannot hear that a sentence is not yours; the
`needs_human_read` note says so.
"""
from __future__ import annotations

import re

from .voice import find_tells

TIERS = {0: "Invisible", 1: "Invisible", 2: "Background noise", 3: "Visible", 4: "Magnetic"}
TIER_ACTION = {
    "Invisible": "Do not publish. Fix every missing dimension first.",
    "Background noise": "One-line edit away from visible. Fix the missing dimensions.",
    "Visible": "Publishable. One more fix makes it magnetic.",
    "Magnetic": "Ship it.",
}

_STANCE = re.compile(
    r"\b(wrong|myth|stop|never|always|overrated|underrated|lie|lies|broken|dead|mistake|"
    r"unpopular|disagree|hot take|nobody|everyone|truth|actually|instead|refuse|don'?t|"
    r"should(?:n'?t)?|bad advice|scam|waste|ignore|quit|kill|nobody tells|the real reason)\b",
    re.I,
)
_EXPLAINERS = re.compile(r"^(?:here are|here's a guide|a guide to|tips for|ways to|\d+ (?:tips|ways|things))", re.I)
_NUM = re.compile(r"(?:\$|£|€)?\d[\d,.]*\s?(?:%|k|m|x|hours?|hrs?|days?|weeks?|months?|years?|clients?|people|calls?|dms?|posts?)?", re.I)
_NAME = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b")


def _split_halves(text: str) -> tuple[str, str]:
    t = text.strip()
    mid = len(t) // 2
    return t[:mid], t[mid:]


def _tail_lines(text: str, n: int = 2) -> str:
    lines = [l for l in text.strip().split("\n") if l.strip()]
    return "\n".join(lines[-n:])


def _asking(text: str, strict: bool) -> tuple[bool, str]:
    tail = _tail_lines(text, 2)
    kw = re.search(r"\b(?:dm|message|comment|reply|type)\b[^\n]{0,40}?[\"'“”‘’]([^\"'“”‘’\n]{2,24})[\"'“”‘’]", tail, re.I) or \
        re.search(r"\b(?:dm|message|comment|reply|type)\s+(?:me\s+)?([A-Z][A-Z0-9]{2,})\b", tail)
    if kw:
        return True, f"keyword invitation ('{kw.group(1)}')"
    if not strict and tail.strip().endswith("?") and len(tail.split()) >= 6:
        return True, "closing question to the reader (accepted unless strict=true)"
    return False, "no keyword DM/comment invitation in the last 2 lines" + ("" if strict else " and no direct closing question")


def diagnose(text: str, profile=None, strict_asking: bool = False) -> dict:
    t = (text or "").strip()
    if not t:
        return {"score": 0, "tier": "Invisible", "dimensions": {}, "fixes": ["Nothing to score."], "chars": 0}

    first, second = _split_halves(t)
    banned = profile.voice["banned"] if profile else []
    tells = find_tells(t, banned)
    hard_tells = [x for x in tells if x.kind not in ("staccato-run",)]

    # ---- Voice -----------------------------------------------------------
    own: list[str] = []
    if profile:
        bank = [w.lower() for w in profile.voice["word_bank"]]
        sig = [w.lower() for w in profile.voice["signature_phrases"]]
        cust = [w.lower() for w in profile.customer["their_words"]]
        low = t.lower()
        hit = {x for x in bank + sig + cust if len(x) > 2 and re.search(r"\b" + re.escape(x) + r"\b", low)}
        own = sorted(x for x in hit if not any(x != y and x in y for y in hit))  # drop items contained in a longer hit
    first_person = bool(re.search(r"\b(i|i'm|i've|my|we|our)\b", t, re.I))
    if profile and (profile.voice["word_bank"] or profile.voice["signature_phrases"]):
        voice_ok = len(own) >= 2 and len(hard_tells) <= 1
        voice_why = (f"uses {len(own)} of your own words/phrases ({', '.join(own[:4])})" if voice_ok else
                     f"only {len(own)} of your own words/phrases found" + (f", {len(hard_tells)} AI tells" if hard_tells else ""))
    else:
        voice_ok = first_person and len(hard_tells) == 0
        voice_why = ("first-person and clean of AI tells (no Voice DNA loaded, so this is a weak proxy)" if voice_ok else
                     "no personal markers or AI tells present (load your Voice DNA for a real voice check)")

    # ---- POV -------------------------------------------------------------
    stance_hits = _STANCE.findall(first[:600] + " " + second[:300])
    pov_ok = len(stance_hits) >= 2 and not _EXPLAINERS.match(t)
    pov_why = ("takes a side (" + ", ".join(sorted({s.lower() for s in stance_hits})[:4]) + ")" if pov_ok else
               "reads as explanation: no clear side taken in the opening")

    # ---- Specificity -----------------------------------------------------
    has_num = bool(_NUM.search(first)) and bool(re.search(r"\d", first))
    names = [n for n in _NAME.findall(first) if n not in ("The", "This", "That", "When", "What", "Most", "Last", "And", "But", "Then", "Here", "Not", "Why", "How")]
    spec_ok = has_num and (len(names) >= 1 or bool(re.search(r"\b(client|customer|founder|coach|member)\b", first, re.I)))
    spec_why = ("number and a real person/entity in the first half" if spec_ok else
                ("a number but no named person/entity" if has_num else "no real number" if not names else "a name but no number") + " in the first half")

    # ---- Asking ----------------------------------------------------------
    ask_ok, ask_why = _asking(t, strict_asking)

    dims = {
        "Voice": (voice_ok, voice_why), "POV": (pov_ok, pov_why),
        "Specificity": (spec_ok, spec_why), "Asking": (ask_ok, ask_why),
    }
    score = sum(1 for ok, _ in dims.values() if ok)
    tier = TIERS[score]

    kw_suggest = (profile.voice["signature_phrases"][0].split()[0].upper() if profile and profile.voice["signature_phrases"] else "PLAYBOOK")
    kw_suggest = re.sub(r"[^A-Z0-9]", "", kw_suggest)[:12] or "PLAYBOOK"
    fix_lines = {
        "Voice": "Swap two generic lines for phrases only you say" + (f" (e.g. {', '.join(profile.voice['signature_phrases'][:2])})" if profile and profile.voice["signature_phrases"] else " (load your Voice DNA)") + "; delete the AI tells listed below.",
        "POV": "Open with the position you hold that someone in your industry would argue with, in the first line.",
        "Specificity": "Add one real name and one real number (from your Business Brain, never invented) in the first half.",
        "Asking": f"Close with a direct invitation, e.g. 'DM me \"{kw_suggest}\" and I'll send it.'",
    }
    fixes = [f"{d}: {fix_lines[d]}" for d, (ok, _) in dims.items() if not ok]

    return {
        "score": score, "tier": tier, "action": TIER_ACTION[tier], "chars": len(t),
        "dimensions": {d: {"point": int(ok), "why": why} for d, (ok, why) in dims.items()},
        "fixes": fixes,
        "ai_tells": [x.render() for x in tells[:25]],
        "needs_human_read": "A score cannot hear that a sentence is not yours. Read it aloud and change any line you would not say.",
    }


def render(result: dict, mode: str = "score-with-fix") -> str:
    if not result.get("dimensions"):
        return "Nothing to score."
    lines = [f"INVISIBILITY DIAGNOSTIC: {result['score']}/4 · {result['tier']} · {result['chars']} chars"]
    if mode == "score-only":
        return lines[0]
    lines.append(result["action"])
    lines.append("")
    for d, v in result["dimensions"].items():
        lines.append(f"  {'✓' if v['point'] else '✗'} {d}: {v['why']}")
    if result["fixes"]:
        lines += ["", "ONE-LINE FIXES (additive, do not rewrite the post):"] + [f"  - {f}" for f in result["fixes"]]
    if result["ai_tells"]:
        lines += ["", "AI TELLS FOUND:"] + [f"  - {x}" for x in result["ai_tells"]]
    lines += ["", result["needs_human_read"]]
    return "\n".join(lines)
