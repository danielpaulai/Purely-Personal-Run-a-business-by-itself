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


# ----------------------------------------------------------------------------
# German (DACH) rules. Used when the text is German: English lists must never touch German prose.
# ----------------------------------------------------------------------------
DE_BANNED_STEMS = [
    "ganzheitlich", "nahtlos", "synerg", "game-changer", "gamechanger", "revolutionär", "wegweisend", "zukunftsweisend",
    "bahnbrechend", "maßgeschneidert", "massgeschneidert", "rundum-sorglos", "state-of-the-art", "cutting-edge", "disruptiv",
    "skalierbar", "impactvoll", "innovationsgetrieben", "lösungsorientiert", "kundenzentriert",
]
DE_BANNED_PHRASES = [
    "in der heutigen schnelllebigen", "in der heutigen digitalen", "in der heutigen dynamischen", "in der heutigen zeit",
    "es ist kein geheimnis", "haben sie sich jemals gefragt", "tauchen sie ein", "lassen sie uns eintauchen",
    "zusammenfassend lässt sich sagen", "es ist wichtig zu beachten", "es ist wichtig zu betonen", "am ende des tages",
    "auf das nächste level", "potenziale heben", "potenziale ausschöpfen", "potenziale entfesseln", "next level",
    "ein game-changer", "den nagel auf den kopf", "in einer welt, in der", "stellen sie sich vor",
    "lassen sie uns darüber sprechen", "ich freue mich auf den austausch",
]
DE_TRANSITIONS = ["darüber hinaus", "des weiteren", "nichtsdestotrotz", "letztendlich", "abschließend", "zusammenfassend", "ferner"]
DE_CLOSINGS = ["was denken sie?", "was meinen sie?", "teilen sie ihre gedanken", "hinterlassen sie einen kommentar",
               "vielen dank fürs lesen", "ich hoffe, das hilft", "ich hoffe, das hilft ihnen weiter", "folgen sie mir für mehr"]
DE_MORAL = ("fazit:", "die lektion", "die moral", "merke:", "take-away", "takeaway")
DE_SWAPS = [  # (regex, replacement with \1 = inflection ending)
    (r"\binnovativ(e|en|er|es|em)?\b", "neu"), (r"\bnahtlos(e|en|er|es|em)?\b", "reibungslos"),
    (r"\bganzheitlich(e|en|er|es|em)?\b", "umfassend"), (r"\bzukunftsweisend(e|en|er|es|em)?\b", "neu"),
]
_DE_STRUCT = [
    ("contrast-frame", re.compile(r"\bnicht nur\b[^.\n!?]{1,80}?,?\s*sondern\b", re.I),
     "Gegensatz-Schema ('nicht nur X, sondern auch Y'). Sag direkt, was zählt."),
    ("contrast-frame", re.compile(r"\bes geht (?:nicht|nicht mehr) (?:um|darum)\b[^.\n!?]{1,80}?[,;.]\s*(?:es geht|sondern)", re.I),
     "Gegensatz-Schema ('es geht nicht um X, sondern um Y'). Einmal klar sagen."),
    ("contrast-frame", re.compile(r"\b(?:das ist|dies ist|es ist) kein\w*\b[^.\n!?]{1,60}[.,;]\s*(?:das ist|dies ist|es ist)\b", re.I),
     "Gegensatz-Schema ('das ist kein X, das ist Y'). Einmal klar sagen."),
    ("contrast-frame", re.compile(r"\bweniger\b [^.,\n]{1,30}, mehr\b", re.I), "'Weniger X, mehr Y'-Schema. Das Konkrete nennen."),
]

_DE_WORDS = set("""der die das und ist nicht mit für ein eine wir ich sie zu auf den dem von bei auch sich werden haben wenn aber oder
als wie im um es nach mehr sind wird kann können muss noch nur schon dass wo was wer warum immer jede jeden zum zur beim vom
unsere unser ihre ihr mein meine dann durch über unter ohne bis gegen""".split())
_EN_WORDS = set("""the and is of to in that for with you are it this was we our your they have has not but or as be at by on from can will
what when how why more about""".split())


def detect_language(text: str) -> str:
    """'de' or 'en'. German wins only on clear evidence, so English text never loses its English rules."""
    toks = re.findall(r"[A-Za-zÄÖÜäöüß']+", (text or "").lower())
    if not toks:
        return "en"
    de = sum(1 for t in toks if t in _DE_WORDS)
    en = sum(1 for t in toks if t in _EN_WORDS)
    umlauts = len(re.findall(r"[äöüß]", (text or "").lower()))
    return "de" if (de >= 3 and de > en) or (de >= 2 and de > en and umlauts >= 2) else "en"


def resolve_lang(text: str, lang: str = "") -> str:
    l = (lang or "").lower()[:2]
    if l in ("de", "en"):
        return l
    return detect_language(text)


