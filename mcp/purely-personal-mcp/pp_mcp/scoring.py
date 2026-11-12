"""The Invisibility Diagnostic (0-4): Voice, POV, Specificity, Asking.

Implements the invisibility-diagnostic skill as code so scoring is repeatable.
The Voice test is personalised: it checks the post against the participant's
own word bank, signature phrases and customer phrases, and against the AI
pattern blacklist. A heuristic cannot hear that a sentence is not yours; the
`needs_human_read` note says so.
"""
from __future__ import annotations

import re

from .voice import find_tells, resolve_lang

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
_STANCE_DE = re.compile(
    r"\b(falsch|mythos|stopp\w*|nie|niemals|überschätzt|unterschätzt|lüge|kaputt|fehler|unpopulär|widerspreche|ehrlich gesagt|"
    r"niemand|alle|wahrheit|eigentlich|stattdessen|verzichte|sollte(?:n)? nicht|schlechter rat|verschwendung|vergiss|hör auf|"
    r"die wahre ursache|unsinn|blödsinn|trugschluss|irrtum)\b", re.I)
_EXPLAINERS_DE = re.compile(r"^(?:hier sind|ein leitfaden|tipps für|wege zu|\d+ (?:tipps|wege|dinge))", re.I)
_PERSON_DE = re.compile(r"\b(kunde|kundin|kunden|hersteller|produktionsleiter\w*|betrieb|firma|werk|anlage|linie|gmbh|ag|kg|herr|frau|"
                        r"geschäftsführer\w*|leiter\w*|feinkost\w*|abfüller)\b", re.I)
_EXPLAINERS = re.compile(r"^(?:here are|here's a guide|a guide to|tips for|ways to|\d+ (?:tips|ways|things))", re.I)
_NUM = re.compile(r"(?:\$|£|€)?\d[\d,.]*\s?(?:%|k|m|x|hours?|hrs?|days?|weeks?|months?|years?|clients?|people|calls?|dms?|posts?)?", re.I)
_NAME = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b")


_STOP_CAPS = {
    "I", "A", "An", "The", "This", "That", "These", "Those", "When", "What", "Where", "Why", "How", "Who", "Which", "While", "If", "In", "On", "At", "By", "For",
    "To", "Of", "It", "He", "She", "We", "They", "You", "My", "Our", "Your", "Their", "His", "Her", "Its", "Most", "Last", "Next", "And", "But", "Or", "So", "Then",
    "Here", "There", "Not", "No", "Yes", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "January", "February", "March", "April",
    "May", "June", "July", "August", "September", "October", "November", "December", "AI", "LinkedIn", "ChatGPT", "Claude", "Google", "Instagram", "Facebook",
    "YouTube", "TikTok", "Twitter", "Notion", "Canva", "Zoom", "Slack", "Apify", "GPT", "CEO", "ICP", "DM", "DMs", "PS", "P.S", "Voice", "Today", "Yesterday",
    "Day", "Week", "Month", "Year", "Mr", "Mrs", "Ms", "Dr", "Every", "Each", "Some", "Many", "Any", "All", "One", "Two", "Three", "Fix", "Stop", "Start", "Read",
    "Count", "Ask", "Try", "Let", "Use", "Make", "Take", "Get", "Give", "Keep", "Drop", "Cut", "Add", "Send", "Write", "Think", "Look", "Imagine", "Remember",
}
_PERSON_CUE = re.compile(r"\b(?:called|named|name was|client|customer|member|founder|coach|colleague|friend|mentor|boss|manager|student|user|buyer|prospect)\s+"
                         r"(?:called |named |of mine |I know )?([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?)\b")
_TITLE = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof)\.?\s+([A-Z][a-z]{2,})\b")
_COMPANY = re.compile(r"\b([A-Z][\w&.\-]{2,}(?:\s+[A-Z][\w&.\-]{2,}){0,2})\s+(?:Ltd|Limited|Inc|LLC|GmbH|AG|KG|SE|Corp|Co\.|BV|SA|Pty)\b")


def _numbers(text: str) -> list[str]:
    """Real figures: digits that are not list markers or part of a date-less ordinal."""
    out = []
    for line in text.split("\n"):
        line = re.sub(r"^\s*(?:\d+[.)]\s+|[-*•]\s+)", "", line)
        out += [m.group(0).strip() for m in re.finditer(
            r"(?<![\w.])[$£€]?\d[\d.,]*(?:\s?(?:%|[kKmMxX]\b|hours?|hrs?|minutes?|days?|weeks?|months?|years?|calls?|clients?|customers?|likes?|DMs?|people|posts?|leads?|"
            r"Stunden|Tage[n]?|Wochen|Monate[n]?|Jahre[n]?|Euro|EUR|Kunden|Gläser|Prozent))?", line)]
    return [n for n in out if re.search(r"\d", n)]


