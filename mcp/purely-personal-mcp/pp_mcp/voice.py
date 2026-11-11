"""Voice rules, AI-tell detection, mechanical clean-up and platform polish.

Everything in here is deterministic. The universal rules come from the
Purely Personal AI Pattern Blacklist; the participant's own banned list
(from their Voice DNA / Business Brain) is layered on top at call time.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# ----------------------------------------------------------------------------
# Universal rules (AI Pattern Blacklist, Purely Personal skill suite)
# ----------------------------------------------------------------------------

# Stems: matched as \bstem\w*
BANNED_STEMS = [
    "leverag", "unlock", "delv", "synerg", "game-chang", "game chang", "cutting-edge",
    "cutting edge", "robust", "scalab", "seamless", "holistic", "actionable",
    "impactful", "transformative", "innovative", "empower", "elevat", "cultivat",
    "harness", "spearhead", "pivotal", "paradigm", "ecosystem", "bandwidth",
    "granular", "supercharg", "revolutioniz", "revolutionis", "tapestry", "unleash",
    "streamlin", "optimiz", "optimis", "utiliz", "utilis", "ideat", "navigat",
]
# Whole phrases (substring, case-insensitive)
BANNED_PHRASES = [
    "circle back", "move the needle", "at the end of the day", "boils down to",
    "the bottom line is", "it goes without saying", "it's important to note",
    "it is important to note", "needless to say", "the fact of the matter",
    "dive deep", "dive into", "deep dive", "in today's fast-paced", "in today's digital age",
    "in today's rapidly changing", "now more than ever", "it's no secret that",
    "we all know that", "you've probably heard", "i'm excited to share",
    "let me be honest", "here's the thing", "here's the truth", "what if i told you",
    "let me tell you something", "i've been thinking a lot about",
    "here's what most people get wrong", "it's not just about", "let's be honest",
    "this resonates deeply", "such a powerful insight", "exactly what i needed to hear",
]
BANNED_TRANSITIONS = [
    "moreover", "furthermore", "in addition to this", "it's worth noting that",
    "having said that", "with that in mind", "on the other hand", "last but not least",
    "at the same time", "that being said",
]
BANNED_CLOSINGS = [
    "thoughts?", "what do you think?", "drop a comment below", "feel free to reach out",
    "hope this helps", "thanks for reading", "if this resonated with you",
    "save this for later", "share this with someone who needs it",
    "what would you add to this list?", "tag someone who needs to hear this",
    "the journey starts now", "your future self will thank you", "the time to act is now",
]
MORAL_OPENERS = ("the lesson", "the takeaway", "the moral", "remember:", "key takeaway", "moral of the story")

# Plain-word swaps used by the mechanical clean-up. Anything not here is flagged only.
SWAPS = {
    "leverage": "use", "leveraging": "using", "leveraged": "used", "utilize": "use",
    "utilise": "use", "utilizing": "using", "unlock": "open up", "unlocking": "opening up",
    "delve into": "look at", "delve": "dig", "seamless": "smooth", "seamlessly": "smoothly",
    "empower": "help", "empowers": "helps", "empowering": "helping", "elevate": "raise",
    "elevates": "raises", "streamline": "simplify", "optimize": "improve", "optimise": "improve",
    "game-changer": "big shift", "game-changing": "big", "cutting-edge": "new",
    "robust": "solid", "holistic": "whole", "actionable": "usable", "impactful": "strong",
    "transformative": "big", "innovative": "new", "supercharge": "speed up",
    "harness": "use", "tapestry": "mix", "ecosystem": "setup", "paradigm": "model",
    "navigate": "work through", "dive deep into": "look closely at", "dive into": "look at",
}

_STRUCT = [
    ("contrast-frame", re.compile(r"\bnot (?:because|about|just|only)\b[^.\n!?]{0,90}?[,;]?\s*\b(?:but|it'?s|it is)\b", re.I),
     "Contrast frame ('not X, but Y'). State the real point directly."),
    ("contrast-frame", re.compile(r"\b(?:it'?s|it is|this is|that'?s) not\b[^.\n!?]{1,80}?[,;]\s*(?:it'?s|it is|this is|that'?s)\b", re.I),
     "Contrast frame ('it's not X, it's Y'). Rewrite as one plain statement."),
    ("contrast-frame", re.compile(r"\bless [a-z' ]{1,30}, more [a-z' ]{1,30}", re.I),
     "'Less X, more Y' frame. Say the specific thing."),
    ("contrast-frame", re.compile(r"\b(?:it'?s|it is|this is|that'?s) not\b[^.\n!?]{1,60}[.]\s+(?:it'?s|it is|this is|that'?s)\b", re.I),
     "Contrast frame split over two sentences ('It's not X. It's Y.'). Say the real point once."),
    ("negative-stack", re.compile(r"(?:^|[.!?]\s+)No [a-z' ]{2,24}\.\s+No [a-z' ]{2,24}\.", re.I | re.M),
     "Negative stack ('No X. No Y.'). Cut to the one that matters."),
]


@dataclass
class Tell:
    kind: str
    line: int
    match: str
    advice: str

    def render(self) -> str:
        return f"L{self.line} [{self.kind}] \"{self.match}\" -> {self.advice}"


def _norm(s: str) -> str:
    return (s or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def _clean_term(t: str) -> str:
    return _norm(t).strip().strip("`*_\"' ").lower()


def user_terms(banned: list[str] | None) -> tuple[list[str], list[str]]:
    """Split a participant's banned list into (words, phrases)."""
    words, phrases = [], []
    for raw in banned or []:
        t = _clean_term(raw)
        if not t or len(t) > 70:
            continue
        (phrases if (" " in t or "-" in t or "'" in t) else words).append(t)
    return words, phrases