def _stem(word: str) -> str:
    """Light German/English stem for matching inflected forms of the participant's own words."""
    w = word.lower().strip()
    for suf in ("sten", "ster", "stes", "stem", "ste", "en", "er", "es", "em", "e", "n", "s", "t"):
        if len(w) >= 5 and w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def _user_regex(term: str) -> re.Pattern:
    """A banned word or phrase -> a regex that also catches inflections ('Potenziale heben' ~ 'Potenzial hebt',
    'Potenziale gehoben'), up to two filler words inside a phrase, and the reversed word order ('hebt Potenziale')."""
    words = [w for w in re.split(r"[\s]+", _clean_term(term)) if w]
    if len(words) == 1:
        return re.compile(r"\b" + re.escape(_stem(words[0])) + r"\w*", re.I)
    glue = r"\W+(?:\w+\W+){0,2}?"

    def part(w: str) -> str:
        return r"\b(?:ge|be|ver|er|ent|zer)?" + re.escape(_stem(w)) + r"\w*"

    fwd = glue.join(part(w) for w in words)
    rev = glue.join(part(w) for w in reversed(words)) if len(words) == 2 else None
    return re.compile(fwd if not rev else f"(?:{fwd})|(?:{rev})", re.I)


def user_terms(banned: list[str] | None) -> tuple[list[str], list[str]]:
    """Split a participant's banned list into (words, phrases)."""
    words, phrases = [], []
    for raw in banned or []:
        t = _clean_term(raw)
        if not t or len(t) > 70:
            continue
        (phrases if (" " in t or "-" in t or "'" in t) else words).append(t)
    return words, phrases


def find_tells(text: str, extra_banned: list[str] | None = None, lang: str = "") -> list[Tell]:
    """Every AI tell and banned item in the text, with line numbers. Language-aware: German text is checked against
    German rules only (English word lists never fire on German prose); the participant's own list always applies."""
    text = _norm(text)
    lang = resolve_lang(text, lang)
    tells: list[Tell] = []
    lines = text.split("\n")
    mine = []
    for raw in extra_banned or []:
        t = _clean_term(raw)
        if t and len(t) <= 70:
            mine.append((t, _user_regex(t)))
    stems = DE_BANNED_STEMS if lang == "de" else BANNED_STEMS
    phrases = DE_BANNED_PHRASES if lang == "de" else BANNED_PHRASES
    transitions = DE_TRANSITIONS if lang == "de" else BANNED_TRANSITIONS
    closings = DE_CLOSINGS if lang == "de" else BANNED_CLOSINGS
    morals = DE_MORAL if lang == "de" else MORAL_OPENERS
    de = lang == "de"

    for i, line in enumerate(lines, 1):
        low = line.lower()
        if "—" in line:
            tells.append(Tell("em-dash", i, "—", "Gedankenstrich (Em dash). Durch Punkt oder Komma ersetzen." if de else "Em dash. Replace with a period or comma."))
        for m in re.finditer(r"\s–\s", line):
            tells.append(Tell("em-dash", i, "–", "Spaced en dash used as a dash. Use a period or comma."))
        for stem in stems:
            for m in re.finditer(r"\b" + re.escape(stem) + r"\w*", low):
                tells.append(Tell("banned-word", i, line[m.start():m.end()], "KI-/Floskelwort. Das einfache Wort nehmen." if de else "Corporate/AI filler. Use the plain word."))
        for ph in phrases:
            if ph in low:
                tells.append(Tell("banned-phrase", i, ph, "KI-Phrase. Streichen oder schlicht sagen." if de else "AI-pattern phrase. Cut or say it plainly."))
        for tr in transitions:
            if re.search(r"(?:^|[.!?]\s+|\n)" + re.escape(tr) + r"\b", low) or low.startswith(tr):
                tells.append(Tell("banned-transition", i, tr, "Füllbrücke. Harter Punkt statt Übergang." if de else "Filler bridge. Use a hard stop instead."))
        stripped = low.strip()
        for cl in closings:
            if stripped == cl or stripped.endswith(cl):
                tells.append(Tell("banned-closing", i, cl, "Floskel-Schluss. Mit etwas Konkretem enden." if de else "Generic closer. End on a specific line."))
        if stripped.startswith(morals):
            tells.append(Tell("tidy-moral", i, stripped[:30], "Ausgesprochene Moral. Die Geschichte trägt die Lehre." if de else "Stated moral. Let the story carry the lesson."))
        for term, rx in mine:
            m = rx.search(line)
            if m:
                tells.append(Tell("your-banned-phrase" if " " in term else "your-banned-word", i, m.group(0),
                                  "Steht auf DEINER Nie-Liste." if de else "On YOUR never-use list."))

    for kind, rx, advice in (_DE_STRUCT if de else _STRUCT):
        for m in rx.finditer(text):
            ln = text.count("\n", 0, m.start()) + 1
            tells.append(Tell(kind, ln, m.group(0).strip()[:80], advice))

    first = next(((i, l) for i, l in enumerate(lines, 1) if l.strip()), None)
    if first and first[1].strip().endswith("?"):
        tells.append(Tell("question-opener", first[0], first[1].strip()[:80],
                          "Beginnt mit einer Frage. Mit Position oder Moment beginnen." if de else "Opens on a question. Open on the position or the moment."))

    paras = [(i, l.strip()) for i, l in enumerate(lines, 1)]
    run: list[tuple[int, str]] = []
    for i, l in paras + [(len(lines) + 1, "")]:
        if l and len(l.split()) <= 5 and not l.startswith(("-", "*", "•")) and not re.match(r"^\d+[.)]", l):
            run.append((i, l))
        else:
            if len(run) >= 3:
                tells.append(Tell("staccato-run", run[0][0], " / ".join(r[1] for r in run[:3]),
                                  "Drei+ Mini-Zeilen für Drama gestapelt. Zusammenführen." if de else "Three+ tiny lines stacked for drama. Merge or vary the rhythm."))
            run = []

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