def _find_name(text: str, de: bool = False) -> str:
    """A real person or company name: cued by 'called/named/client X', a title (Mr/Dr X), a legal-form company, or a capitalised
    word in mid-sentence that is not a day, month, tool or ordinary word. Generic roles ('a client', 'a founder') never count."""
    for rx in (_PERSON_CUE, _TITLE, _COMPANY):
        m = rx.search(text)
        if m and m.group(1) not in _STOP_CAPS:
            return m.group(1)
    if de:  # German capitalises every noun; only explicit cues count
        m = re.search(r"\b(?:Herr|Frau|Dr\.)\s+([A-ZÄÖÜ][a-zäöüß]{2,})|\b([A-ZÄÖÜ][\wäöüß&.\-]+(?:\s+[A-ZÄÖÜ][\wäöüß&.\-]+){0,2})\s+(?:GmbH|AG|KG|SE|UG|e\.K\.)\b"
                      r"|\b(?:Kunde|Kundin|Kunden|Firma|Betrieb|Herr|Frau)\s+([A-ZÄÖÜ][a-zäöüß]{2,})\b|\b([A-ZÄÖÜ][a-zäöüß]{2,})\s+aus\s+[A-ZÄÖÜ]", text)
        return next((g for g in (m.groups() if m else ()) if g and g not in _STOP_CAPS), "")
    for m in re.finditer(r"(?<=[a-z,;:])\s+([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?)\b", text):  # mid-sentence capitalised word
        cand = m.group(1)
        if cand.split()[0] not in _STOP_CAPS:
            return cand
    return ""


_POV_STRONG = [
    (r"\b(?:is|are|was|were|isn'?t|aren'?t|wasn'?t|weren'?t)(?: not|n'?t)? (?:the |a |an )?(?:problem|issue|point|answer|reason|goal|fix|solution)\b[^.\n]{0,40}[,;.]\s*\w+ (?:is|are|was)\b", "names the real cause"),
    (r"\b\w+ (?:is|are|was|were) not (?:the |a |an )?(?:problem|issue|point|answer|reason|goal)\b", "says what is NOT the problem"),
    (r"\bI (?:told|asked|advised|begged|urged) \w+(?: \w+)? to (?:stop|quit|pause|drop|cut|skip|ignore|delete|delay|say no)\b", "tells someone to stop"),
    (r"\b(?:stop|quit|never|avoid|ignore|forget|skip|delete)\s+(?:\w+ing|\w+)\b", "a direct instruction"),
    (r"\b(?:wrong|myth|mistake|overrated|underrated|lie|lies|scam|waste|broken|unpopular|disagree|bad advice|backwards|nonsense)\b", "calls something wrong"),
    (r"\bthe real (?:problem|reason|issue|cost|reason)\b", "names the real cause"),
    (r"\b(?:don'?t|do not|should(?:n'?t| not)|must(?:n'?t)?) \w+", "says what to do or not do"),
    (r"\b(?:costs?|matters?|pays?|is worth|are worth|is more important|beats?) (?:you )?(?:far )?more than\b", "makes a comparative claim"),
    (r"\bthe (?:one |biggest |worst |only )?(?:mistake|error) (?:\w+ ){0,4}(?:make|made|makes)\b", "names the mistake"),
]
_POV_WEAK = [(r"\b(?:actually|instead|truth|always|nobody|everyone|honestly|rather than)\b", "absolute or contrast word")]
_POV_STRONG_DE = [
    (r"\b(?:ist|sind|war|waren) (?:nicht|kein\w*) (?:das |der |die )?(?:problem|thema|punkt|ursache|grund|lösung)\b", "sagt, was NICHT das Problem ist"),
    (r"\b(?:falsch|mythos|unsinn|blödsinn|trugschluss|irrtum|lüge|kaputt|überschätzt|schlechter rat|verschwendung)\b", "nennt etwas falsch"),
    (r"\b(?:hör(?:t|en)? auf|stopp\w*|vergiss\w*|niemals|lass(?:t|en)? (?:das|es)|verzicht\w*)\b", "klare Anweisung"),
    (r"\bich (?:habe|hab) (?:ihr|ihm|ihnen|ihn|sie)\b[^.\n]{0,40}\b(?:geraten|empfohlen|gesagt)\b[^.\n]{0,30}\b(?:aufzuhören|zu lassen|zu stoppen)", "rät zum Aufhören"),
    (r"\bdie (?:wahre|eigentliche) (?:ursache|grund|problem)\b", "nennt die wahre Ursache"),
    (r"\b(?:kostet|ist|bringt|zählt|wiegt) (?:oft |meist |viel |deutlich )?(?:mehr|wichtiger|teurer|schlimmer) als\b", "behauptet einen Vergleich"),
    (r"\b(?:der|ein|größte[rn]?|häufigste[rn]?|teuerste[rn]?) fehler\b", "benennt den Fehler"),
]
_POV_WEAK_DE = [(r"\b(?:eigentlich|stattdessen|wahrheit|immer|niemand|alle|ehrlich gesagt)\b", "Absolut- oder Kontrastwort")]


