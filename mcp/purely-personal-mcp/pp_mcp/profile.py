"""A participant's profile: Business Brain + ICP + Voice DNA, parsed.

The three Day 1 documents are written by Claude from the participant's
own answers, so their headings vary. Parsing is therefore best-effort and
heading-driven; the raw documents are always kept and always passed
through to the work orders. Parsed fields feed the deterministic checks
(banned words, word bank, customer phrases) and the readiness audit.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

MAX_DOC = 200_000  # characters per document

DEFAULT_BRAND = {"accent": "#e90d41", "ink": "#0d0d0f", "paper": "#fbfbf9", "secondary": "#4a4e54"}


# ----------------------------------------------------------------------------
# Markdown helpers
# ----------------------------------------------------------------------------
_HEAD = re.compile(
    r"^(?:#{1,6}\s+(?P<h>.+?)|\*\*(?P<b>[^*]{3,80})\*\*:?|(?:SECTION\s+\d+[,.:]?\s*)?(?P<c>[A-Z][A-Z0-9 &'/,\-]{3,70}))\s*:?\s*$"
)


def _strip(s: str) -> str:
    return re.sub(r"[`*_]+", "", s or "").strip()


def split_sections(md: str) -> list[dict]:
    sections: list[dict] = [{"title": "", "body": []}]
    for raw in (md or "").replace("\r", "").split("\n"):
        line = raw.rstrip()
        m = _HEAD.match(line.strip()) if line.strip() else None
        if m and not line.strip().startswith(("-", "*", "|", ">")) or (m and line.strip().startswith("**")):
            title = _strip(m.group("h") or m.group("b") or m.group("c"))
            # skip "heading" lines that are really sentences / bullets
            if title and len(title.split()) <= 10 and not title.endswith((".", "?")):
                sections.append({"title": title, "body": []})
                continue
        sections[-1]["body"].append(raw)
    return [{"title": s["title"], "key": s["title"].lower(), "body": "\n".join(s["body"]).strip()} for s in sections]


def find_sections(secs: list[dict], *needles: str) -> str:
    out = []
    for s in secs:
        if any(n in s["key"] for n in needles) and s["body"]:
            out.append(s["body"])
    return "\n".join(out)


def bullets(body: str) -> list[str]:
    items = []
    for line in (body or "").split("\n"):
        m = re.match(r"^\s*(?:[-*•]|\d+[.)])\s+(.*)$", line)
        if m:
            items.append(_strip(m.group(1)))
    if not items:
        # a single short comma-separated line of short items
        lines = [l for l in (body or "").split("\n") if l.strip()]
        if len(lines) <= 2:
            flat = " ".join(lines)
            if flat.count(",") >= 3 and len(flat) < 1200:
                items = [_strip(x) for x in flat.split(",") if len(x.split()) <= 5 and not x.strip().endswith(".")]
    return [i for i in items if i]


def quoted(body: str) -> list[str]:
    q = re.findall(r"[\"“]([^\"”\n]{2,90})[\"”]", body or "")
    q += re.findall(r"`([^`\n]{2,60})`", body or "")
    return [x.strip() for x in q if x.strip()]


def _dedupe_prefix(items: list[str], limit: int = 12) -> list[str]:
    seen, out = set(), []
    for i in items:
        k = re.sub(r"[^a-z ]", "", re.split(r"[.:]", i)[0].lower()).strip()
        if k and k not in seen:
            seen.add(k)
            out.append(i)
    return out[:limit]


def _dedupe(items: list[str], limit: int = 80) -> list[str]:
    seen, out = set(), []
    for i in items:
        k = i.lower().strip()
        if k and k not in seen:
            seen.add(k)
            out.append(i.strip())
    return out[:limit]


# ----------------------------------------------------------------------------
# Extraction
# ----------------------------------------------------------------------------

def extract_voice(*docs: str) -> dict:
    word_bank, signature, banned, rules, redflags = [], [], [], [], []
    test_line, rhythm = "", ""
    for md in docs:
        if not md:
            continue
        secs = split_sections(md)
        wb = find_sections(secs, "word bank", "my language", "vocabulary")
        for b in bullets(wb):
            if len(b.split()) <= 6:
                word_bank.append(b)
        for b in bullets(find_sections(secs, "word bank")) or []:
            word_bank.append(b)
        for m in re.finditer(r"Word bank\s*:\s*([^\n]+?)(?:\.\s+Signature|\n|$)", md, re.I):
            word_bank += [_strip(x) for x in m.group(1).split(",") if x.strip() and len(x.split()) <= 5]
        for m in re.finditer(r"Signature phrases?\s*:\s*([^\n]+)", md, re.I):
            signature += quoted(m.group(1))
        sig = find_sections(secs, "signature")
        for line in sig.split("\n"):
            q = quoted(line)
            if q:
                signature.append(q[0])
            else:
                m = re.match(r"^\s*(?:[-*•]|\d+[.)])\s+(.*?)(?:\s[-:]\s|$)", line)
                if m and len(m.group(1).split()) <= 8:
                    signature.append(_strip(m.group(1)))
        nv = find_sections(secs, "never", "banned", "red flag", "forbidden", "words you never", "do not use")
        banned += quoted(nv)
        for b in bullets(nv):
            if len(b.split()) <= 6:
                banned.append(b)
        for line in (md or "").split("\n"):
            m = re.match(r"^\s*(?:WORDS I NEVER USE|Words you never use|Banned(?: words)?)\s*:\s*(.+)$", line, re.I)
            if m:
                banned += [x.strip(" .`*\"'") for x in m.group(1).split(",") if x.strip()]
            m = re.match(r"^\s*NEVER:\s*[\"“](.+?)[\"”]", line)
            if m:
                banned.append(m.group(1))
        rl = find_sections(secs, "writing rules", "my rules", "rules")
        for line in rl.split("\n"):
            m = re.match(r"^\s*(?:RULE\s*\d+\s*[:.\-]\s*|(?:\d+[.)]|[-*•])\s+)(.+)$", line, re.I)
            if m:
                rules.append(_strip(m.group(1))[:200])
        rhythm = rhythm or find_sections(secs, "rhythm")[:600]
        for line in md.split("\n"):
            if re.match(r"^\s*[\"“]?\s*If it does not sound like", line, re.I):
                test_line = _strip(line).strip("\"“” ")
        t = find_sections(secs, "the test")
        if t and not test_line:
            test_line = _strip(t.split("\n")[0])
    return {
        "word_bank": _dedupe(word_bank, 40),
        "signature_phrases": _dedupe(signature, 15),
        "banned": _dedupe([b.strip(" .") for b in banned if len(b) <= 70 and not re.match(r"(?i)^(no|never|always)\s", b.strip())
                           and not b.strip().lower().startswith(("if it ", "rewrite"))], 80),
        "rules": _dedupe_prefix(rules, 12),
        "rhythm": rhythm,
        "test_line": test_line,
    }


def extract_icp(*docs: str) -> dict:
    persona, their_words, objections, themes, triggers, tried, want = "", [], [], [], "", "", ""
    for md in docs:
        if not md:
            continue
        secs = split_sections(md)
        persona = persona or find_sections(secs, "the person", "one person i write for", "persona")
        tw = find_sections(secs, "their words", "phrases", "words they use")
        their_words += [q for q in quoted(tw)] or bullets(tw)
        ob = find_sections(secs, "objection", "make them say no", "say no")
        for line in ob.split("\n"):
            m = re.match(r"^\s*(?:[-*•]|\d+[.)])\s+(.*)$", line)
            if m:
                objections.append(_strip(m.group(1))[:240])
            elif line.strip().startswith("|") and not set(line.strip()) <= set("|-: "):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[0].lower() not in ("objection", "reason", "what they want"):
                    objections.append(_strip(cells[0])[:240])
        th = find_sections(secs, "what to talk about", "themes", "own")
        themes += bullets(th)
        triggers = triggers or find_sections(secs, "triggers", "how they buy", "decide")
        tried = tried or find_sections(secs, "already tried", "tried")
        want = want or find_sections(secs, "what they want", "want")
    return {
        "persona": persona[:1200], "their_words": _dedupe(their_words, 20),
        "objections": _dedupe(objections, 10), "themes": _dedupe(themes, 10),
        "triggers": triggers[:800], "tried": tried[:600], "want": want[:800],
    }


def extract_brand(*docs: str) -> dict:
    text = "\n".join(d for d in docs if d)
    brand: dict = {}
    roles = {"accent": "accent", "primary": "accent", "highlight": "accent", "secondary": "secondary",
             "ink": "ink", "text": "ink", "paper": "paper", "background": "paper", "bg": "paper"}
    for m in re.finditer(r"\b(accent|primary|highlight|secondary|ink|text|paper|background|bg)\b\W{0,14}(#[0-9a-fA-F]{6})\b", text, re.I):
        brand.setdefault(roles[m.group(1).lower()], m.group(2).lower())
    fonts = re.findall(r"(?:font|typeface)s?\s*[:\-]\s*([A-Za-z0-9 ,&+\-]{3,60})", text, re.I)
    if fonts:
        brand["fonts"] = fonts[0].strip()
    return brand


def extract_name(brain: str, icp: str, voice: str) -> str:
    for md in (brain, voice, icp):
        m = re.search(r"(?:\*\*)?Name(?:\*\*)?\s*[:\-]\s*([A-Z][^\n*|]{2,60})", md or "")
        if m:
            return _strip(m.group(1))
        m = re.search(r"#\s*(?:BUSINESS BRAIN|Voice (?:DNA|Profile)|ICP)\s*[—\-:·]\s*(.+)", md or "", re.I)
        if m:
            return _strip(m.group(1))
    m = re.search(r"^\s*1\.\s*WHO I AM\s*\n+\s*([A-Z][A-Za-z.\- ]{2,40})[,.]", brain or "", re.M | re.I)
    return _strip(m.group(1)) if m else ""


# ----------------------------------------------------------------------------
# Profile model
# ----------------------------------------------------------------------------
@dataclass
class Profile:
    token: str = ""
    name: str = ""
    brain: str = ""
    icp: str = ""
    voice_dna: str = ""
    language: str = "English"
    never_claim: str = ""
    platform: str = "linkedin"
    handle: str = ""
    brand: dict = field(default_factory=dict)
    demo: bool = False
    created: str = ""
    updated: str = ""

    # -- parsed (computed on demand, cheap) -----------------------------
    @property
    def voice(self) -> dict:
        return extract_voice(self.voice_dna, self.brain)

    @property
    def customer(self) -> dict:
        return extract_icp(self.icp, self.brain)

    @property
    def colours(self) -> dict:
        out = dict(DEFAULT_BRAND)
        out.update(extract_brand(self.brain, self.voice_dna, self.icp))
        out.update({k: v for k, v in (self.brand or {}).items() if v})
        return out

    def to_dict(self) -> dict:
        return {
            "name": self.name, "brain": self.brain, "icp": self.icp, "voice_dna": self.voice_dna,
            "language": self.language, "never_claim": self.never_claim, "platform": self.platform,
            "handle": self.handle, "brand": self.brand, "created": self.created, "updated": self.updated,
        }

    @classmethod
    def from_dict(cls, token: str, d: dict) -> "Profile":
        keys = {"name", "brain", "icp", "voice_dna", "language", "never_claim", "platform", "handle", "brand", "created", "updated"}
        return cls(token=token, **{k: v for k, v in d.items() if k in keys})

    # -- readiness ------------------------------------------------------
    def audit(self) -> dict:
        v, c = self.voice, self.customer
        checks: list[tuple[str, bool, str, int]] = [
            ("Business Brain present", len(self.brain) > 300, "Paste BUSINESS-BRAIN.md (Day 1, Step 3).", 20),
            ("ICP present", len(self.icp) > 300 or len(c["persona"]) > 100,
             "Paste ICP.md (Day 1, Step 1) or make sure the Brain has the customer section.", 15),
            ("Voice DNA present", len(self.voice_dna) > 300 or bool(v["word_bank"]),
             "Paste VOICE-DNA.md (Day 1, Step 2).", 15),
            ("Word bank (20+ words)", len(v["word_bank"]) >= 20,
             f"Found {len(v['word_bank'])}. The voice check needs 20+ of your own words.", 10),
            ("Signature phrases (5+)", len(v["signature_phrases"]) >= 5,
             f"Found {len(v['signature_phrases'])}. Re-run Voice DNA Step 2 with messier, longer spoken answers.", 8),
            ("Banned list (8+)", len(v["banned"]) >= 8, f"Found {len(v['banned'])} banned items.", 7),
            ("Customer phrases (8+)", len(c["their_words"]) >= 8,
             f"Found {len(c['their_words'])}. Hooks are built from these, so thin = generic.", 10),
            ("Objections (3+)", len(c["objections"]) >= 3, f"Found {len(c['objections'])}.", 7),
            ("Never-claim guard rail", bool(self.never_claim.strip()),
             "Add what the employee must never claim (results, clients, numbers).", 5),
            ("Name known", bool(self.name), "Pass name= to set_my_context.", 3),
        ]
        score = sum(w for _, ok, _, w in checks if ok)
        return {
            "score": score,
            "checks": [{"check": n, "ok": ok, "fix": "" if ok else fix} for n, ok, fix, _ in checks],
            "ready": score >= 70,
            "counts": {
                "word_bank": len(v["word_bank"]), "signature_phrases": len(v["signature_phrases"]),
                "banned": len(v["banned"]), "writing_rules": len(v["rules"]),
                "customer_phrases": len(c["their_words"]), "objections": len(c["objections"]),
                "themes": len(c["themes"]),
            },
        }

    def clipped(self) -> "Profile":
        for f in ("brain", "icp", "voice_dna"):
            setattr(self, f, (getattr(self, f) or "")[:MAX_DOC])
        return self