def fix_dashes(text: str, lang: str = "en") -> tuple[str, int]:
    """Em dashes (and spaced en dashes) -> clean punctuation with correct spacing. Ranges like 2-3 are left alone."""
    n = 0
    out = []
    for line in text.split("\n"):
        if "—" not in line and not re.search(r"\s–\s", line):
            out.append(line)
            continue
        parts = [p.strip() for p in re.split(r"\s*(?:—|\s–\s)\s*", line)]
        parts = [p for p in parts if p]
        if not parts:
            out.append("")
            continue
        s = parts[0]
        for nxt in parts[1:]:
            n += 1
            if lang == "de" or len(s.split()) < 3:
                s = s.rstrip(",;:") + ", " + nxt
            else:
                s = s.rstrip(".,;:") + ". " + nxt[:1].upper() + nxt[1:]
        out.append(s)
    return "\n".join(out), n


def mechanical_clean(text: str, extra_banned: list[str] | None = None, lang: str = "") -> tuple[str, list[str]]:
    """Deterministic clean-up. Returns (new_text, change_log). Never invents content and never changes the
    language of the text: English swaps are applied to English text only."""
    changes: list[str] = []
    t = _norm(text)
    lang = resolve_lang(t, lang)

    t, n = fix_dashes(t, lang)
    changes += ["Gedankenstrich ersetzt" if lang == "de" else "em dash replaced"] * n

    if lang == "de":
        for rx, repl in DE_SWAPS:
            r = re.compile(rx, re.I)
            if r.search(t):
                t = r.sub(lambda m: _match_case(m.group(0), repl + (m.group(1) or "")), t)
                changes.append(f"'{rx.split('(')[0].strip(chr(92) + 'b')}' -> '{repl}'")
        transitions, closings = DE_TRANSITIONS, DE_CLOSINGS
    else:
        for key in sorted(SWAPS, key=len, reverse=True):
            rx = re.compile(r"\b" + re.escape(key) + r"\b", re.I)
            if rx.search(t):
                t = rx.sub(lambda m: _match_case(m.group(0), SWAPS[key]), t)
                changes.append(f"'{key}' -> '{SWAPS[key]}'")
        transitions, closings = BANNED_TRANSITIONS, BANNED_CLOSINGS

    for tr in ([] if lang == "de" else transitions):  # German: flag only; dropping 'Darüber hinaus' breaks verb-second order
        rx = re.compile(r"(^|[.!?]\s+|\n)" + re.escape(tr) + r",?\s+(\w)", re.I)
        if rx.search(t):
            t = rx.sub(lambda m: m.group(1) + m.group(2).upper(), t)
            changes.append(f"Übergang '{tr}' entfernt" if lang == "de" else f"transition '{tr}' removed")

    kept = []
    for line in t.split("\n"):
        if _clean_term(line) in closings:
            changes.append(f"Schluss '{line.strip()}' entfernt" if lang == "de" else f"closing '{line.strip()}' removed")
            continue
        kept.append(line)
    t = "\n".join(kept)

    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)  # no space before punctuation
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
    verbs = r"(?:dm|message|comment|reply|nachricht|schreib\w*|schick\w*|kommentier\w*|antwort\w*|meld\w*)"
    return bool(re.search(r"\b" + verbs + r"\b[^\n]{0,40}?[\"'„“”‘’]?\b[A-ZÄÖÜ][A-ZÄÖÜ0-9]{2,}\b", tail)
                or re.search(r"\b" + verbs + r"\b[^\n]{0,40}?[\"„“'‚‘]([^\"”“'’‘\n]{2,24})[\"”“'’‘]", tail, re.I))


def polish(text: str, platform: str = "linkedin", extra_banned: list[str] | None = None, lang: str = "") -> dict:
    platform = (platform or "linkedin").lower().replace("twitter", "x")
    lo, hi, cap, hook_win = PLATFORMS.get(platform, PLATFORMS["linkedin"])
    lang = resolve_lang(text, lang)
    cleaned, changes = mechanical_clean(text, extra_banned, lang)
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

    tells = find_tells(cleaned, extra_banned, lang)
    return {"language": lang, 
        "platform": platform, "chars": n, "target": f"{lo}-{hi}", "polished": cleaned,
        "mechanical_changes": changes, "structure_issues": issues,
        "remaining_tells": [t.render() for t in tells], "has_keyword_cta": has_kw, "ends_on_question": ends_q,
    }