def find_tells(text: str, extra_banned: list[str] | None = None) -> list[Tell]:
    """Every AI tell and banned item in the text, with line numbers."""
    text = _norm(text)
    tells: list[Tell] = []
    lines = text.split("\n")
    xwords, xphrases = user_terms(extra_banned)

    for i, line in enumerate(lines, 1):
        low = line.lower()
        if "—" in line:
            tells.append(Tell("em-dash", i, "—", "Em dash. Replace with a period or comma."))
        for m in re.finditer(r"\s–\s", line):
            tells.append(Tell("em-dash", i, "–", "Spaced en dash used as a dash. Use a period or comma."))
        for stem in BANNED_STEMS:
            for m in re.finditer(r"\b" + re.escape(stem) + r"\w*", low):
                tells.append(Tell("banned-word", i, line[m.start():m.end()], "Corporate/AI filler. Use the plain word."))
        for ph in BANNED_PHRASES:
            if ph in low:
                tells.append(Tell("banned-phrase", i, ph, "AI-pattern phrase. Cut or say it plainly."))
        for tr in BANNED_TRANSITIONS:
            if re.search(r"(?:^|[.!?]\s+|\n)" + re.escape(tr) + r"\b", low) or low.startswith(tr):
                tells.append(Tell("banned-transition", i, tr, "Filler bridge. Use a hard stop instead."))
        stripped = low.strip()
        for cl in BANNED_CLOSINGS:
            if stripped == cl or stripped.endswith(cl):
                tells.append(Tell("banned-closing", i, cl, "Generic closer. End on a specific line."))
        if stripped.startswith(MORAL_OPENERS):
            tells.append(Tell("tidy-moral", i, stripped[:30], "Stated moral. Let the story carry the lesson."))
        for w in xwords:
            for m in re.finditer(r"\b" + re.escape(w) + r"\w*", low):
                tells.append(Tell("your-banned-word", i, line[m.start():m.end()], "On YOUR never-use list."))
        for p in xphrases:
            if p in low:
                tells.append(Tell("your-banned-phrase", i, p, "On YOUR never-use list."))

    flat = text
    for kind, rx, advice in _STRUCT:
        for m in rx.finditer(flat):
            ln = flat.count("\n", 0, m.start()) + 1
            tells.append(Tell(kind, ln, m.group(0).strip()[:80], advice))

    # Rhetorical question as the opening line
    first = next(((i, l) for i, l in enumerate(lines, 1) if l.strip()), None)
    if first and first[1].strip().endswith("?"):
        tells.append(Tell("question-opener", first[0], first[1].strip()[:80],
                          "Opens on a question. Open on the position or the moment."))

    # Triple staccato: three or more consecutive tiny single-line paragraphs
    paras = [(i, l.strip()) for i, l in enumerate(lines, 1)]
    run: list[tuple[int, str]] = []
    for i, l in paras + [(len(lines) + 1, "")]:
        if l and len(l.split()) <= 5 and not l.startswith(("-", "*", "•")) and not re.match(r"^\d+[.)]", l):
            run.append((i, l))
        else:
            if len(run) >= 3:
                tells.append(Tell("staccato-run", run[0][0], " / ".join(r[1] for r in run[:3]),
                                  "Three+ tiny lines stacked for drama. Merge or vary the rhythm."))
            run = []

    # de-duplicate on (line, match); prefer the participant's own rule over the universal one
    seen, out = set(), []
    for t in sorted(tells, key=lambda t: (not t.kind.startswith("your-"),)):
        k = (t.line, t.match.lower()) if t.kind in ("banned-word", "banned-phrase", "your-banned-word", "your-banned-phrase") else (t.kind, t.line, t.match.lower())
        if k not in seen:
            seen.add(k)
            out.append(t)
    return sorted(out, key=lambda t: (t.line, t.kind))