def _pov_signals(text: str, de: bool) -> dict:
    strong, weak = [], []
    for pats, bucket in (((_POV_STRONG_DE if de else _POV_STRONG), strong), ((_POV_WEAK_DE if de else _POV_WEAK), weak)):
        for rx, label in pats:
            m = re.search(rx, text, re.I)
            if m:
                bucket.append(f'"{m.group(0).strip()[:40]}" ({label})')
    return {"strong": strong, "weak": weak}


def _split_halves(text: str) -> tuple[str, str]:
    t = text.strip()
    mid = len(t) // 2
    return t[:mid], t[mid:]


def _tail_lines(text: str, n: int = 2) -> str:
    lines = [l for l in text.strip().split("\n") if l.strip()]
    return "\n".join(lines[-n:])


def _asking(text: str, strict: bool) -> tuple[bool, str]:
    tail = _tail_lines(text, 2)
    verbs = r"(?:dm|message|comment|reply|type|nachricht|schreib\w*|schick\w*|kommentier\w*|antwort\w*|meld\w*|tipp\w*)"
    kw = re.search(r"\b" + verbs + r"\b[^\n]{0,40}?[\"'„“”‚‘’]([^\"'„“”‚‘’\n]{2,24})[\"'“”‘’]", tail, re.I) or \
        re.search(r"\b" + verbs + r"\b(?:\s+(?:me|mir|uns))?\s+([A-ZÄÖÜ][A-ZÄÖÜ0-9]{2,})\b", tail)
    if kw:
        return True, f"keyword invitation ('{kw.group(1)}')"
    if not strict and tail.strip().endswith("?") and len(tail.split()) >= 6:
        return True, "closing question to the reader (accepted unless strict=true)"
    return False, "no keyword DM/comment invitation in the last 2 lines" + ("" if strict else " and no direct closing question")


def diagnose(text: str, profile=None, strict_asking: bool = False, lang: str = "") -> dict:
    t = (text or "").strip()
    if not t:
        return {"score": 0, "tier": "Invisible", "dimensions": {}, "fixes": ["Nothing to score."], "chars": 0}

    first, second = _split_halves(t)
    banned = profile.voice["banned"] if profile else []
    lang = resolve_lang(t, lang)
    de = lang == "de"
    tells = find_tells(t, banned, lang)
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
    first_person = bool(re.search(r"\b(ich|mein\w*|wir|unser\w*)\b" if de else r"\b(i|i'm|i've|my|we|our)\b", t, re.I))
    if profile and (profile.voice["word_bank"] or profile.voice["signature_phrases"]):
        voice_ok = len(own) >= 2 and len(hard_tells) <= 1
        voice_why = (f"uses {len(own)} of your own words/phrases ({', '.join(own[:4])})" if voice_ok else
                     f"only {len(own)} of your own words/phrases found" + (f", {len(hard_tells)} AI tells" if hard_tells else ""))
    else:
        voice_ok = first_person and len(hard_tells) == 0
        voice_why = ("first-person and clean of AI tells (no Voice DNA loaded, so this is a weak proxy)" if voice_ok else
                     "no personal markers or AI tells present (load your Voice DNA for a real voice check)")

    # ---- POV: does it take a side? ---------------------------------------------------------------------------------
    sides = _pov_signals(t, de)
    explainer = bool((_EXPLAINERS_DE if de else _EXPLAINERS).match(t))
    pov_ok = (len(sides["strong"]) >= 1 or len(sides["weak"]) >= 2) and not explainer
    shown = sides["strong"][:3] + sides["weak"][:2]
    pov_why = ("takes a side (" + "; ".join(shown) + ")" if pov_ok else
               "reads as explanation: no clear side taken" if not shown else f"only a hint of a side ({'; '.join(shown)}): state the position outright")

    # ---- Specificity: a real NAME and a real NUMBER in the first half ---------------------------------------------
    nums = _numbers(first)
    name = _find_name(first, de)
    spec_ok = bool(nums) and bool(name)
    spec_why = (f"a number ({nums[0]}) and a name ({name}) in the first half" if spec_ok else
                f"a number ({nums[0]}) but no real name (a role like 'a client' or 'a founder' does not count)" if nums else
                f"a name ({name}) but no number" if name else "no real name and no number in the first half")

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