def _match_case(src: str, repl: str) -> str:
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[:1].isupper():
        return repl[:1].upper() + repl[1:]
    return repl


def mechanical_clean(text: str, extra_banned: list[str] | None = None) -> tuple[str, list[str]]:
    """Deterministic clean-up. Returns (new_text, change_log). Never invents content."""
    changes: list[str] = []
    t = _norm(text)

    # 1. Em dashes -> period (new sentence) or comma for short asides
    def dash(m: re.Match) -> str:
        before, after = m.group(1), m.group(2)
        changes.append("em dash replaced")
        if len(before.split()) < 3:
            return before + ", " + after
        return before + ". " + after[:1].upper() + after[1:]

    t = re.sub(r"([^\s—][^\n—]*?)\s*—\s*([^\n]+?)(?=—|\n|$)", dash, t) if "—" in t else t
    t = t.replace("—", ", ") if "—" in t else t
    t = re.sub(r"\s–\s", ". ", t)

    # 2. Plain-word swaps (longest key first)
    for key in sorted(SWAPS, key=len, reverse=True):
        rx = re.compile(r"\b" + re.escape(key) + r"\b", re.I)
        if rx.search(t):
            t = rx.sub(lambda m: _match_case(m.group(0), SWAPS[key]), t)
            changes.append(f"'{key}' -> '{SWAPS[key]}'")

    # 3. Strip leading banned transitions
    for tr in BANNED_TRANSITIONS:
        rx = re.compile(r"(^|[.!?]\s+|\n)" + re.escape(tr) + r",?\s+([a-z])", re.I)
        if rx.search(t):
            t = rx.sub(lambda m: m.group(1) + m.group(2).upper(), t)
            changes.append(f"transition '{tr}' removed")

    # 4. Drop lines that are only a banned closing
    kept = []
    for line in t.split("\n"):
        if _clean_term(line) in BANNED_CLOSINGS:
            changes.append(f"closing '{line.strip()}' removed")
            continue
        kept.append(line)
    t = "\n".join(kept)

    # 5. Whitespace hygiene
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t, changes


# ----------------------------------------------------------------------------
# Platform polish
# ----------------------------------------------------------------------------

PLATFORMS = {
    # name: (target_min, target_max, hard_cap, hook_window)
    "linkedin": (1300, 1500, 3000, 210),
    "instagram": (1500, 2200, 2200, 125),
    "x": (180, 280, 280, 140),
    "threads": (150, 500, 500, 140),
    "facebook": (400, 1200, 63206, 125),
    "newsletter": (900, 6000, 20000, 90),
}


def _kw_cta(text: str) -> bool:
    tail = "\n".join([l for l in text.strip().split("\n") if l.strip()][-3:])
    return bool(re.search(r"\b(?:dm|message|comment|reply)\b[^\n]{0,30}?[\"'“”‘’]?\b[A-Z][A-Z0-9]{2,}\b", tail)
                or re.search(r"\b(?:dm|comment|reply)\s+(?:me\s+)?[\"“']([^\"”']{2,20})[\"”']", tail, re.I))


def polish(text: str, platform: str = "linkedin", extra_banned: list[str] | None = None) -> dict:
    platform = (platform or "linkedin").lower().replace("twitter", "x")
    lo, hi, cap, hook_win = PLATFORMS.get(platform, PLATFORMS["linkedin"])
    cleaned, changes = mechanical_clean(text, extra_banned)
    n = len(cleaned)
    issues: list[str] = []

    first_line = next((l for l in cleaned.split("\n") if l.strip()), "")
    if len(first_line) > hook_win:
        issues.append(f"Hook line is {len(first_line)} chars; the fold is about {hook_win}. Tighten the first line.")
    if len(first_line.split()) < 4:
        issues.append("Hook line is under 4 words. Give it enough substance to stop the scroll.")

    if n < lo:
        issues.append(f"{n} chars is under the {platform} target ({lo}-{hi}). Add a concrete detail, not filler.")
    if n > hi and platform != "newsletter":
        issues.append(f"{n} chars is over the {platform} target ({lo}-{hi}). Cut the weakest paragraph.")
    if n > cap:
        issues.append(f"{n} chars exceeds the hard limit ({cap}).")

    paras = [p for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
    for idx, p in enumerate(paras, 1):
        sents = len(re.findall(r"[.!?](?:\s|$)", p))
        if (sents > 4 or len(p) > 420) and not re.match(r"^\s*(?:[-*•]|\d+[.)])", p):
            issues.append(f"Paragraph {idx} runs {sents} sentences / {len(p)} chars. Break it up for mobile.")
    if len(paras) < 3 and n > 500 and platform in ("linkedin", "instagram", "facebook", "threads"):
        issues.append("Fewer than 3 paragraphs. Add white space between ideas.")

    tags = re.findall(r"(?<!\w)#\w+", cleaned)
    if platform == "x" and tags:
        issues.append("Hashtags on X are deprioritised. Remove them.")
    if platform == "linkedin" and len(tags) > 3:
        issues.append(f"{len(tags)} hashtags. Keep it to 3 or fewer on LinkedIn.")
    if platform == "instagram" and tags and not (9 <= len(tags) <= 12):
        issues.append(f"{len(tags)} hashtags. Aim for 9-12 on Instagram, placed after a separator line.")

    last = [l for l in cleaned.split("\n") if l.strip()][-1:] or [""]
    has_kw = _kw_cta(cleaned)
    ends_q = last[0].strip().endswith("?")
    if not (has_kw or ends_q) and platform in ("linkedin", "instagram", "threads", "facebook"):
        issues.append("No ask at the end. Add a keyword DM invitation or a specific question.")

    tells = find_tells(cleaned, extra_banned)
    return {
        "platform": platform, "chars": n, "target": f"{lo}-{hi}", "polished": cleaned,
        "mechanical_changes": changes, "structure_issues": issues,
        "remaining_tells": [t.render() for t in tells], "has_keyword_cta": has_kw, "ends_on_question": ends_q,
    }
